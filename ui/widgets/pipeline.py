from PyQt5.QtCore import QRectF, QPoint, QTimer, Qt, QPropertyAnimation
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem,
                             QGraphicsDropShadowEffect)

from ui.ui_objects.pulse_wave import PulseWave
from ui.ui_objects.flow_line import FlowLine
from ui.styles import scroll_bar_style
from eda.eda_handlers import EDA
from alg.testing_handlers import Tester
from alg.report_maker import Reporter


class Pipeline(QWidget):
    def __init__(self, data, data_name: str):
        super().__init__()
        layout = QVBoxLayout(self)
        self.scene_width = 1919
        self.scene = QGraphicsScene(0, 0, self.scene_width, 1300)
        self.scene.setBackgroundBrush(QColor(22, 22, 35))
        self.view = QGraphicsView(self.scene)
        self.view.setSceneRect(self.scene.sceneRect())
        self.view.setStyleSheet(scroll_bar_style)
        self.view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(self.view, alignment=Qt.AlignLeft)

        self.data_name = data_name
        self.eda = EDA(data, self)
        self.tester = Tester(self)
        self.reporter = Reporter(self)
        self.actions = (self.eda.handle_unimportant, self.eda.handle_duplicates, self.eda.handle_nulls,
                        self.eda.split_to_data_and_target, self.eda.handle_encoding, self.tester.get_algs,
                        self.tester.perform_testing, self.reporter.create_report)
        self.current_action = 0
        self.node_radius = 30
        self.node_start_x = 200
        self.node_step = 500
        self.steps = []
        self.flow = FlowLine(self.scene)
        self.pulse_wave = None
        self.current = -1
        self.activated_first = False
        self.fade_step = 0
        self.fade_timer = QTimer()
        self.flow_line_timer = QTimer()
        self.scroll_animation = None

        for i in range(2 * len(data.columns) + 4):
            node = self.create_node(self.node_start_x + i * self.node_step, self.scene.height() // 2)
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

    def expand_scene(self):
        item_rect = self.steps[self.current].sceneBoundingRect()
        current_rect = self.scene.sceneRect()
        if item_rect.right() > current_rect.right() / 2:
            current_rect.setWidth(current_rect.width() + self.node_step)
            self.scene.setSceneRect(current_rect)
            self.view.setSceneRect(current_rect)
            self.animate_scroll_to(self.view.horizontalScrollBar().maximum() -
                                   (current_rect.right() - item_rect.right() - self.scene_width // 2))

    def animate_scroll_to(self, value):
        scrollbar = self.view.horizontalScrollBar()
        self.scroll_animation = QPropertyAnimation(scrollbar, b"value")
        self.scroll_animation.setDuration(300)
        self.scroll_animation.setStartValue(scrollbar.value())
        self.scroll_animation.setEndValue(value)
        self.scroll_animation.start()

    def set_node_active(self, node):
        color = QColor(160, 255, 245, 60)
        node.setBrush(QBrush(color))
        node.setPen(QPen(QColor(255, 255, 255, 140), 2))
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(50)
        glow.setOffset(0, 0)
        glow.setColor(QColor(0, 255, 255, 140))
        node.setGraphicsEffect(glow)

        p1 = self.steps[self.current].sceneBoundingRect().center()
        p1.setX(p1.x() + self.node_radius)
        p2 = self.steps[self.current + 1].sceneBoundingRect().center()
        p2.setX(p2.x() - self.node_radius)
        self.flow = FlowLine(self.scene, p1, p2, pen_style=Qt.DashLine)
        self.flow_line_timer = QTimer()
        self.flow_line_timer.timeout.connect(self.flow.animate)
        self.flow_line_timer.start(1100)
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
        self.view.horizontalScrollBar().setEnabled(False)
        self.eda.dialog.close()
        self.tester.alg_chooser.close()
        self.flow_line_timer.stop()
        self.flow.remove_from_scene()

        if not self.activated_first:
            entry = QPoint(0, self.steps[0].sceneBoundingRect().center().y())
            target = self.steps[0].sceneBoundingRect().center()
            target.setX(target.x() - self.node_radius)
            self.current += 1
            self.flow = FlowLine(self.scene, entry, target, on_finished=self.activate)
            self.flow.animate()
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
            self.flow = FlowLine(self.scene, p1, p2, on_finished=self.activate)
            self.flow.animate()

        self.expand_scene()

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
