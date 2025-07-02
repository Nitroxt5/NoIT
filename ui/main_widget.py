from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout

from ui.file_loader import CsvDropZone
from ui.pipeline import Pipeline


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NoIT")
        self.setFixedSize(2000, 1500)
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.addWidget(CsvDropZone(self.open_pipeline))

        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)

    def open_pipeline(self, data):
        pipeline = Pipeline(data)
        self.stacked_widget.addWidget(pipeline)
        self.stacked_widget.setCurrentWidget(pipeline)
