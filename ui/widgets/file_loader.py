import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QLabel, QPushButton, QWidget, QFileDialog,
    QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontMetrics

from ui.styles import scroll_bar_style, table_style, file_loader_style


class CsvDropZone(QWidget):
    def __init__(self, on_success_callback=None):
        super().__init__()
        self.setAcceptDrops(True)
        self.on_success_callback = on_success_callback
        self.df = pd.DataFrame()

        self.label = QLabel('Drop CSV here or click and choose it')
        self.label.setFont(QFont('Segoe UI', 11))
        self.label.setAlignment(Qt.AlignCenter)

        self.setStyleSheet(file_loader_style + table_style + scroll_bar_style)

        self.table = QTableWidget()
        self.table.setCornerButtonEnabled(False)
        self.table.verticalHeader().setDefaultSectionSize(28)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().sectionClicked.connect(self._draw_distribution)
        self._enable_table(False)
        self.path = ''
        self.continue_btn = QPushButton('Continue')
        self.continue_btn.clicked.connect(self._on_continue)
        self._enable_buttons(False)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.continue_btn)

    def _adapt_table_width(self):
        for col in range(self.table.columnCount()):
            self.table.setColumnWidth(col, 150)
        font_metrics = QFontMetrics(self.table.font())
        for col in range(self.table.columnCount()):
            max_width = font_metrics.width(self.table.horizontalHeaderItem(col).text()) + 20
            for row in range(self.table.rowCount()):
                item = self.table.item(row, col)
                if item:
                    item_width = font_metrics.width(item.text()) + 20
                    max_width = max(max_width, item_width)
                if max_width > self.table.columnWidth(col):
                    self.table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeToContents)
                    break

    def _draw_distribution(self, ind):
        column = self.table.horizontalHeaderItem(ind).text()
        plt.figure(figsize=(12, 12))
        plt.xticks(fontsize=16)
        plt.yticks(fontsize=16)
        sns.histplot(x=column, data=self.df)
        plt.title(column, fontsize=24)
        plt.xlabel(column, fontsize=20)
        plt.ylabel('Count', fontsize=20)
        plt.show()

    def _on_continue(self):
        if self.on_success_callback:
            self.on_success_callback(self.df, self.path.split("/")[-1].rpartition('.')[0])

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._select_file()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            if file_path.lower().endswith('.csv'):
                event.acceptProposedAction()
                self.label.setText('Drop CSV here')
            else:
                self.label.setText('Wrong file format')
        else:
            event.ignore()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path.lower().endswith('.csv'):
            self._load_csv(file_path)
        else:
            self.label.setText('Wrong file format')

    def dragLeaveEvent(self, event):
        self.label.setText(f'File: {self.path.split("/")[-1]}')

    def _select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Choose CSV file', filter='CSV Files (*.csv)'
        )
        if file_path:
            self._load_csv(file_path)

    def _enable_buttons(self, value: bool):
        self.continue_btn.setEnabled(value)
        self.continue_btn.setVisible(value)

    def _enable_table(self, value: bool):
        self.table.setEnabled(value)
        self.table.setVisible(value)

    def _load_csv(self, path):
        self.path = path
        try:
            self.df = pd.read_csv(self.path, encoding='utf-8')
            self.df = self.df.convert_dtypes()

            if self.df.empty:
                self.label.setText('File is empty')
                self.table.clear()
                self.table.setColumnCount(0)
                self.table.setRowCount(0)
                self._enable_table(False)
                self._enable_buttons(False)
                return

            headers = self.df.columns.tolist()
            preview = self.df.head(100).values.tolist()

            self._enable_table(True)
            self.table.clear()
            self.table.setColumnCount(len(headers))
            self.table.setRowCount(len(preview))
            self.table.setHorizontalHeaderLabels(headers)
            for i, row in enumerate(preview):
                for j, val in enumerate(row):
                    item = QTableWidgetItem(str(val))
                    item.setForeground(Qt.white)
                    self.table.setItem(i, j, item)

            self.label.setText(f'File: {self.path.split("/")[-1]}')
            self._enable_buttons(True)
            self._adapt_table_width()
        except Exception as e:
            self.label.setText(f'Error: {e}')
            self.table.clear()
