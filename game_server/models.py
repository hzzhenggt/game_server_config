from django.db import models

from .utils import ssh_connect, list_files, get_file, save_file, execute_command


class Server(models.Model):
    name = models.CharField(max_length=100, unique=True)
    host = models.CharField(max_length=100)
    port = models.IntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)
    private_key_password = models.CharField(max_length=100, blank=True, null=True, default="")

    def __str__(self):
        return self.host
    
    def get_ssh_client(self):
        ssh = ssh_connect(self)
        return ssh


class ServerFile(models.Model):
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
    
    

class Command(models.Model):
    name = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    lastrun = models.DateTimeField(null=True, blank=True)
    lastresult = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class HistoryAction:
    """操作类型"""
    ExecCmd = 'exec_cmd'
    UploadFile = 'upload_file'


class History(models.Model):
    # user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    user = models.CharField(max_length=100, null=True, blank=True, default="")
    server = models.CharField(max_length=100, null=True, blank=True, default="")
    action = models.CharField(max_length=100, null=True, blank=True, default="")
    content = models.TextField(null=True, blank=True)
    result = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.server} - {self.action}'