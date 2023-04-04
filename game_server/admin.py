
# Register your models here.
from django.contrib import admin
from .models import Command, Server, ServerFile

admin.site.register(Command)
admin.site.register(Server)
admin.site.register(ServerFile)
