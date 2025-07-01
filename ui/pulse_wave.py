from PyQt5.QtCore import QObject, Qt, QTimer
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsEllipseItem


class PulseWave(QObject):
    def __init__(self, scene, center, color=QColor(0, 255, 255), base_radius=30):
        super().__init__()
        self.scene = scene
        self.center = center
        self.base_radius = base_radius
        self.radius = base_radius
        self.max_radius = 100

        self.ellipse = QGraphicsEllipseItem()
        self.ellipse.setBrush(QBrush(Qt.NoBrush))
        self.pen_color = color
        self.pen_color.setAlpha(180)
        self.ellipse.setPen(QPen(self.pen_color, 2))
        self.ellipse.setZValue(-2)
        self.scene.addItem(self.ellipse)

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def animate(self):
        if self.radius > self.max_radius:
            self.radius = self.base_radius
        alpha = int(200 * (1 - self.radius / self.max_radius))
        self.ellipse.setRect(self.center.x() - self.radius, self.center.y() - self.radius,
                             2 * self.radius, 2 * self.radius)
        self.ellipse.setPen(QColor(self.pen_color.red(), self.pen_color.green(), self.pen_color.blue(), alpha))
        self.radius += 2

    def remove_from_scene(self):
        self.timer.stop()
        self.scene.removeItem(self.ellipse)