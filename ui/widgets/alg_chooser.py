from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QComboBox, QTableWidgetItem, QHeaderView

from ui.styles import scroll_bar_style, table_style, combo_box_style, dialog_button_style
from ui.widgets.animated_window import AnimatedWindow
from ui.ui_objects.draggable_table import DraggableTable
from alg.algs_list import algs


class AlgChooser(AnimatedWindow):
    def __init__(self, buttons: list, parent=None, size=QSize(1600, 1200), pos=QPoint(0, 0)):
        super().__init__(buttons, parent, 'Choose algorithms to test:', size, pos)
        self.possible_algs = {alg: 0 for alg in algs.keys()}

        self.label = QLabel()
        self.label.setMaximumHeight(self.label.sizeHint().height() + 20)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('color: white; font-size: 30px;')

        self.dropdown = QComboBox()
        self.dropdown.setMaxVisibleItems(8)
        self.dropdown.setStyleSheet(combo_box_style + scroll_bar_style)
        self.dropdown.addItems(self.possible_algs.keys())
        self.dropdown.activated.connect(self._add_alg)

        self.table = DraggableTable()
        self.table.horizontalHeader().setVisible(False)
        self.table.setStyleSheet(table_style + scroll_bar_style)
        self.table.setColumnCount(2)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

    def _add_alg(self):
        item = QTableWidgetItem(self.dropdown.currentText() + str(self.possible_algs[self.dropdown.currentText()]))
        self.possible_algs[self.dropdown.currentText()] += 1
        self.table.insert_row(self.algs_count)
        self.table.setItem(self.algs_count - 1, 0, item)

    def _create_contents(self, scroll_bar):
        self.setFixedWidth(self.max_size.width())
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.dropdown)
        self.layout.addWidget(self.table)
        btn_layout = QHBoxLayout()
        for btn in self.buttons:
            btn_layout.addWidget(btn)
            btn.setStyleSheet(dialog_button_style)
        self.layout.addLayout(btn_layout)
        self._start_typing_effect()
        scroll_bar.setEnabled(True)

    @property
    def algs_count(self):
        return self.table.rowCount()
