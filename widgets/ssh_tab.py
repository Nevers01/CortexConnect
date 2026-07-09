from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit
from PyQt6.QtGui import QTextCursor
from PyQt6.QtCore import Qt
from widgets.terminal.ansi_parser import ansi_to_html

from services.ssh.session import SSHSession


class SSHTab(QWidget):
    def __init__(self, server):
        super().__init__()
        self.server = server
        self.session = SSHSession(server)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("""
            QTextEdit {
                background-color: #050505;
                color: #d0d7de;
                font-family: Consolas, Monospace;
                font-size: 13px;
                border: none;
                padding: 10px;
            }
        """)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Komut yaz ve Enter'a bas...")
        self.input.setStyleSheet("""
            QLineEdit {
                background-color: #0d1117;
                color: white;
                border: 1px solid #30363d;
                padding: 10px;
                font-family: Consolas, Monospace;
            }
        """)

        layout.addWidget(self.output, 1)
        layout.addWidget(self.input)

        self.setLayout(layout)

        self.input.returnPressed.connect(self.send_command)

        self.session.output_received.connect(self.append_output)
        self.session.error_received.connect(self.append_error)
        self.session.connected.connect(self.on_connected)
        self.session.disconnected.connect(self.on_disconnected)

        self.append_output(f"{server.name} SSH bağlantısı başlatılıyor...\n")
        self.session.connect()

    def send_command(self):
        command = self.input.text().strip()

        if not command:
            return

        self.append_output(f"\n$ {command}\n")
        self.session.send(command)
        self.input.clear()

    def append_output(self, text):
        html_text = ansi_to_html(text)

        self.output.moveCursor(QTextCursor.MoveOperation.End)
        self.output.insertHtml(html_text)
        self.output.moveCursor(QTextCursor.MoveOperation.End)

    def append_error(self, text):
        self.append_output(f"\n[HATA] {text}\n")

    def on_connected(self):
        self.append_output("SSH bağlantısı başarılı.\n\n")

    def on_disconnected(self):
        self.append_output("\nSSH bağlantısı kapandı.\n")

    def close_terminal(self):
        self.session.disconnect()