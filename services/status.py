import platform
import socket
import subprocess


def ping_host(host):
    try:

        system = platform.system().lower()

        count = "1"

        cmd = ["ping"]

        if system == "windows":
            cmd += ["-n", count]
        else:
            cmd += ["-c", count]

        cmd.append(host)

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3)

        return result.returncode == 0

    except:
        return False


def port_open(host, port):

    try:

        sock = socket.socket()

        sock.settimeout(2)

        result = sock.connect_ex((host, port))

        sock.close()

        return result == 0

    except:

        return False
