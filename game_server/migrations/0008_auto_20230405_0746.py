# Generated by Django 3.2.5 on 2023-04-04 23:46

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('game_server', '0007_history_action'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='command',
            options={'permissions': (('can_view_command', 'Can view command'), ('can_add_command', 'Can add command'), ('can_change_command', 'Can change command'), ('can_delete_command', 'Can delete command'))},
        ),
        migrations.AlterModelOptions(
            name='history',
            options={'permissions': (('can_view_history', 'Can view history'), ('can_add_history', 'Can add history'), ('can_change_history', 'Can change history'), ('can_delete_history', 'Can delete history'))},
        ),
        migrations.AlterModelOptions(
            name='server',
            options={'permissions': (('can_view_server', 'Can view server'), ('can_add_server', 'Can add server'), ('can_change_server', 'Can change server'), ('can_delete_server', 'Can delete server'))},
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('group_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.group')),
                ('admins', models.ManyToManyField(blank=True, related_name='project_admins', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(blank=True, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.AddField(
            model_name='command',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='server_commands', to='game_server.project'),
        ),
        migrations.AddField(
            model_name='history',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='server_historys', to='game_server.project'),
        ),
        migrations.AddField(
            model_name='server',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='servers', to='game_server.project'),
        ),
        migrations.AddField(
            model_name='serverfile',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='server_files', to='game_server.project'),
        ),
    ]
