from PyQt5.QtCore import QRectF, QPoint, QTimer
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem,
                             QGraphicsDropShadowEffect)

from ui.pulse_wave import PulseWave
from ui.flow_line import FlowLine
from eda.eda_handlers import EDA


class Pipeline(QWidget):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle('NoIT')
        self.setFixedSize(2000, 1500)

        layout = QVBoxLayout(self)
        self.scene = QGraphicsScene(0, 0, 2000, 1500)
        self.scene.setBackgroundBrush(QColor(22, 22, 35))
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.node_radius = 30
        layout.addWidget(self.view)

        self.eda = EDA(data, self)
        self.actions = (self.eda.handle_unimportant, self.eda.handle_duplicates, self.eda.handle_nulls)
        self.current_action = 0
        self.node_start_x = 200
        self.node_step = 200
        self.steps = []
        self.flows = []
        self.pulse_wave = None
        self.current = -1
        self.activated_first = False
        self.fade_step = 0
        self.fade_timer = QTimer()

        for i in range(10):
            node = self.create_node(self.node_start_x + i * self.node_step, self.geometry().height() // 2)
            self.scene.addItem(node)
            self.steps.append(node)

        self.fade_in_node(self.steps[0])
        self.next_step()

    def create_node(self, x, y):
        node = QGraphicsEllipseItem(QRectF(0, 0, self.node_radius * 2, self.node_radius * 2))
        node.setBrush(QBrush(QColor(255, 255, 255, 30)))
        node.setPen(QPen(QColor(255, 255, 255, 80), 1.5))
        node.setPos(x, y)
        node.setVisible(False)
        node.setTransformOriginPoint(node.boundingRect().center())

        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(35)
        glow.setOffset(0, 0)
        glow.setColor(QColor(255, 255, 255, 60))
        node.setGraphicsEffect(glow)
        return node

    def set_node_active(self, node):
        color = QColor(160, 255, 245, 60)
        node.setBrush(QBrush(color))
        node.setPen(QPen(QColor(255, 255, 255, 140), 2))
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(50)
        glow.setOffset(0, 0)
        glow.setColor(QColor(0, 255, 255, 140))
        node.setGraphicsEffect(glow)

        self.pulse_wave = PulseWave(self.scene, node.sceneBoundingRect().center())

        try:
            while self.actions[self.current_action]():
                self.current_action += 1
                self.eda.first = True
        except IndexError:
            pass

    def set_node_complete(self, node):
        color = QColor(190, 255, 180, 40)
        node.setBrush(QBrush(color))
        node.setPen(QPen(QColor(255, 255, 255, 90), 1.5))
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(30)
        glow.setOffset(0, 0)
        glow.setColor(QColor(160, 255, 180, 80))
        node.setGraphicsEffect(glow)
        self.pulse_wave.remove_from_scene()

    def next_step(self):
        self.eda.dialog.close()

        if not self.activated_first:
            entry = QPoint(-80, self.steps[0].sceneBoundingRect().center().y())
            target = self.steps[0].sceneBoundingRect().center()
            target.setX(target.x() - self.node_radius)
            self.current += 1
            flow = FlowLine(self.scene, entry, target, on_finished=self.activate)
            flow.animate()
            self.flows.append(flow)
            return

        if self.current >= 0:
            self.set_node_complete(self.steps[self.current])

        self.current += 1
        if self.current >= len(self.steps):
            return

        if self.current > 0:
            p1 = self.steps[self.current - 1].sceneBoundingRect().center()
            p1.setX(p1.x() + self.node_radius)
            p2 = self.steps[self.current].sceneBoundingRect().center()
            p2.setX(p2.x() - self.node_radius)
            flow = FlowLine(self.scene, p1, p2, on_finished=self.activate)
            flow.animate()
            self.flows.append(flow)

    def activate(self):
        self.set_node_active(self.steps[self.current])
        self.activated_first = True
        try:
            self.fade_in_node(self.steps[self.current + 1])
        except IndexError:
            pass

    def fade_in_node(self, node):
        steps = 20
        self.fade_step = 0

        def fade():
            t = self.fade_step / steps
            node.setOpacity(t)
            self.fade_step += 3
            if self.fade_step >= steps:
                self.fade_timer.stop()

        node.setVisible(True)
        node.setOpacity(0)
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(fade)
        self.fade_timer.start(30)
