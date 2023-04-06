from django.db import models

from .utils import ssh_connect, list_files, get_file, save_file, execute_command
from django.contrib.auth.models import User, Group


class Project(Group):
    admins = models.ManyToManyField(User, related_name='project_admins', blank=True)
    users = models.ManyToManyField(User, related_name='projects', blank=True)


class Server(models.Model):
    name = models.CharField(max_length=100, unique=True)
    host = models.CharField(max_length=100)
    port = models.IntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)
    private_key_password = models.CharField(max_length=100, blank=True, null=True, default="")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='servers', blank=True, null=True)

    def __str__(self):
        return self.host

    def get_ssh_client(self):
        ssh = ssh_connect(self)
        return ssh

    class Meta:
        permissions = (
            ('can_view_server', 'Can view server'),
            ('can_add_server', 'Can add server'),
            ('can_change_server', 'Can change server'),
            ('can_delete_server', 'Can delete server'),
        )


class ServerFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='server_files', blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True, default="新的文件")
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='files')
    deploy_path = models.CharField(max_length=1000, blank=True, null=True, default="")
    size = models.BigIntegerField(default=0)
    content = models.TextField(blank=True, null=True, default="")
    last_modified = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True, default="")

    def __str__(self):
        return self.deploy_path

    def get_file_content(self):
        return get_file(self.server, self.deploy_path)

    def deploy_file(self, deploy_path):
        return save_file(self.server, deploy_path, self.content)
    
    class Meta:
        permissions = (
            ('can_view_serverfile', 'Can view serverfile'),
            ('can_add_serverfile', 'Can add serverfile'),
            ('can_change_serverfile', 'Can change serverfile'),
            ('can_delete_serverfile', 'Can delete serverfile'),
        )


class Command(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='server_commands', blank=True, null=True)
    name = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    lastrun = models.DateTimeField(null=True, blank=True)
    lastresult = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        permissions = (
            ('can_view_command', 'Can view command'),
            ('can_add_command', 'Can add command'),
            ('can_change_command', 'Can change command'),
            ('can_delete_command', 'Can delete command'),
        )


class HistoryAction:
    """操作类型"""
    ExecCmd = 'exec_cmd'
    UploadFile = 'upload_file'


class History(models.Model):
    # user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='server_historys', blank=True, null=True)
    user = models.CharField(max_length=100, null=True, blank=True, default="")
    server = models.CharField(max_length=100, null=True, blank=True, default="")
    action = models.CharField(max_length=100, null=True, blank=True, default="")
    content = models.TextField(null=True, blank=True)
    result = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.server} - {self.action}'
    
    class Meta:
        permissions = (
            ('can_view_history', 'Can view history'),
            ('can_add_history', 'Can add history'),
            ('can_change_history', 'Can change history'),
            ('can_delete_history', 'Can delete history'),
        )
