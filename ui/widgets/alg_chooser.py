from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QComboBox, QTableWidgetItem, QHeaderView, QLineEdit, QWidget, \
    QVBoxLayout

from ui.styles import scroll_bar_style, table_style, combo_box_style, dialog_button_style, line_edit_style
from ui.widgets.animated_window import AnimatedWindow
from ui.ui_objects.draggable_table import DraggableTable
from alg.algs_list import algs, hyperparams


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
        self.table.setColumnCount(3)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)

    def _add_alg(self):
        alg_name = self.dropdown.currentText()
        self.table.insert_row(self.algs_count)

        item = QTableWidgetItem(alg_name + str(self.possible_algs[alg_name]))
        self.possible_algs[alg_name] += 1
        self.table.setItem(self.algs_count - 1, 0, item)

        layout = QHBoxLayout()
        for param, values in hyperparams[alg_name].items():
            v_layout = QVBoxLayout()
            label = QLabel(param)
            label.setStyleSheet('color: white; font-size: 25px; border: none; text-align: center; '
                                'background: transparent')
            v_layout.addWidget(label, stretch=1)
            if param == 'criterion' or param == 'kernel':
                dropdown = QComboBox()
                dropdown.setObjectName(param)
                dropdown.setMaxVisibleItems(8)
                dropdown.setStyleSheet(combo_box_style + scroll_bar_style)
                dropdown.addItems(['auto'] + values)
                v_layout.addWidget(dropdown, stretch=1)
            else:
                int_input = QLineEdit()
                int_input.setObjectName(param)
                int_input.setPlaceholderText('auto')
                int_input.setValidator(QIntValidator(min(values['range']), max(values['range'])))
                int_input.setStyleSheet(line_edit_style)
                v_layout.addWidget(int_input)
            layout.addLayout(v_layout, stretch=1)
        proxy = QWidget()
        proxy.setStyleSheet('border: none; border-radius: 0px')
        proxy.setLayout(layout)
        self.table.setCellWidget(self.algs_count - 1, 1, proxy)
        self.table.setItem(self.algs_count - 1, 1, QTableWidgetItem())
        self.table.resizeRowsToContents()

    def _create_contents(self, scroll_bar):
        super()._create_contents(scroll_bar)
        self.layout.addWidget(self.dropdown)
        self.layout.addWidget(self.table)
        btn_layout = QHBoxLayout()
        for btn in self.buttons:
            btn_layout.addWidget(btn)
            btn.setStyleSheet(dialog_button_style)
        self.layout.addLayout(btn_layout)

    @property
    def algs_count(self):
        return self.table.rowCount()
