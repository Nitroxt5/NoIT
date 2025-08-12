from PyQt5.QtCore import QPoint, QThread, pyqtSignal, QSize
from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsItem, QPushButton, QComboBox, QLineEdit
from sklearn.model_selection import train_test_split, GridSearchCV
from time import perf_counter
from math import ceil

from ui.widgets.alg_chooser import AlgChooser
from ui.widgets.static_info import StaticInfo
from ui.widgets.progress_bar import ProgressBar
from alg.algs_list import algs, hyperparams


class Tester(QThread):
    progress_changed = pyqtSignal(int, str)

    def __init__(self, pipeline):
        super().__init__()
        self.pipeline = pipeline
        self.alg_chooser = AlgChooser([])
        self.progress_bar = ProgressBar([])
        self.first = True
        self.true = {}
        self.pred = {}
        self.params = {}
        self.fit_time = {}
        self.pred_time = {}

    def _on_click(self, action, text, answer):
        self._create_static_info(text, answer)
        action()
        self.pipeline.next_step()

    def _create_static_info(self, text, answer):
        pos = self.pipeline.view.mapToScene(self.pipeline.view.viewport().rect().topLeft())
        pos = QPoint(pos.x() + self.pipeline.steps[self.pipeline.current].x() -
                     self.pipeline.view.horizontalScrollBar().value(),
                     pos.y() + self.pipeline.steps[self.pipeline.current].y() - 310)
        info = StaticInfo(self.pipeline.parent().parent(), text, answer, pos=pos)
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(info)
        proxy.setFlags(QGraphicsItem.ItemIgnoresParentOpacity | QGraphicsItem.ItemIgnoresTransformations)
        self.pipeline.scene.addItem(proxy)

    def _create_progress_bar(self, buttons, start_text, end_text):
        pos = self.pipeline.view.mapToScene(self.pipeline.view.viewport().rect().topLeft())
        pos = QPoint(pos.x() + self.pipeline.steps[self.pipeline.current].x() -
                     self.pipeline.view.horizontalScrollBar().value(),
                     pos.y() + self.pipeline.steps[self.pipeline.current].y() - self.pipeline.node_radius)
        self.progress_bar = ProgressBar(buttons, self.pipeline.parent().parent(), start_text, end_text, pos=pos,
                                        on_success_callback=self.start)
        self.progress_changed.connect(self.progress_bar.check_completion)
        self.progress_bar.show_animated(self.pipeline.view.horizontalScrollBar())
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(self.progress_bar)
        proxy.setFlags(QGraphicsItem.ItemIgnoresParentOpacity | QGraphicsItem.ItemIgnoresTransformations)
        self.pipeline.scene.addItem(proxy)

    def get_algs(self):
        if not self.first:
            return True
        self.first = False
        size = self.pipeline.view.size()
        size = QSize(size.width() - 200, size.height() - 200)
        pos = self.pipeline.view.mapToScene(self.pipeline.view.viewport().rect().topLeft())
        pos = QPoint(pos.x() + 100, pos.y() + size.height() + 100)
        next_btn = QPushButton('Next')
        next_btn.clicked.connect(lambda: self._on_click(lambda: None,
                                                        f'{self.alg_chooser.algs_count} algorithms were chosen',
                                                        next_btn.text()))
        self.alg_chooser = AlgChooser([next_btn], self.pipeline.parent().parent(), size, pos)
        self.alg_chooser.show_animated(self.pipeline.view.horizontalScrollBar())
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(self.alg_chooser)
        self.pipeline.scene.addItem(proxy)
        return False

    def _test_alg(self, row, x_train, x_test, y_train, y_test):
        model_name = self.alg_chooser.table.item(row, 0).text()
        param_grid = self._get_param_grid(row, model_name)
        model = algs[model_name[:-1]]()
        grid_search = GridSearchCV(estimator=model, param_grid=param_grid)
        fit_time_start = perf_counter()
        grid_search.fit(x_train, y_train)
        fit_time = perf_counter() - fit_time_start
        predict_time_start = perf_counter()
        self.pred[model_name] = grid_search.best_estimator_.predict(x_test)
        predict_time = perf_counter() - predict_time_start
        self.true[model_name] = y_test
        self.params[model_name] = grid_search.best_params_
        self.fit_time[model_name] = fit_time
        self.pred_time[model_name] = predict_time

    def _get_param_grid(self, row, model_name):
        param_grid = {}
        h_layout = self.alg_chooser.table.cellWidget(row, 1).layout()
        for v_layout in h_layout.children():
            for i in range(v_layout.count()):
                widget = v_layout.itemAt(i).widget()
                if isinstance(widget, QComboBox):
                    if widget.currentText() == 'auto':
                        param_grid[widget.objectName()] = hyperparams[model_name[:-1]][widget.objectName()]
                    else:
                        param_grid[widget.objectName()] = [widget.currentText()]
                if isinstance(widget, QLineEdit):
                    if widget.text() == '':
                        param_grid[widget.objectName()] = hyperparams[model_name[:-1]][widget.objectName()]['range']
                    else:
                        param_grid[widget.objectName()] = [int(widget.text())]
        return param_grid

    def perform_testing(self):
        if not self.first:
            return True
        self.first = False
        next_btn = QPushButton('Next')
        next_btn.clicked.connect(lambda: self._on_click(lambda: None,
                                                        f'{self.alg_chooser.algs_count} algorithms were tested',
                                                        next_btn.text()))
        self._create_progress_bar([next_btn], 'Testing is in progress...', 'Testing is done.')
        return False

    def run(self):
        x_train, x_test, y_train, y_test = train_test_split(self.pipeline.eda.data, self.pipeline.eda.target,
                                                            test_size=0.2, random_state=19)
        if self.alg_chooser.algs_count != 0:
            self.progress_changed.emit(0, f'Currently testing {self.alg_chooser.table.item(0, 0).text()}...')
        for row in range(self.alg_chooser.algs_count):
            self._test_alg(row, x_train, x_test, y_train, y_test)
            if row == self.alg_chooser.algs_count - 1:
                text = ''
            else:
                text = f'Currently testing {self.alg_chooser.table.item(row + 1, 0).text()}...'
            self.progress_changed.emit(ceil((row + 1) / self.alg_chooser.algs_count * 100), text)
        if self.alg_chooser.algs_count == 0:
            self.progress_changed.emit(self.progress_bar.progress.maximum(), '')
