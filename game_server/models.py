from django.db import models

# Create your models here.
from django.db import models


class Server(models.Model):
    name = models.CharField(max_length=100, unique=True)
    host = models.CharField(max_length=100)
    port = models.IntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.host
    


class ServerFile(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.server.name} - {self.path}/{self.name}'
