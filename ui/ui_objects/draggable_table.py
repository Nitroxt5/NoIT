from PyQt5.QtWidgets import QTableWidget, QPushButton
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

    def insert_row(self, row):
        self.insertRow(row)
        self._update_buttons()

    def remove_row(self, row):
        self.removeRow(row)
        self._update_buttons()

    def _update_buttons(self):
        for r in range(self.rowCount()):
            btn = QPushButton('✖')
            btn.setStyleSheet(delete_button_style)
            btn.clicked.connect(lambda _, row=r: self.remove_row(row))
            self.setCellWidget(r, self.columnCount() - 1, btn)

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

        for col in range(self.columnCount()):
            source_item = self.takeItem(source_row, col)
            target_item = self.takeItem(target_row, col)
            self.setItem(source_row, col, target_item)
            self.setItem(target_row, col, source_item)

        event.accept()
