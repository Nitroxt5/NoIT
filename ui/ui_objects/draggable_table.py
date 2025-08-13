from PyQt5.QtWidgets import QTableWidget, QPushButton, QWidget, QTableWidgetItem
from PyQt5.QtCore import Qt, QMimeData, QByteArray
from PyQt5.QtGui import QDrag

from ui.styles import delete_button_style


class DraggableTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setDragDropMode(QTableWidget.InternalMove)
        self.verticalScrollBar().valueChanged.connect(self._update_widget_positions)

    def insert_row(self, row):
        self.insertRow(row)
        self._update_buttons()

    def remove_row(self, row):
        self.removeRow(row)
        self._update_buttons()

    def _update_widget_positions(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                widget = self.cellWidget(row, col)
                if widget:
                    rect = self.visualItemRect(self.item(row, col))
                    widget.setGeometry(rect)

    def _update_button(self, r):
        btn = QPushButton('✖')
        btn.setStyleSheet(delete_button_style)
        btn.clicked.connect(lambda _, row=r: self.remove_row(row))
        self.setCellWidget(r, self.columnCount() - 1, btn)
        self.setItem(r, self.columnCount() - 1, QTableWidgetItem())

    def _update_buttons(self):
        for r in range(self.rowCount()):
            self._update_button(r)

    def startDrag(self, supported_actions):
        drag = QDrag(self)
        mime_data = QMimeData()
        row = self.currentRow()
        mime_data.setData('application/x-qabstractitemmodeldatalist', QByteArray(str(row).encode()))
        drag.setMimeData(mime_data)
        drag.exec_(Qt.MoveAction)

    def dropEvent(self, event):
        source_row = int(event.mimeData().data('application/x-qabstractitemmodeldatalist').data().decode())
        target_row = self.rowAt(event.pos().y())
        if target_row == -1 or source_row == target_row:
            return

        for col in range(self.columnCount() - 1):
            if col == 0:
                source_item = self.takeItem(source_row, col)
                target_item = self.takeItem(target_row, col)
                self.setItem(source_row, col, target_item)
                self.setItem(target_row, col, source_item)
                continue
            if col == 1:
                source_widget = self.cellWidget(source_row, col)
                target_widget = self.cellWidget(target_row, col)
                self.removeCellWidget(source_row, col)
                self.removeCellWidget(target_row, col)
                new_source_widget, new_target_widget = QWidget(), QWidget()
                new_source_widget.setLayout(target_widget.layout())
                new_source_widget.setStyleSheet('border: none; border-radius: 0px')
                new_target_widget.setLayout(source_widget.layout())
                new_target_widget.setStyleSheet('border: none; border-radius: 0px')
                self.setCellWidget(source_row, col, new_source_widget)
                self.setCellWidget(target_row, col, new_target_widget)

        self._update_button(source_row)
        self._update_button(target_row)
        self.resizeRowsToContents()
        event.accept()
