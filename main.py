import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QTabWidget

import services.DataBase
from pages.servers_page import ServersPage
from widgets.sidebar import Sidebar
from widgets.ssh_terminal_tab import SshTerminalTab
from styles import APP_STYLE


class CortexConnect(QWidget):
    def __init__(self):
        super().__init__()
        services.DataBase.init_db()

        self.setWindowTitle("Cortex Connect")
        self.resize(1100, 680)
        self.setMinimumSize(900, 560)
        self.setStyleSheet(APP_STYLE)

        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.servers_page = ServersPage()
        self.tabs.addTab(self.servers_page, "Sunucular")

        self.sidebar = Sidebar(
            on_add_server=self.servers_page.add_server,
            on_refresh=self.servers_page.load_servers
        )

        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.tabs)

        self.setLayout(self.main_layout)

    def open_ssh_tab(self, server):
        tab = SshTerminalTab(server)
        index = self.tabs.addTab(tab, server.name)
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        if index == 0:
            return

        widget = self.tabs.widget(index)

        if hasattr(widget, "close_terminal"):
            widget.close_terminal()

        self.tabs.removeTab(index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CortexConnect()
    window.show()
    sys.exit(app.exec())