import paramiko
from scp import SCPClient

from typing import Optional

def get_ssh_connection(hostname, username: str, password: str, port=22):
    """Creates an SSH connection for a given hostname."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port=port, username=username, password=password)
    return ssh

def copy_file_to_remote(
    filepath: str, 
    remote_dir: str = '', 
    ssh_connection: Optional = None
):
    """Copy a local file to a remote host"""
    if ssh_connection is None:
        raise ValueError('SSH connection cannot be None')

    with SCPClient(ssh_connection.get_transport()) as scp:
        scp.put(filepath, remote_dir)