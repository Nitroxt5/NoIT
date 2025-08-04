from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtCore import Qt, QMimeData, QByteArray
from PyQt5.QtGui import QDrag


class DraggableTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setDragDropMode(QTableWidget.InternalMove)

    def startDrag(self, supportedActions):
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
