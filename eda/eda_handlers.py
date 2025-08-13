import numpy as np
import pandas as pd
from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtWidgets import QPushButton, QComboBox, QGraphicsProxyWidget, QGraphicsItem

from ui.widgets.dialog_window import AnimatedDialog
from ui.widgets.static_info import StaticInfo
from eda.encoding_handlers import encode_data


class EDA:
    def __init__(self, data: pd.DataFrame, pipeline):
        self.data = data
        self.target = None
        self.first = True
        self.unimportant_exists = False
        self.dropdown = QComboBox()
        self.pipeline = pipeline
        self.dialog = AnimatedDialog([])

        self.ignored_unimportant_columns = []

    def _on_click(self, action, answer: str):
        self.pipeline.history.append((self.dialog.text, answer))
        info = StaticInfo(self.pipeline.parent().parent(), self.dialog.text, answer, self.dialog.max_size,
                          self.dialog.pos())
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(info)
        proxy.setFlags(QGraphicsItem.ItemIgnoresParentOpacity | QGraphicsItem.ItemIgnoresTransformations)
        self.pipeline.scene.addItem(proxy)
        action()
        self.pipeline.next_step()

    def create_dialog_window(self, buttons: list, question='', size=QSize(400, 300), mode='horizontal'):
        pos = self.pipeline.view.mapToScene(self.pipeline.view.viewport().rect().topLeft())
        pos = QPoint(pos.x() + self.pipeline.steps[self.pipeline.current].x() -
                     self.pipeline.view.horizontalScrollBar().value(),
                     pos.y() + self.pipeline.steps[self.pipeline.current].y() - self.pipeline.node_radius)
        self.dialog = AnimatedDialog(buttons, self.pipeline.parent().parent(), question, size, pos, mode)
        self.dialog.show_animated(self.pipeline.view.horizontalScrollBar())
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(self.dialog)
        proxy.setFlags(QGraphicsItem.ItemIgnoresParentOpacity | QGraphicsItem.ItemIgnoresTransformations)
        self.pipeline.scene.addItem(proxy)

    def _create_info_window(self, info=''):
        next_btn = QPushButton('Next')
        next_btn.clicked.connect(lambda: self._on_click(lambda: None, next_btn.text()))
        self.create_dialog_window([next_btn], info)

    def handle_unimportant(self):
        self.data = self.data.convert_dtypes()
        unique_counts = self.data.nunique()
        row_count = len(self.data)
        for col, count in unique_counts.items():
            if col in self.ignored_unimportant_columns:
                continue
            if count * 2 < row_count:
                continue

            self.unimportant_exists = True
            yes_btn = QPushButton('Yes')
            no_btn = QPushButton('No')
            yes_btn.clicked.connect(lambda: self._on_click(lambda: self.data.drop(col, axis=1, inplace=True),
                                                           yes_btn.text()))
            no_btn.clicked.connect(lambda: self._on_click(lambda: self.ignored_unimportant_columns.append(col),
                                                          no_btn.text()))
            self.create_dialog_window([yes_btn, no_btn], f'Column `{col}` seems to be unimportant. Remove?')
            return False
        if not self.unimportant_exists and self.first:
            self._create_info_window('No unimportant columns found.')
            self.first = False
            return False
        return True

    def handle_duplicates(self):
        if not self.first:
            return True
        self.first = False
        duplicates_count = self.data.duplicated().value_counts().get(True, 0)
        if duplicates_count == 0:
            self._create_info_window('No duplicates found.')
            return False
        yes_btn = QPushButton('Yes')
        no_btn = QPushButton('No')
        yes_btn.clicked.connect(lambda: self._on_click(lambda: self.data.drop_duplicates(inplace=True), yes_btn.text()))
        no_btn.clicked.connect(lambda: self._on_click(lambda: None, no_btn.text()))
        self.create_dialog_window([yes_btn, no_btn], f'Detected {duplicates_count} duplicates. Remove?')
        return False

    def handle_nulls(self):
        self.data = self.data.convert_dtypes()
        nulls_count = self.data.isnull().sum()
        cols_with_empty_values = self.data.columns[self.data.isnull().any()]
        for col in cols_with_empty_values:
            self.first = False
            dc_btn = QPushButton('Delete column')
            dc_btn.clicked.connect(lambda: self._on_click(lambda: self.data.drop(col, axis=1, inplace=True),
                                                          dc_btn.text()))
            dr_btn = QPushButton('Delete row')
            dr_btn.clicked.connect(lambda: self._on_click(lambda: self.data.dropna(subset=[col], inplace=True),
                                                          dr_btn.text()))
            fr_btn = QPushButton('Fill with random')
            fr_btn.clicked.connect(lambda: self._on_click(lambda: self._fill_with_random(col), fr_btn.text()))
            if pd.api.types.is_numeric_dtype(self.data[col].dtype):
                fz_btn = QPushButton('Fill with zeros')
                fz_btn.clicked.connect(lambda: self._on_click(lambda: self.data.fillna({col: 0}, inplace=True),
                                                              fz_btn.text()))
                fa_btn = QPushButton('Fill with average')
                fa_btn.clicked.connect(lambda: self._on_click(lambda: self._fill_with_avg(col), fa_btn.text()))
                buttons = [dc_btn, dr_btn, fz_btn, fa_btn, fr_btn]
            else:
                buttons = [dc_btn, dr_btn, fr_btn]
            self.create_dialog_window(buttons, f'{nulls_count[col]} empty values detected in column `{col}`. '
                                               f'How to handle them?', QSize(400, 400), 'vertical')
            return False
        if cols_with_empty_values.empty and self.first:
            self._create_info_window('No empty values found.')
            self.first = False
            return False
        self.data = self.data.convert_dtypes()
        return True

    def _fill_with_random(self, col):
        if pd.api.types.is_numeric_dtype(self.data[col].dtype):
            low = self.data[col].min()
            high = self.data[col].max()
            if pd.api.types.is_integer_dtype(self.data[col].dtype):
                self.data[col] = self.data[col].map(lambda x: np.random.randint(low, high) if pd.isna(x) else x)
            else:
                self.data[col] = self.data[col].map(lambda x: np.random.uniform(low, high) if pd.isna(x) else x)
        else:
            unique_values = self.data[col].drop_duplicates().dropna()
            self.data[col] = self.data[col].map(lambda x: np.random.choice(unique_values) if pd.isna(x) else x)

    def _fill_with_avg(self, col):
        avg = self.data[col].mean()
        if pd.api.types.is_integer_dtype(self.data[col].dtype):
            avg = round(avg)
        self.data.fillna({col: avg}, inplace=True)

    def split_to_data_and_target(self):
        if not self.first:
            return True
        self.first = False
        self.dropdown.addItems(self.data.columns)
        self.dropdown.currentIndexChanged.connect(lambda: self._on_click(self._on_target_selection,
                                                                         self.dropdown.currentText()))
        self.create_dialog_window([self.dropdown], 'Choose a target variable:', mode='dropdown')
        return False

    def _on_target_selection(self):
        choice = self.dropdown.currentText()
        self.target = self.data[choice]
        self.data.drop(choice, axis=1, inplace=True)

    def handle_encoding(self):
        if not self.first:
            return True
        self.first = False
        self.data = encode_data(self.data)
        self._create_info_window('Data is encoded.')
        return False
