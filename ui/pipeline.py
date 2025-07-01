from PyQt5.QtCore import QRectF, QPointF, QTimer
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QPushButton, QGraphicsEllipseItem,
                             QGraphicsDropShadowEffect)

from ui.pulse_wave import PulseWave
from ui.flow_line import FlowLine


class Pipeline(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NoIT")
        self.setFixedSize(740, 320)

        layout = QVBoxLayout(self)
        self.scene = QGraphicsScene(0, 0, 740, 280)
        self.scene.setBackgroundBrush(QColor(22, 22, 35))
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.node_radius = 30
        layout.addWidget(self.view)

        self.steps = []
        self.flows = []
        self.pulse_wave = None
        self.current = -1
        self.activated_first = False
        self.fade_step = 0
        self.fade_timer = QTimer()

        for i in range(5):
            node = self.create_node(100 + i * 110, 110)
            self.scene.addItem(node)
            self.steps.append(node)
            node.setVisible(False)

        self.next_btn = QPushButton("Next step")
        self.next_btn.clicked.connect(self.next_step)
        layout.addWidget(self.next_btn)

        self.fade_in_node(self.steps[0], lambda: None)
        self.next_step()

    def create_node(self, x, y):
        node = QGraphicsEllipseItem(QRectF(0, 0, self.node_radius * 2, self.node_radius * 2))
        node.setBrush(QBrush(QColor(255, 255, 255, 30)))
        node.setPen(QPen(QColor(255, 255, 255, 80), 1.5))
        node.setPos(x, y)
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

        center = node.sceneBoundingRect().center()
        self.pulse_wave = PulseWave(self.scene, center)

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
        self.next_btn.setEnabled(False)

        def activate():
            self.set_node_active(self.steps[self.current])
            self.activated_first = True
            try:
                self.fade_in_node(self.steps[self.current + 1], lambda: self.next_btn.setEnabled(True))
            except IndexError:
                self.next_btn.setEnabled(True)

        if not self.activated_first:
            entry = QPointF(-80, self.steps[0].sceneBoundingRect().center().y())
            target = self.steps[0].sceneBoundingRect().center()
            target.setX(target.x() - self.node_radius)
            self.current += 1
            flow = FlowLine(self.scene, entry, target, on_finished=activate)
            flow.animate()
            self.flows.append(flow)
            return

        if self.current >= 0:
            self.set_node_complete(self.steps[self.current])

        self.current += 1
        if self.current >= len(self.steps):
            self.next_btn.setEnabled(False)
            return

        if self.current > 0:
            p1 = self.steps[self.current - 1].sceneBoundingRect().center()
            p1.setX(p1.x() + self.node_radius)
            p2 = self.steps[self.current].sceneBoundingRect().center()
            p2.setX(p2.x() - self.node_radius)
            flow = FlowLine(self.scene, p1, p2, on_finished=activate)
            flow.animate()
            self.flows.append(flow)

    def fade_in_node(self, node, on_finished):
        steps = 20
        self.fade_step = 0

        def fade():
            t = self.fade_step / steps
            node.setOpacity(t)
            self.fade_step += 3
            if self.fade_step >= steps:
                self.fade_timer.stop()
                on_finished()

        node.setVisible(True)
        node.setOpacity(0)
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(fade)
        self.fade_timer.start(30)
