from PyQt5.QtCore import Qt, QTimer, QSequentialAnimationGroup, QRect, QPropertyAnimation, QEasingCurve, QPoint, QSize
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout


class AnimatedDialog(QDialog):
    def __init__(self, parent=None, text="", size=QSize(400, 200), pos=QPoint(0, 0)):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet("""
            background-color: rgba(0, 0, 0, 200);
            color: white;
            border: 2px solid cyan;
            border-radius: 8px;
        """)
        if parent:
            self.initial_pos = QPoint(parent.pos().x() + pos.x(), parent.pos().y() + pos.y())
        else:
            self.initial_pos = pos
        self.max_size = size
        self.text = text
        self.label = QLabel()
        self.label.setWordWrap(True)
        self.typing_index = 0
        self.typing_timer = QTimer()
        self.exit_btn = QPushButton()
        self.sequence = QSequentialAnimationGroup()

    def show_animated(self):
        start_w, start_h = 20, 20
        mid_h = self.max_size.height()
        final_w = self.max_size.width()
        x = self.initial_pos.x()
        y = self.initial_pos.y()

        start_rect = QRect(x, y, start_w, start_h)
        mid_rect = QRect(x, y - (mid_h - start_h), start_w, mid_h)
        final_rect = QRect(x, y - (mid_h - start_h), final_w, mid_h)

        self.setGeometry(start_rect)
        self.show()

        anim_up = QPropertyAnimation(self, b"geometry")
        anim_up.setDuration(400)
        anim_up.setStartValue(start_rect)
        anim_up.setEndValue(mid_rect)
        anim_up.setEasingCurve(QEasingCurve.InOutQuad)

        anim_right = QPropertyAnimation(self, b"geometry")
        anim_right.setDuration(400)
        anim_right.setStartValue(mid_rect)
        anim_right.setEndValue(final_rect)
        anim_right.setEasingCurve(QEasingCurve.InOutQuad)

        self.sequence.addAnimation(anim_up)
        self.sequence.addAnimation(anim_right)
        self.sequence.finished.connect(self.create_contents)
        self.sequence.start()

    def start_typing_effect(self):
        self.label.setText("")

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
        layout = QVBoxLayout(self)
        self.exit_btn = QPushButton('Exit', self)
        self.exit_btn.clicked.connect(self.close)
        layout.addWidget(self.label)
        layout.addWidget(self.exit_btn)
        self.start_typing_effect()
