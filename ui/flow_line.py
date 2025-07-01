from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPen, QColor


class FlowLine:
    def __init__(self, scene, p1, p2, on_finished=None):
        self.scene = scene
        self.p1 = p1
        self.p2 = p2
        self.on_finished = on_finished
        self.progress = 0.0

        self.line = scene.addLine(0, 0, 0, 0)
        pen = QPen(QColor(255, 255, 255, 40), 3, Qt.SolidLine)
        pen.setCapStyle(Qt.RoundCap)
        self.line.setPen(pen)

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_step)

    def animate(self):
        self.progress = 0.0
        self.timer.start(30)

    def animate_step(self):
        self.progress += 0.03
        if self.progress >= 1.0:
            self.progress = 1.0
            self.timer.stop()
            self.line.setLine(self.p1.x(), self.p1.y(), self.p2.x(), self.p2.y())
            if self.on_finished:
                self.on_finished()
            return

        x = self.p1.x() + (self.p2.x() - self.p1.x()) * self.progress
        y = self.p1.y() + (self.p2.y() - self.p1.y()) * self.progress
        self.line.setLine(self.p1.x(), self.p1.y(), x, y)
