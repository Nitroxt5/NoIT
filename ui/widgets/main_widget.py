from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout

from ui.widgets.file_loader import CsvDropZone
from ui.widgets.pipeline import Pipeline


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('NoIT')
        self.showMaximized()
        self.stacked_widget = QStackedWidget(self)
        self.file_loader = CsvDropZone(self._open_pipeline)
        self.stacked_widget.addWidget(self.file_loader)
        self.pipeline = None

        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)

    def _open_pipeline(self, data, data_name: str):
        self.pipeline = Pipeline(self, data, data_name)
        self.stacked_widget.addWidget(self.pipeline)
        self.stacked_widget.setCurrentWidget(self.pipeline)

    def open_file_loader(self):
        self.stacked_widget.setCurrentWidget(self.file_loader)
