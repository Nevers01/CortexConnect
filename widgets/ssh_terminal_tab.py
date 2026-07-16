import subprocess
import uuid

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class SshTerminalTab(QWidget):
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.process = None
        self.window_id = None
        self.title = f"CORTEX_SSH_{server.name}_{uuid.uuid4().hex[:6]}"

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.placeholder = QLabel(f"{server.name} SSH başlatılıyor...")
        self.placeholder.setStyleSheet("padding: 12px; color: #8b949e; background:#111;")

        layout.addWidget(self.placeholder)
        self.setLayout(layout)

        QTimer.singleShot(500, self.start_terminal)
        self.follow_timer = QTimer(self)
        self.follow_timer.timeout.connect(self.position_terminal)

    def start_terminal(self):
        cmd = (
            f"ssh "
            f"-o ServerAliveInterval=30 "
            f"-o ServerAliveCountMax=120 "
            f"-o TCPKeepAlive=yes "
            f"-p {self.server.port} "
            f"{self.server.username}@{self.server.host}"
        )

        self.process = subprocess.Popen([
            "xterm",
            "-T", self.title,
            "-fa", "Monospace",
            "-fs", "11",
            "-bg", "black",
            "-fg", "white",
            "-e", "bash", "-lc", cmd
        ])

        QTimer.singleShot(800, self.find_terminal_window)

    def find_terminal_window(self):
        result = subprocess.run(
            ["xdotool", "search", "--name", self.title],
            capture_output=True,
            text=True
        )

        ids = result.stdout.strip().splitlines()

        if ids:
            self.window_id = ids[-1]
            self.placeholder.hide()
            self.position_terminal()
            self.follow_timer.start(500)

    def position_terminal(self):
        if not self.window_id:
            return

        pos = self.mapToGlobal(self.rect().topLeft())
        width = self.width()
        height = self.height()

        subprocess.run(["xdotool", "windowmove", self.window_id, str(pos.x()), str(pos.y())])
        subprocess.run(["xdotool", "windowsize", self.window_id, str(width), str(height)])

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.position_terminal()

    def showEvent(self, event):
        super().showEvent(event)
        if self.window_id:
            subprocess.run(["xdotool", "windowmap", self.window_id])
            self.position_terminal()

    def hideEvent(self, event):
        super().hideEvent(event)
        if self.window_id:
            subprocess.run(["xdotool", "windowunmap", self.window_id])

    def close_terminal(self):
        self.follow_timer.stop()

        if self.process and self.process.poll() is None:
            self.process.terminate()