import platform
import subprocess


def open_connection(server):
    server_id, name, server_type, host, port, username, password, notes = server

    system = platform.system().lower()

    if server_type == "SSH":
        cmd = [
            "ssh",
            "-o", "ServerAliveInterval=30",
            "-o", "ServerAliveCountMax=120",
            "-p", str(port),
            f"{username}@{host}"
        ]

        if "windows" in system:
            subprocess.Popen(["powershell", "-NoExit", "-Command", " ".join(cmd)])
        else:
            subprocess.Popen(["xterm", "-T", name, "-e", " ".join(cmd)])

    elif server_type == "RDP":
        if "windows" in system:
            rdp_file = f"{name}.rdp"
            with open(rdp_file, "w", encoding="utf-8") as f:
                f.write(f"full address:s:{host}:{port}\n")
                f.write(f"username:s:{username}\n")
                f.write("prompt for credentials:i:1\n")
                f.write("screen mode id:i:2\n")
            subprocess.Popen(["mstsc", rdp_file])
        else:
            subprocess.Popen([
                "xfreerdp",
                f"/v:{host}:{port}",
                f"/u:{username}",
                f"/p:{password}",
                "/dynamic-resolution",
                "/cert:ignore"
            ])

    elif server_type == "VNC":
        if "windows" in system:
            raise RuntimeError("Windows tarafında VNC için viewer ayrıca kurulmalı.")
        else:
            subprocess.Popen([
                "vncviewer",
                f"{host}:{port}"
            ])