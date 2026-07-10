import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from PyQt6.QtCore import Qt

import services.db as DataBase
from pages.servers_page import ServersPage
from widgets.ssh_tab import SSHTab
from widgets.rdp_tab import RdpTab
from styles.app_style import APP_STYLE


class CortexConnect(QWidget):
    def __init__(self):
        super().__init__()
        DataBase.init_db()

        self.setWindowTitle("Cortex Connect")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
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

        layout.addWidget(self.tabs, 1)
        self.setLayout(layout)

    def open_ssh_tab(self, server):
        tab = SSHTab(server)
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
    window.showFullScreen()
    sys.exit(app.exec())