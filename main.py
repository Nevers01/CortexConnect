import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget

import services.DataBase
from pages.servers_page import ServersPage
from widgets.ssh_terminal_tab import SshTerminalTab
from widgets.rdp_tab import RdpTab
from styles import APP_STYLE


class CortexConnect(QWidget):
    def __init__(self):
        super().__init__()
        services.DataBase.init_db()

        self.setWindowTitle("Cortex Connect")
        self.resize(1100, 680)
        self.setMinimumSize(900, 560)
        self.setStyleSheet(APP_STYLE)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)

        self.servers_page = ServersPage(
            on_open_ssh_tab=self.open_ssh_tab,
            on_open_rdp_tab=self.open_rdp_tab
        )

        self.tabs.addTab(self.servers_page, "Sunucular")
        self.tabs.tabBar().setTabButton(
            0,
            self.tabs.tabBar().ButtonPosition.RightSide,
            None
        )

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def open_ssh_tab(self, server):
        tab = SshTerminalTab(server)
        index = self.tabs.addTab(tab, server.name)
        self.tabs.setCurrentIndex(index)

    def open_rdp_tab(self, server):
        tab = RdpTab(server)
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