from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QTextEdit,
    QPushButton,
    QMessageBox,
)


class ServerDialog(QDialog):
    def __init__(self, parent=None, server=None):
        super().__init__(parent)
        self.server = server
        self.setWindowTitle("Sunucu Ekle" if server is None else "Sunucu Düzenle")
        self.setFixedWidth(420)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.name = QLineEdit()
        self.type = QComboBox()
        self.type.addItems(["SSH", "RDP", "VNC"])
        self.host = QLineEdit()
        self.port = QLineEdit()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.notes = QTextEdit()
        self.notes.setFixedHeight(70)

        form.addRow("Sunucu Adı", self.name)
        form.addRow("Tip", self.type)
        form.addRow("Host / IP", self.host)
        form.addRow("Port", self.port)
        form.addRow("Username", self.username)
        form.addRow("Password", self.password)
        form.addRow("Not", self.notes)

        self.type.currentTextChanged.connect(self.set_default_port)

        save_btn = QPushButton("Kaydet")
        save_btn.clicked.connect(self.accept_data)

        layout.addLayout(form)
        layout.addWidget(save_btn)
        self.setLayout(layout)

        if server:
            self.load_server(server)
        else:
            self.set_default_port("SSH")

    def set_default_port(self, value):
        if value == "SSH":
            self.port.setText("22")
        elif value == "RDP":
            self.port.setText("3389")
        elif value == "VNC":
            self.port.setText("5900")

    def load_server(self, server):
        self.name.setText(server.name)
        self.type.setCurrentText(server.type)
        self.host.setText(server.host)
        self.port.setText(str(server.port))
        self.username.setText(server.username)
        self.password.setText(server.password or "")
        self.notes.setText(server.notes or "")

    def get_data(self):
        return {
            "name": self.name.text().strip(),
            "type": self.type.currentText(),
            "host": self.host.text().strip(),
            "port": int(self.port.text().strip()),
            "username": self.username.text().strip(),
            "password": self.password.text(),
            "notes": self.notes.toPlainText().strip(),
        }

    def accept_data(self):
        if not self.name.text().strip():
            QMessageBox.warning(self, "Eksik Bilgi", "Sunucu adı boş olamaz.")
            return

        if not self.host.text().strip():
            QMessageBox.warning(self, "Eksik Bilgi", "Host/IP boş olamaz.")
            return

        if not self.username.text().strip():
            QMessageBox.warning(self, "Eksik Bilgi", "Username boş olamaz.")
            return

        try:
            int(self.port.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Hatalı Port", "Port sayı olmalı.")
            return

        self.accept()
