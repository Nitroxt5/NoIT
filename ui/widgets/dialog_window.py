from PyQt5.QtCore import Qt, QTimer, QSequentialAnimationGroup, QRect, QPropertyAnimation, QEasingCurve, QPoint, QSize
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QSizePolicy, QWidget, QHBoxLayout

from ui.styles import scroll_bar_style, button_style, combo_box_style, dialog_background_style


class AnimatedDialog(QWidget):
    def __init__(self, buttons: list, parent=None, text='', size=QSize(400, 300), pos=QPoint(0, 0), mode='horizontal'):
        super().__init__(parent)
        self.mode = mode
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet(dialog_background_style)
        self.initial_pos = pos
        self.start_size = QSize(20, 20)
        self.max_size = size
        self.text = text
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.label.setStyleSheet('color: white; font-size: 25px;')
        self.layout = QVBoxLayout(self)
        self.typing_index = 0
        self.typing_timer = QTimer()
        self.sequence = QSequentialAnimationGroup()
        if self.mode == 'vertical':
            self.button_box = QVBoxLayout(self)
        else:
            self.button_box = QHBoxLayout(self)
        if self.mode == 'dropdown':
            buttons[0].setMaxVisibleItems(8)
        for btn in buttons:
            if mode == 'dropdown':
                btn.setStyleSheet(combo_box_style + scroll_bar_style)
            else:
                btn.setStyleSheet(button_style)
            self.button_box.addWidget(btn)
        self.button_box.setEnabled(False)
        self.label.setText('')

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor(255, 255, 255, 70))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -2, -2), 12, 12)

    def show_animated(self, scroll_bar):
        start_w, start_h = self.start_size.width(), self.start_size.height()
        mid_h = self.max_size.height()
        final_w = self.max_size.width()
        x = self.initial_pos.x()
        y = self.initial_pos.y()

        start_rect = QRect(x, y, start_w, start_h)
        mid_rect = QRect(x, y - (mid_h - start_h), start_w, mid_h)
        final_rect = QRect(x, y - (mid_h - start_h), final_w, mid_h)

        self.setGeometry(start_rect)
        self.show()

        anim_up = QPropertyAnimation(self, b'geometry')
        anim_up.setDuration(400)
        anim_up.setStartValue(start_rect)
        anim_up.setEndValue(mid_rect)
        anim_up.setEasingCurve(QEasingCurve.InOutQuad)

        anim_right = QPropertyAnimation(self, b'geometry')
        anim_right.setDuration(400)
        anim_right.setStartValue(mid_rect)
        anim_right.setEndValue(final_rect)
        anim_right.setEasingCurve(QEasingCurve.InOutQuad)

        self.sequence.addAnimation(anim_up)
        self.sequence.addAnimation(anim_right)
        self.sequence.finished.connect(lambda: self.create_contents(scroll_bar))
        self.sequence.start()

    def start_typing_effect(self):
        self.label.setText('')

        def type_next():
            if self.typing_index >= len(self.text):
                self.typing_timer.stop()
                return
            self.typing_index += 1
            self.label.setText(self.text[:self.typing_index])

        self.typing_timer.timeout.connect(type_next)
        self.typing_timer.start(30)

    def create_contents(self, scroll_bar):
        self.setFixedWidth(self.max_size.width())
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.button_box)
        self.start_typing_effect()
        self.button_box.setEnabled(True)
        scroll_bar.setEnabled(True)
