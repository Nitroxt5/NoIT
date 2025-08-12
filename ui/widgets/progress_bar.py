from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtWidgets import QHBoxLayout, QProgressBar

from ui.styles import dialog_button_style, progress_bar_style
from ui.widgets.animated_window import AnimatedWindow


class ProgressBar(AnimatedWindow):
    def __init__(self, buttons: list, parent=None, start_text='', end_text='', size=QSize(400, 300), pos=QPoint(0, 0),
                 on_success_callback=None):
        super().__init__(buttons, parent, start_text, size, pos)
        self.end_text = end_text
        self.on_success_callback = on_success_callback
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 100)
        self.progress.setVisible(False)
        self.progress.setStyleSheet(progress_bar_style)

    def check_completion(self, value, text):
        self.typing_timer.stop()
        self.progress.setValue(value)
        if value != self.progress.maximum():
            self.label.setText(f'{self.text}\n{text}')
            return
        self.progress.setVisible(False)
        self.layout.removeWidget(self.progress)
        self.typing_timer.stop()
        self.label.setText(self.end_text)
        h_layout = QHBoxLayout()
        for btn in self.buttons:
            btn.setStyleSheet(dialog_button_style)
            h_layout.addWidget(btn)
        self.layout.addLayout(h_layout)

    def _create_contents(self, scroll_bar):
        super()._create_contents(scroll_bar)
        self.layout.addWidget(self.progress)
        self.progress.setVisible(True)
        if self.on_success_callback:
            self.on_success_callback()
