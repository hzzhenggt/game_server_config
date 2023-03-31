from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Server, ServerFile
from .forms import ServerForm
from .utils import ssh_connect, list_files, get_file, save_file, execute_command

def server_list(request):
    servers = Server.objects.all()
    return render(request, 'viewer/server_list.html', {'servers': servers})

def server_add(request):
    if request.method == 'POST':
        form = ServerForm(request.POST)
        if form.is_valid():
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
    files = list_files(server, '/srv/conf/')
    return render(request, 'viewer/server_detail.html', {'server': server, 'files': files})

def file_detail(request, pk):
    server_file = get_object_or_404(ServerFile, pk=pk)
    file_content = get_file(server_file)
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

@csrf_exempt
def run_command(request, pk):
    server = get_object_or_404(Server, pk=pk)
    if request.method == 'POST':
        command = request.POST['command']
        output, error = execute_command(server, command)
        return JsonResponse({'output': output, 'error': error})
    else:
        return render(request, 'viewer/run_command.html', {'server': server})

@csrf_exempt
def upload_file(request, pk):
    server = get_object_or_404(Server, pk=pk)
    if request.method == 'POST':
        file_obj = request.FILES['file']
        file_path = request.POST['file_path']
        server_file = ServerFile(server=server, path=file_path, content=file_obj.read().decode('utf-8'))
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
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(server_file.name)
        response['Content-Type'] = 'application/octet-stream'
        return response
    except IOError:
        return HttpResponse('Error: Could not download file.')

    finally:
        ssh.close()

   
