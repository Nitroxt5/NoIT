import pandas as pd
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QGraphicsProxyWidget, QGraphicsItem, QTableWidget, QPushButton
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
# from sklearn.neighbors import KNeighborsClassifier
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.linear_model import LogisticRegression
# from sklearn.svm import SVC
# from sklearn.ensemble import RandomForestClassifier
# from src.alg.metric.alg1 import Alg1
# from src.alg.metric.alg2 import Alg2
# from src.alg.metric.alg3 import Alg3

from ui.widgets.alg_chooser import AlgChooser
from ui.widgets.static_info import StaticInfo


class Tester:
    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.alg_chooser = AlgChooser([])
        self.table = QTableWidget()
        self.first = True

    def on_click(self, action):
        pos = self.pipeline.view.mapToScene(self.pipeline.view.viewport().rect().topLeft())
        pos = QPoint(pos.x() + self.pipeline.steps[self.pipeline.current].x() -
                     self.pipeline.view.horizontalScrollBar().value(),
                     pos.y() + self.pipeline.steps[self.pipeline.current].y() - self.pipeline.node_radius - 300)
        info = StaticInfo(self.pipeline.parent().parent(),
                          f'{self.alg_chooser.algs_count} algorithms were chosen', 'Next', pos=pos)
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(info)
        proxy.setFlags(QGraphicsItem.ItemIgnoresParentOpacity | QGraphicsItem.ItemIgnoresTransformations)
        self.pipeline.scene.addItem(proxy)
        action()
        self.pipeline.next_step()

    def get_algs(self):
        if not self.first:
            return True
        self.first = False
        pos = self.pipeline.view.mapToScene(self.pipeline.view.viewport().rect().topLeft())
        pos = QPoint(pos.x() + 150, pos.y() + 1300)
        next_btn = QPushButton('Next')
        next_btn.clicked.connect(lambda: self.on_click(lambda: None))
        self.alg_chooser = AlgChooser([next_btn], self.pipeline.parent().parent(), self.table, pos=pos)
        self.alg_chooser.show_animated(self.pipeline.view.horizontalScrollBar())
        proxy = QGraphicsProxyWidget()
        proxy.setWidget(self.alg_chooser)
        proxy.setFlags(QGraphicsItem.ItemIgnoresParentOpacity | QGraphicsItem.ItemIgnoresTransformations)
        self.pipeline.scene.addItem(proxy)
        return False

    def perform_testing(self):
        pass
        # x_train, x_test, y_train, y_test = train_test_split(self.eda.data, self.eda.target, test_size=0.2,
        #                                                     random_state=19)
        # for name, alg in algs.items():
        #     model = alg()
        #     model.fit(x_train, y_train)
        #     y_pred = model.predict(x_test)
        #     print(f'{name}:')
        #     print(classification_report(y_test, y_pred))
