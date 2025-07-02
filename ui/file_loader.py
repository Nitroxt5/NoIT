import pandas as pd
from PyQt5.QtWidgets import (
    QLabel, QPushButton, QWidget, QFileDialog,
    QVBoxLayout, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class CsvDropZone(QWidget):
    def __init__(self, on_success_callback=None):
        super().__init__()
        self.setAcceptDrops(True)
        self.on_success_callback = on_success_callback
        self.df = pd.DataFrame()

        self.label = QLabel("Drop CSV here or click and choose it")
        self.label.setFont(QFont("Segoe UI", 11))
        self.label.setAlignment(Qt.AlignCenter)

        self.setStyleSheet("""
            QWidget {
                background-color: rgba(20, 40, 80, 160);
                border: 1px solid rgba(255, 255, 255, 60);
                border-radius: 12px;
                color: white;
                font-family: 'Segoe UI', sans-serif;
            }

            QLabel {
                font-size: 30px;
            }

            QPushButton {
                color: white;
                background-color: rgba(30, 60, 120, 100);
                border: 1px solid rgba(255, 255, 255, 40);
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 30px;
            }

            QPushButton:hover {
                background-color: rgba(100, 140, 200, 180);
            }

            QTableWidget {
                color: white;
                gridline-color: rgba(255,255,255,40);
                border: none;
            }
            QTableCornerButton::section {
                background-color: rgba(20, 40, 80, 160);
            }

            QHeaderView::section {
                background-color: rgba(255,255,255,40);
                color: white;
                font-weight: bold;
                border: none;
                padding: 4px;
            }
        """)

        self.table = QTableWidget()
        self.table.setCornerButtonEnabled(False)
        self.table.verticalHeader().setDefaultSectionSize(28)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.continue_btn = QPushButton('Continue', self)
        self.continue_btn.clicked.connect(self.on_continue)
        self.continue_btn.setEnabled(False)
        self.continue_btn.setVisible(False)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.label)

    def on_continue(self):
        if self.on_success_callback:
            self.on_success_callback(self.df)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.select_file()

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
            self.load_csv(file_path)
        else:
            self.label.setText('Wrong file format')

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Choose CSV file', filter='CSV Files (*.csv)'
        )
        if file_path:
            self.load_csv(file_path)

    def load_csv(self, path):
        try:
            self.df = pd.read_csv(path, encoding='utf-8')

            if self.df.empty:
                self.label.setText('File is empty')
                self.table.clear()
                return

            headers = self.df.columns.tolist()
            preview = self.df.head(100).values.tolist()

            self.table.clear()
            self.table.setColumnCount(len(headers))
            self.table.setRowCount(len(preview))
            self.table.setHorizontalHeaderLabels(headers)
            for i, row in enumerate(preview):
                for j, val in enumerate(row):
                    item = QTableWidgetItem(str(val))
                    item.setForeground(Qt.white)
                    self.table.setItem(i, j, item)

            self.label.setText(f'File: {path.split("/")[-1]}')
            self.continue_btn.setEnabled(True)
            self.continue_btn.setVisible(True)
            self.layout.addWidget(self.table)
            self.layout.addWidget(self.continue_btn)
        except Exception as e:
            self.label.setText(f"Error: {e}")
            self.table.clear()
