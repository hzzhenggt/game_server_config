import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException
import yaml
import os


def ssh_connect(server):
    """Creates an SSH connection to a server."""
    if server.password:
        auth = {'password': server.password}
    else:
        key = paramiko.RSAKey.from_private_key(server.private_key, password=server.private_key_password)
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
    try:
        file = sftp.file(path)
        data = file.read().decode("utf-8")
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
    """Runs a command on an SSH server."""
    ssh = ssh_connect(server)
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    ssh.close()
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
