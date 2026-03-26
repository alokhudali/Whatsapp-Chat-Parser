from PyQt6.QtCore import QThread, pyqtSignal
from components.parser import parse_chat


class ParserThread(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            messages = parse_chat(self.file_path)
            self.finished.emit(messages)
        except Exception as e:
            self.error.emit(str(e))