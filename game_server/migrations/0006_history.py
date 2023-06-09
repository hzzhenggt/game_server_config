# Generated by Django 3.2.5 on 2023-04-03 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_server', '0005_command'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('server', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('result', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
