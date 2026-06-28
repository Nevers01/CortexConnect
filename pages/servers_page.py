from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QMessageBox
from PyQt6.QtCore import Qt

import services.DataBase as DataBase
from widgets.server_card import ServerCard
from dialogs.server_dialog import ServerDialog
from services.connection import open_connection
from services.status import ping_host


class ServersPage(QWidget):
    def __init__(self, on_open_ssh_tab=None, on_open_rdp_tab=None):
        super().__init__()
        self.on_open_ssh_tab = on_open_ssh_tab
        self.on_open_rdp_tab = on_open_rdp_tab
        self.build_ui()
        self.load_servers()

    def build_ui(self):
        wrapper = QVBoxLayout()
        wrapper.setContentsMargins(26, 26, 26, 26)

        header = QLabel("Sunucular")
        header.setObjectName("Title")

        desc = QLabel("SSH, RDP ve VNC bağlantılarını tek ekrandan yönet.")
        desc.setObjectName("SubTitle")

        self.server_layout = QVBoxLayout()
        self.server_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.server_layout.setSpacing(14)

        scroll_content = QWidget()
        scroll_content.setLayout(self.server_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_content)

        wrapper.addWidget(header)
        wrapper.addWidget(desc)
        wrapper.addSpacing(16)
        wrapper.addWidget(scroll)

        self.setLayout(wrapper)

    def load_servers(self):
        while self.server_layout.count():
            item = self.server_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        servers = DataBase.get_servers()

        if not servers:
            empty = QLabel("Henüz sunucu yok. Sol taraftan Sunucu Ekle.")
            empty.setObjectName("SubTitle")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.server_layout.addWidget(empty)
            return

        for server in servers:
            online = ping_host(server.host)
            card = ServerCard(
                server=server,
                is_online=online,
                on_connect=self.connect_server,
                on_edit=self.edit_server,
                on_delete=self.remove_server
            )
            self.server_layout.addWidget(card)

    def add_server(self):
        dialog = ServerDialog(self)

        if dialog.exec():
            data = dialog.get_data()
            DataBase.add_server(
                data["name"],
                data["type"],
                data["host"],
                data["port"],
                data["username"],
                data["password"],
                data["notes"],
            )
            self.load_servers()

    def edit_server(self, server):
        dialog = ServerDialog(self, server)

        if dialog.exec():
            data = dialog.get_data()
            DataBase.update_server(
                server.id,
                data["name"],
                data["type"],
                data["host"],
                data["port"],
                data["username"],
                data["password"],
                data["notes"],
            )
            self.load_servers()

    def remove_server(self, server_id, name):
        answer = QMessageBox.question(self, "Silinsin mi?", f"{name} silinsin mi?")

        if answer == QMessageBox.StandardButton.Yes:
            DataBase.delete_server(server_id)
            self.load_servers()

    def connect_server(self, server):
        try:
            if server.type == "SSH":
                if self.on_open_ssh_tab:
                    self.on_open_ssh_tab(server)
                return

            if server.type == "RDP":
                if self.on_open_rdp_tab:
                    self.on_open_rdp_tab(server)
                return

            open_connection(server)

        except Exception as e:
            QMessageBox.critical(self, "Bağlantı Hatası", str(e))