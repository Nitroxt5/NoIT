import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from alg.metric.precedence_dichotomy import PrecedenceDichotomyAlg


class PrecedenceDichotomyUpgradedAlg(BaseEstimator, ClassifierMixin):
    def __init__(self, kernel='pos'):
        assert kernel in ('pos', 'neg', 'mean')
        self.kernel = kernel
        self.x = np.ndarray(0)
        self.y = np.ndarray(0)
        self.main_alg_y = np.ndarray(0)
        self.x_test = np.ndarray(0)
        self.class_count = 0
        self.class_count_for_first_start = 0
        self.merged_nodes_count = 0
        self.main_alg = PrecedenceDichotomyAlg(self.kernel)
        self.helper_algs = []

    def _prepare_data(self, x_train: pd.DataFrame, y_train: pd.Series):
        self.class_count = y_train.nunique()
        self.class_count_for_first_start = 1 << (self.class_count.bit_length() - 1)
        self.merged_nodes_count = self.class_count - self.class_count_for_first_start
        self.x = x_train.to_numpy()
        self.y = y_train.to_numpy()
        self.main_alg_y = self.y.copy()
        old_number = self.class_count - 2 * self.merged_nodes_count
        new_number = old_number
        for i in range(self.merged_nodes_count):
            self.main_alg_y[self.main_alg_y == old_number] = new_number
            self.main_alg_y[self.main_alg_y == old_number + 1] = new_number
            new_number += 1
            old_number += 2

    def _create_algs(self):
        for i in range(self.merged_nodes_count):
            self.helper_algs.append(PrecedenceDichotomyAlg(self.kernel))

    def fit(self, x_train: pd.DataFrame, y_train: pd.Series):
        self._prepare_data(x_train, y_train)
        self._create_algs()
        self.main_alg.fit(self.x, self.main_alg_y)
        current_class = self.class_count_for_first_start - self.merged_nodes_count
        for i, alg in enumerate(self.helper_algs):
            tmp_x = self.x[self.main_alg_y == current_class]
            tmp_y = self.y[self.main_alg_y == current_class]
            tmp_y -= current_class + i
            alg.fit(tmp_x, tmp_y)
            current_class += 1

    def predict(self, x_test: pd.DataFrame):
        self.x_test = x_test.to_numpy()
        y_pred = self.main_alg.predict(self.x_test)
        current_class = self.class_count_for_first_start - 1
        shift = self.class_count - 2
        for i in range(len(self.helper_algs) - 1, -1, -1):
            tmp_x = self.x_test[y_pred == current_class]
            y_pred_tmp = self.helper_algs[i].predict(tmp_x) + shift
            y_pred[y_pred == current_class] = y_pred_tmp
            current_class -= 1
            shift -= 2
        return y_pred
