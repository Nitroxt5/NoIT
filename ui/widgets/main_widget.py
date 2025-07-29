from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout

from ui.widgets.file_loader import CsvDropZone
from ui.widgets.pipeline import Pipeline


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NoIT")
        self.setFixedSize(2000, 1500)
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(CsvDropZone(self.open_pipeline))
        self.pipeline = None

        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)

    def open_pipeline(self, data, data_name: str):
        self.pipeline = Pipeline(data, data_name)
        self.stacked_widget.addWidget(self.pipeline)
        self.stacked_widget.setCurrentWidget(self.pipeline)
