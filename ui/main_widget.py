from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout

from ui.file_loader import CsvDropZone
from ui.pipeline import Pipeline
from ui.dialog_window import AnimatedDialog


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

    def open_pipeline(self, data):
        self.pipeline = Pipeline(data)
        self.stacked_widget.addWidget(self.pipeline)
        self.stacked_widget.setCurrentWidget(self.pipeline)

    def moveEvent(self, event):
        super().moveEvent(event)
        for child in self.findChildren(AnimatedDialog):
            child.move(QPoint(self.pipeline.steps[self.pipeline.current].x(),
                              self.pipeline.steps[self.pipeline.current].y() - self.pipeline.node_radius) +
                       self.pos() - QPoint(0, child.height() - child.start_size.height()))
