import typing
import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException
import yaml
import os
import chardet
from io import StringIO


def ssh_connect(server):
    """Creates an SSH connection to a server."""
    if server.password:
        auth = {'password': server.password}
    else:
        key = paramiko.RSAKey.from_private_key(StringIO(server.private_key), password=server.private_key_password)
        auth = {'pkey': key}

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(server.host, server.port, server.username, **auth)
    except (AuthenticationException, SSHException) as e:
        print(f"Failed to connect to {server.name} {server.host}:{server.port}: {e}")
        return None
    return ssh


def list_files(server, path="."):
    """Returns a list of files at a given path on an SSH server."""
    ssh = ssh_connect(server)
    if ssh is None:
        return []

    sftp = ssh.open_sftp()
    try:
        files = sftp.listdir(path)
    except IOError:
        files = []
    sftp.close()
    ssh.close()
    return files


def get_file(server, path):
    """Downloads a file from an SSH server."""
    ssh = ssh_connect(server)
    if ssh is None:
        return None
    sftp = ssh.open_sftp()
    print(f"path: {server.name} - {server.host}:{server.port} {path}")
    try:
        file = sftp.file(path)
        data = file.read().decode("utf-8")
        print(f"data: {data}")
    except IOError:
        data = None
    sftp.close()
    ssh.close()
    return data


def save_file(server, path, data):
    """Uploads a file to an SSH server."""
    ssh = ssh_connect(server)
    if ssh is None:
        return False
    sftp = ssh.open_sftp()
    try:
        with sftp.open(path, "w") as file:
            file.write(data)
    except IOError:
        sftp.close()
        ssh.close()
        return False
    sftp.close()
    ssh.close()
    return True


def execute_command(server, command):
    # print("#####00", command, type(command))
    ssh = ssh_connect(server)
    stdin, stdout, stderr = ssh.exec_command(command)
    bstdout = stdout.read()
    bstderr = stderr.read()
    # 检测 stdout 和 stderr 的编码方式
    _encoding = chardet.detect(bstdout + bstderr)['encoding']
    #print("#####11", bstdout + bstderr, _encoding)
    # 解码 stdout 和 stderr 为字符串
    output = bstdout.decode(_encoding)
    error = bstderr.decode(_encoding)
    ssh.close()
    # print("#####22", output, error, _encoding)
    return output, error



def load_config(config_path):
    """Loads a YAML configuration file."""
    if not os.path.exists(config_path):
        return None
    with open(config_path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config


def save_config(config_path, config):
    """Saves a YAML configuration file."""
    with open(config_path, "w") as file:
        yaml.dump(config, file)
