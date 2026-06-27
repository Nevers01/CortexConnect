import platform
import subprocess


def open_connection(server):
    system = platform.system().lower()

    if server.type == "SSH":
        cmd = [
            "ssh",
            "-o",
            "ServerAliveInterval=30",
            "-o",
            "ServerAliveCountMax=120",
            "-p",
            str(server.port),
            f"{server.username}@{server.host}",
        ]

        if "windows" in system:
            subprocess.Popen(["powershell", "-NoExit", "-Command", " ".join(cmd)])
        else:
            subprocess.Popen(["xterm", "-T", server.name, "-e", " ".join(cmd)])

    elif server.type == "RDP":
        if "windows" in system:
            rdp_file = f"{server.name}.rdp"
            with open(rdp_file, "w", encoding="utf-8") as f:
                f.write(f"full address:s:{server.host}:{server.port}\n")
                f.write(f"username:s:{server.username}\n")
                f.write("prompt for credentials:i:1\n")
                f.write("screen mode id:i:2\n")

            subprocess.Popen(["mstsc", rdp_file])
        else:
            subprocess.Popen(
                [
                    "xfreerdp",
                    f"/v:{server.host}:{server.port}",
                    f"/u:{server.username}",
                    f"/p:{server.password}",
                    "/dynamic-resolution",
                    "/cert:ignore",
                ]
            )

    elif server.type == "VNC":
        if "windows" in system:
            raise RuntimeError("Windows tarafında VNC için viewer ayrıca kurulmalı.")
        else:
            subprocess.Popen(
                [
                    "vncviewer",
                    f"{server.host}:{server.port}",
                ]
            )
