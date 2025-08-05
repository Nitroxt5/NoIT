from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout

from ui.styles import scroll_bar_style, dialog_button_style, combo_box_style
from ui.widgets.animated_window import AnimatedWindow


class AnimatedDialog(AnimatedWindow):
    def __init__(self, buttons: list, parent=None, text='', size=QSize(400, 300), pos=QPoint(0, 0), mode='horizontal'):
        super().__init__(buttons, parent, text, size, pos)
        self.mode = mode
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
                btn.setStyleSheet(dialog_button_style)
            self.button_box.addWidget(btn)
        self.button_box.setEnabled(False)

    def _create_contents(self, scroll_bar):
        super()._create_contents(scroll_bar)
        self.layout.addLayout(self.button_box)
        self.button_box.setEnabled(True)
