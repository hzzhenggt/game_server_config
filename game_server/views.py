
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from django.utils.html import escape
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Command, History, HistoryAction, Server, ServerFile
from .forms import CommandForm, ServerForm, ServerFileForm
from .utils import ssh_connect, list_files, get_file, save_file, execute_command

import os
import difflib
# import pygments
# from pygments.lexers import get_lexer_for_filename
# from pygments.formatters import HtmlFormatter


def history_list(request):
    historys = History.objects.all().order_by('-created')
    paginator = Paginator(historys, 10)  # 10 items per page
    page = request.GET.get('page')
    try:
        historys = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        historys = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        historys = paginator.page(paginator.num_pages)

    return render(request, 'viewer/history_list.html', {'historys': historys})


def history_detail(request, pk):
    history = get_object_or_404(History, pk=pk)
    return render(request, 'viewer/history_detail.html', {"history": history})


def server_list(request):
    servers = Server.objects.all().order_by('-id')
    paginator = Paginator(servers, 10)  # 10 items per page
    page = request.GET.get('page')
    try:
        servers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        servers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        servers = paginator.page(paginator.num_pages)
    return render(request, 'viewer/server_list.html', {'servers': servers})


def server_file_list(request):
    server_files = ServerFile.objects.all().order_by('-id')
    paginator = Paginator(server_files, 10)  # 10 items per page
    page = request.GET.get('page')
    try:
        server_files = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        server_files = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        server_files = paginator.page(paginator.num_pages)
    return render(request, 'viewer/server_file_list.html', {'server_files': server_files})


def server_add(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
            # Check if server with given name already exists
            if Server.objects.filter(name=form.cleaned_data['name']).exists():
                messages.error(
                    request, 'Server with given name already exists.')
                return render(request, 'viewer/server_form.html', {'form': form})
            form.save()
            return redirect('server_list')
    else:
        form = ServerForm()
    return render(request, 'viewer/server_form.html', {'form': form})


def server_edit(request, pk):
    server = get_object_or_404(Server, pk=pk)
    if request.method == 'POST':
        form = ServerForm(request.POST, instance=server)
        if form.is_valid():
            form.save()
            return redirect('server_list')
    else:
        form = ServerForm(instance=server)
    return render(request, 'viewer/server_form.html', {'form': form})


def server_delete(request, pk):
    server = get_object_or_404(Server, pk=pk)
    if request.method == 'POST':
        server.delete()
        return redirect('server_list')
    return render(request, 'viewer/server_confirm_delete.html', {'object': server})


def server_detail(request, pk):
    server = get_object_or_404(Server, pk=pk)
    files = ServerFile.objects.filter(server=server)

    context = {
        'server': server,
        'files': files,
    }

    return render(request, 'viewer/server_detail.html', context)


def server_file_detail(request, pk):
    # ...
    if request.method == 'GET':
        server_file = get_object_or_404(ServerFile, pk=pk)
        content = server_file.content
        if content is None:
            content = ''
        # else:
        #     lexer = get_lexer_for_filename(server_file.name)
        #     formatter = HtmlFormatter(style='colorful')
        #     content = pygments.highlight(content, lexer, formatter)
        return render(request, 'viewer/server_file_detail.html', {'file': server_file, 'content': content})
# class ServerFileDetailView(DetailView):
#     model = ServerFile
#     template_name = 'viewer/server_file_detail.html'
#     context_object_name = 'server_file'

#     def get(self, request, pk, *args, **kwargs):
#         self.object = self.get_object()
#         context = self.get_context_data(object=self.object)
#         context['content'] = self.object.get_file_content()
#         return self.render_to_response(context)

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         deploy_path = request.POST.get('deploy_path')
#         self.object.deploy_file(deploy_path)
#         return HttpResponseRedirect(reverse('server_file_list'))


def get_file_content(request, pk):
    server_file = get_object_or_404(ServerFile, pk=pk)
    content = get_file(server_file.server, server_file.deploy_path)
    return render(request, 'viewer/server_file_content.html', {'server_file': server_file, 'content': content})


@csrf_exempt
def deploy_file(request, pk):
    server_file = get_object_or_404(ServerFile, pk=pk)

    if request.method == 'POST':
        form = ServerFileForm(request.POST, request.FILES, instance=server_file)
        if form.is_valid():
            form.save()
            save_file(server_file.server, server_file.deploy_path, server_file.content)
            messages.success(request, 'File deployed successfully.')
            return redirect('server_detail', pk=server_file.server.pk)
    else:
        form = ServerFileForm(instance=server_file)

    return render(request, 'viewer/server_file_deploy.html', {'server_file': server_file, 'form': form})


def server_file_add(request, pk):
    server = get_object_or_404(Server, pk=pk)
    if request.method == 'POST':
        form = ServerFileForm(request.POST)
        if form.is_valid():
            server_file = form.save(commit=False)
            server_file.server = server
            server_file.size = len(server_file.content)
            server_file.save()
            return HttpResponseRedirect(reverse('server_detail', args=[pk]))
    else:
        form = ServerFileForm()
    context = {
        'server': server,
        'form': form,
    }
    return render(request, 'viewer/server_file_add.html', context)


def server_file_edit(request, pk):
    server_file = get_object_or_404(ServerFile, pk=pk)

    if request.method == 'POST':
        form = ServerFileForm(request.POST, instance=server_file)
        if form.is_valid():
            server_file = form.save(commit=False)
            server_file.save()
            return redirect('server_file_detail', pk=pk)
    else:
        form = ServerFileForm(instance=server_file)

    return render(request, 'viewer/server_file_edit.html', {'form': form, 'server_file': server_file, 'title': 'Edit Server File'})


def server_file_compare(request, pk):
    server_file = get_object_or_404(ServerFile, pk=pk)
    server = server_file.server

    # Get the contents of the server file
    server_file_content = server_file.content

    # Get the contents of the remote file
    remote_file_content = get_file(server, server_file.deploy_path)
    if remote_file_content is None:
        remote_file_content = ''

    # Do the diff
    d = difflib.Differ()
    diff = list(d.compare(server_file_content.splitlines(), remote_file_content.splitlines()))

    context = {
        "server":server, 
        'server_file': server_file,
        'diff': diff
    }
    return render(request, 'viewer/server_file_compare.html', context)


class ServerFileDeleteView(DeleteView):
    model = ServerFile
    template_name = 'viewer/server_file_delete.html'
    success_url = reverse_lazy('server_list')


def file_detail(request, pk, path):
    # server_file = get_object_or_404(ServerFile, pk=pk)
    server = get_object_or_404(Server, pk=pk)
    server_file = path
    file_content = get_file(server, path)
    return render(request, 'viewer/file_detail.html', {'file': server_file, 'file_content': file_content})


def file_edit(request, pk):
    server_file = get_object_or_404(ServerFile, pk=pk)
    server = server_file.server
    if request.method == 'POST':
        file_content = request.POST['file_content']
        save_file(server_file, file_content)
        return redirect('file_detail', pk=pk)
    else:
        file_content = get_file(server_file)
    return render(request, 'viewer/file_edit.html', {'file': server_file, 'file_content': file_content})




def command_list(request):
    commands = Command.objects.all()
    # search
    search_query = request.GET.get('search')
    if search_query:
        commands = commands.filter(Q(name__icontains=search_query))
    # pagination
    paginator = Paginator(commands, 10)
    page = request.GET.get('page')
    try:
        commands = paginator.page(page)
    except PageNotAnInteger:
        commands = paginator.page(1)
    servers = Server.objects.all()
    return render(request, 'viewer/commands.html', {'commands': commands, 'servers': servers})



def add_command(request):
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Command added successfully.')
            return redirect('commands')
    else:
        form = CommandForm()
    return render(request, 'viewer/add_command.html', {'form': form})


def edit_command(request, pk):
    command = get_object_or_404(Command, pk=pk)
    if request.method == 'POST':
        form = CommandForm(request.POST, instance=command)
        if form.is_valid():
            form.save()
            return redirect('commands')
    else:
        form = CommandForm(instance=command)
    return render(request, 'viewer/edit_command.html', {'form': form, 'command': command})


def delete_command(request, pk):
    command = get_object_or_404(Command, pk=pk)
    command.delete()
    return redirect('commands')



def create_history(request, action, server, content, result):
    """创建一个历史记录"""
    try:
        his_data = {
            "user": f"{request.user}",
            "action": f"{action}",
            "server": f"{server}",
            "content": f"{content}",
            "result": f"{result}",
        }
        his = History.objects.create(**his_data)
        print(f"create history {his.id}: {his_data}")
    except Exception as e:
        print(f"create history error: {e}")


@csrf_exempt
def handle_execute_command(request):
    if request.method == 'POST':
        content = request.POST['command']
        server_id = request.POST['server']
        server = get_object_or_404(Server, pk=server_id)
        output, error = execute_command(server, content)
        result = {'output': output, 'error': error}
        create_history(request, HistoryAction.ExecCmd, server, content, result)
        return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'output': "", 'error': "method must be post"}, safe=False, json_dumps_params={'ensure_ascii': False})


def commands(request):
    return command_list(request)


@csrf_exempt
def run_command(request):
    """执行 command
    需要 post 两个参数 command 和 server
    """
    if request.method == 'POST':
        command_id = request.POST['command']
        server_id = request.POST['server']
        server = get_object_or_404(Server, pk=server_id)
        command = get_object_or_404(Command, pk=command_id)
        output, error = execute_command(server, command.content)
        result = {'output': output, 'error': error}
        create_history(request, HistoryAction.ExecCmd, server, command.content, result)
        return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({'output': "", 'error': "method must be post"}, safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def upload_file(request, pk):
    server = get_object_or_404(Server, pk=pk)
    if request.method == 'POST':
        file_obj = request.FILES['file']
        file_path = request.POST['file_path']
        server_file = ServerFile(
            server=server, path=file_path, content=file_obj.read().decode('utf-8'))
        server_file.save()
        return redirect('server_detail', pk=server.pk)
    else:
        return render(request, 'viewer/upload_file.html', {'server': server})


def download_file(request, pk):
    """
    Downloads a file from a server and returns it as an attachment.
    """
    server_file = get_object_or_404(ServerFile, pk=pk)
    server = server_file.server
    ssh = ssh_connect(server)

    sftp = ssh.open_sftp()
    remote_file = os.path.join(server_file.directory, server_file.name)
    try:
        f = sftp.file(remote_file, 'r')
        response = HttpResponse(f.read())
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
            server_file.name)
        response['Content-Type'] = 'application/octet-stream'
        return response
    except IOError:
        return HttpResponse('Error: Could not download file.')

    finally:
        ssh.close()
