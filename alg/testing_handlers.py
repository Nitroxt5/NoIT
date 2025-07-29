# import pandas as pd
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsItem, QPushButton
from sklearn.model_selection import train_test_split, GridSearchCV
# from sklearn.ensemble import RandomForestClassifier
from time import perf_counter

from ui.widgets.alg_chooser import AlgChooser
from ui.widgets.static_info import StaticInfo
from alg.algs_list import algs


class Tester:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.alg_chooser = AlgChooser([])
        self.first = True
        self.true_pred = {}
        self.times = {}

    def on_click(self, action, answer):
        self.create_static_info(f'{self.alg_chooser.algs_count} algorithms were chosen', answer)
        action()
        self.pipeline.next_step()

    def create_static_info(self, text, answer):
        pos = self.pipeline.view.mapToScene(self.pipeline.view.viewport().rect().topLeft())
        pos = QPoint(pos.x() + self.pipeline.steps[self.pipeline.current].x() -
                     self.pipeline.view.horizontalScrollBar().value(),
                     pos.y() + self.pipeline.steps[self.pipeline.current].y() - 310)
        info = StaticInfo(self.pipeline.parent().parent(), text, answer, pos=pos)
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(info)
        proxy.setFlags(QGraphicsItem.ItemIgnoresParentOpacity | QGraphicsItem.ItemIgnoresTransformations)
        self.pipeline.scene.addItem(proxy)

    def get_algs(self):
        if not self.first:
            return True
        self.first = False
        pos = self.pipeline.view.mapToScene(self.pipeline.view.viewport().rect().topLeft())
        pos = QPoint(pos.x() + 150, pos.y() + 1300)
        next_btn = QPushButton('Next')
        next_btn.clicked.connect(lambda: self.on_click(lambda: None, next_btn.text()))
        self.alg_chooser = AlgChooser([next_btn], self.pipeline.parent().parent(), pos=pos)
        self.alg_chooser.show_animated(self.pipeline.view.horizontalScrollBar())
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(self.alg_chooser)
        proxy.setFlags(QGraphicsItem.ItemIgnoresParentOpacity | QGraphicsItem.ItemIgnoresTransformations)
        self.pipeline.scene.addItem(proxy)
        return False

    def perform_testing(self):
        x_train, x_test, y_train, y_test = train_test_split(self.pipeline.eda.data, self.pipeline.eda.target,
                                                            test_size=0.2, random_state=19)
        for row in range(self.alg_chooser.algs_count):
            model_name = self.alg_chooser.table.item(row, 0).text()
            model = algs[model_name[:-1]]()
            fit_time_start = perf_counter()
            model.fit(x_train, y_train)
            fit_time = perf_counter() - fit_time_start
            predict_time_start = perf_counter()
            self.true_pred[model_name] = (y_test, model.predict(x_test))
            predict_time = perf_counter() - predict_time_start
            self.times[model_name] = (fit_time, predict_time)
        self.pipeline.eda.create_info_window('Testing done.')
        return True
