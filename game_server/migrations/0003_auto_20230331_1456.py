# Generated by Django 3.2.5 on 2023-03-31 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_server', '0002_auto_20230331_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serverfile',
            name='path',
        ),
        migrations.AddField(
            model_name='serverfile',
            name='deploy_path',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]