from PyQt5.QtCore import Qt, QPoint, QSize, QRect
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget


class StaticInfo(QWidget):
    def __init__(self, parent=None, text='', answer='', size=QSize(400, 200), pos=QPoint(0, 0)):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet("""
            background-color: rgba(20, 40, 80, 160);
            border: 1px solid rgba(255, 255, 255, 70);
            border-radius: 12px;
        """)
        self.pos = pos
        self.size = size
        self.text = text
        self.answer = answer
        self.text_label = QLabel(self.text)
        self.text_label.setStyleSheet('color: white; font-size: 25px;')
        self.ans_label = QLabel(self.answer)
        self.ans_label.setStyleSheet('color: white; font-size: 25px;')
        self.ans_label.setAlignment(Qt.AlignCenter)
        self.ans_label.setMaximumHeight(self.ans_label.sizeHint().height() + 4)
        self.layout = QVBoxLayout(self)
        self.setGeometry(QRect(self.pos, self.size))
        self.create_contents()
        self.show()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(QColor(255, 255, 255, 70))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -2, -2), 12, 12)

    def create_contents(self):
        self.setFixedWidth(self.size.width())
        self.text_label.setWordWrap(True)
        self.ans_label.setWordWrap(True)
        self.layout.addWidget(self.text_label)
        self.layout.addWidget(self.ans_label)
