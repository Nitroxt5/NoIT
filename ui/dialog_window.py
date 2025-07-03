from PyQt5.QtCore import Qt, QTimer, QSequentialAnimationGroup, QRect, QPropertyAnimation, QEasingCurve, QPoint, QSize
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QDialogButtonBox


class AnimatedDialog(QDialog):
    def __init__(self, parent=None, text='', size=QSize(400, 200), pos=QPoint(0, 0)):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet("""
            background-color: rgba(20, 40, 80, 160);
            border: 1px solid rgba(255, 255, 255, 70);
            border-radius: 12px;
        """)
        if parent:
            self.initial_pos = QPoint(parent.pos().x() + pos.x(), parent.pos().y() + pos.y())
        else:
            self.initial_pos = pos
        self.start_size = QSize(20, 20)
        self.max_size = size
        self.text = text
        self.label = QLabel()
        self.label.setWordWrap(True)
        self.label.setStyleSheet('color: white;')
        self.typing_index = 0
        self.typing_timer = QTimer()
        self.sequence = QSequentialAnimationGroup()
        self.button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        self.button_box.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgba(20, 40, 80, 100);
                border: 1px solid rgba(255, 255, 255, 60);
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: rgba(100, 140, 200, 180);
            }
        """)
        self.button_box.setEnabled(False)
        self.button_box.button(QDialogButtonBox.Yes).setFixedSize(60, 40)
        self.button_box.button(QDialogButtonBox.No).setFixedSize(60, 40)
        self.button_box.button(QDialogButtonBox.Yes).setStyleSheet('color: white;')
        self.button_box.button(QDialogButtonBox.No).setStyleSheet('color: white;')

    def show_animated(self):
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
        self.sequence.finished.connect(self.create_contents)
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

    def create_contents(self):
        self.setFixedWidth(self.max_size.width())
        layout_v = QVBoxLayout(self)
        layout_v.addWidget(self.label)
        layout_v.addWidget(self.button_box)
        self.start_typing_effect()
        self.button_box.setEnabled(True)
