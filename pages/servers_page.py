from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QMessageBox
from PyQt6.QtCore import Qt

import services.DataBase as DataBase
from widgets.server_card import ServerCard
from dialogs.server_dialog import ServerDialog
from services.connection import open_connection
from services.status import ping_host
from PyQt6.QtWidgets import QTabWidget
from widgets.ssh_terminal_tab import SshTerminalTab


class ServersPage(QWidget):
    def __init__(self):
        super().__init__()
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
        self.terminal_tabs = QTabWidget()
        self.terminal_tabs.setTabsClosable(True)
        self.terminal_tabs.tabCloseRequested.connect(self.close_terminal_tab)
        self.terminal_tabs.setMinimumHeight(260)

        wrapper.addWidget(self.terminal_tabs)

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
                tab = SshTerminalTab(server)
                index = self.terminal_tabs.addTab(tab, server.name)
                self.terminal_tabs.setCurrentIndex(index)
            else:
                open_connection(server)
        except Exception as e:
            QMessageBox.critical(self, "Bağlantı Hatası", str(e))

    def close_terminal_tab(self, index):
        widget = self.terminal_tabs.widget(index)

        if hasattr(widget, "close_terminal"):
            widget.close_terminal()

        self.terminal_tabs.removeTab(index)