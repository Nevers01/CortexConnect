import paramiko

from PyQt6.QtCore import QObject, pyqtSignal, QThread


class SSHReader(QThread):
    output_received = pyqtSignal(str)
    error_received = pyqtSignal(str)
    disconnected = pyqtSignal()

    def __init__(self, channel):
        super().__init__()
        self.channel = channel
        self.running = True

    def run(self):
        try:
            while self.running:
                if self.channel.recv_ready():
                    data = self.channel.recv(4096)
                    text = data.decode("utf-8", errors="ignore")
                    self.output_received.emit(text)

                self.msleep(30)

        except Exception as e:
            self.error_received.emit(str(e))

        finally:
            self.disconnected.emit()

    def stop(self):
        self.running = False
        self.quit()
        self.wait(1000)


class SSHSession(QObject):
    output_received = pyqtSignal(str)
    error_received = pyqtSignal(str)
    connected = pyqtSignal()
    disconnected = pyqtSignal()

    def __init__(self, server):
        super().__init__()
        self.server = server
        self.client = None
        self.channel = None
        self.reader = None

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            self.client.connect(
                hostname=self.server.host,
                port=int(self.server.port),
                username=self.server.username,
                password=self.server.password,
                look_for_keys=False,
                allow_agent=False,
                timeout=10,
            )

            self.channel = self.client.invoke_shell()
            self.channel.settimeout(0.0)

            self.reader = SSHReader(self.channel)
            self.reader.output_received.connect(self.output_received.emit)
            self.reader.error_received.connect(self.error_received.emit)
            self.reader.disconnected.connect(self.disconnected.emit)
            self.reader.start()

            self.connected.emit()

        except Exception as e:
            self.error_received.emit(str(e))

    def send(self, command):
        try:
            if self.channel:
                self.channel.send(command + "\n")
        except Exception as e:
            self.error_received.emit(str(e))

    def disconnect(self):
        try:
            if self.reader:
                self.reader.stop()

            if self.channel:
                self.channel.close()

            if self.client:
                self.client.close()

            self.disconnected.emit()

        except Exception as e:
            self.error_received.emit(str(e))