from PyQt5.QtCore import QPoint, QThread, pyqtSignal
from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsItem, QPushButton
from sklearn.model_selection import train_test_split
from time import perf_counter
from math import ceil

from ui.widgets.alg_chooser import AlgChooser
from ui.widgets.static_info import StaticInfo
from ui.widgets.progress_bar import ProgressBar
from alg.algs_list import algs


class Tester(QThread):
    progress_changed = pyqtSignal(int)

    def __init__(self, pipeline):
        super().__init__()
        self.pipeline = pipeline
        self.alg_chooser = AlgChooser([])
        self.progress_bar = ProgressBar([])
        self.first = True
        self.true_pred = {}
        self.times = {}

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
        self.progress_changed.connect(self.progress_bar.progress.setValue)
        self.progress_bar.show_animated(self.pipeline.view.horizontalScrollBar())
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(self.progress_bar)
        proxy.setFlags(QGraphicsItem.ItemIgnoresParentOpacity | QGraphicsItem.ItemIgnoresTransformations)
        self.pipeline.scene.addItem(proxy)

    def get_algs(self):
        if not self.first:
            return True
        self.first = False
        pos = self.pipeline.view.mapToScene(self.pipeline.view.viewport().rect().topLeft())
        pos = QPoint(pos.x() + 150, pos.y() + 1300)
        next_btn = QPushButton('Next')
        next_btn.clicked.connect(lambda: self._on_click(lambda: None,
                                                        f'{self.alg_chooser.algs_count} algorithms were chosen',
                                                        next_btn.text()))
        self.alg_chooser = AlgChooser([next_btn], self.pipeline.parent().parent(), pos=pos)
        self.alg_chooser.show_animated(self.pipeline.view.horizontalScrollBar())
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(self.alg_chooser)
        proxy.setFlags(QGraphicsItem.ItemIgnoresParentOpacity | QGraphicsItem.ItemIgnoresTransformations)
        self.pipeline.scene.addItem(proxy)
        return False

    def _test_alg(self, row, x_train, x_test, y_train, y_test):
        model_name = self.alg_chooser.table.item(row, 0).text()
        model = algs[model_name[:-1]]()
        fit_time_start = perf_counter()
        model.fit(x_train, y_train)
        fit_time = perf_counter() - fit_time_start
        predict_time_start = perf_counter()
        self.true_pred[model_name] = (y_test, model.predict(x_test))
        predict_time = perf_counter() - predict_time_start
        self.times[model_name] = (fit_time, predict_time)

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
        for row in range(self.alg_chooser.algs_count):
            self._test_alg(row, x_train, x_test, y_train, y_test)
            self.progress_changed.emit(ceil((row + 1) / self.alg_chooser.algs_count * 100))
        if self.alg_chooser.algs_count == 0:
            self.progress_changed.emit(self.progress_bar.progress.maximum())
