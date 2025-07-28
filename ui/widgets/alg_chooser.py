from PyQt5.QtCore import Qt, QTimer, QSequentialAnimationGroup, QRect, QPropertyAnimation, QEasingCurve, QPoint, QSize
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import (QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QWidget, QComboBox, QTableWidget,
                             QTableWidgetItem, QHeaderView)

from ui.styles import scroll_bar_style, table_style, combo_box_style, dialog_background_style, button_style
from alg.algs_list import algs


class AlgChooser(QWidget):
    def __init__(self, buttons: list, parent=None, size=QSize(1600, 1200), pos=QPoint(0, 0)):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet(dialog_background_style)
        self.text = 'Choose algorithms to test:'
        self.initial_pos = pos
        self.start_size = QSize(20, 20)
        self.max_size = size
        self.buttons = buttons
        self.possible_algs = {alg: 0 for alg in algs.keys()}

        self.label = QLabel()
        self.label.setWordWrap(True)
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.label.setMaximumHeight(self.label.sizeHint().height() + 20)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('color: white; font-size: 30px;')

        self.dropdown = QComboBox()
        self.dropdown.setMaxVisibleItems(8)
        self.dropdown.setStyleSheet(combo_box_style + scroll_bar_style)
        self.dropdown.addItems(self.possible_algs.keys())
        self.dropdown.activated.connect(self.add_alg)

        self.table = QTableWidget()
        self.table.horizontalHeader().setVisible(False)
        self.table.setStyleSheet(table_style + scroll_bar_style)
        self.table.setColumnCount(1)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        self.layout = QVBoxLayout(self)
        self.typing_index = 0
        self.typing_timer = QTimer()
        self.sequence = QSequentialAnimationGroup()

    def add_alg(self):
        item = QTableWidgetItem(self.dropdown.currentText() + str(self.possible_algs[self.dropdown.currentText()]))
        self.possible_algs[self.dropdown.currentText()] += 1
        self.table.insertRow(self.algs_count)
        self.table.setItem(self.algs_count - 1, 0, item)

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
        self.layout.addWidget(self.dropdown)
        self.layout.addWidget(self.table)
        btn_layout = QHBoxLayout()
        for btn in self.buttons:
            btn_layout.addWidget(btn)
            btn.setStyleSheet(button_style)
        self.layout.addLayout(btn_layout)
        self.start_typing_effect()
        scroll_bar.setEnabled(True)

    @property
    def algs_count(self):
        return self.table.rowCount()
