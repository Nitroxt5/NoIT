import numpy as np
import pandas as pd


class Alg1:
    def __init__(self):
        self.class_count = 0
        self.x = np.ndarray(0)
        self.y = np.ndarray(0)
        self.a = np.ndarray(0)
        self.x_test = np.ndarray(0)
        self.is_fit = False

    def fit(self, x_train: pd.DataFrame, y_train: pd.Series):
        self.class_count = y_train.nunique()
        self.x = x_train.to_numpy()
        self.y = y_train.to_numpy()
        split_x = np.ndarray((self.class_count,), dtype=np.ndarray)
        for i in range(self.class_count):
            split_x[i] = self.x[self.y == i]
        b = np.ndarray((self.class_count, len(self.x[0])))
        for i in range(self.class_count):
            b[i] = split_x[i].sum(0) / len(split_x[i])
        avg = b.sum(0) / self.class_count
        self.a = np.abs(b - avg)
        self.is_fit = True

    def predict(self, x_test: pd.DataFrame):
        assert self.is_fit
        self.x_test = x_test.to_numpy()
        a_sum = self.a.sum(1)
        y_pred = []
        for x in self.x_test:
            s_vals = np.zeros((len(self.a), len(self.x)))
            for i in range(len(self.x)):
                s_vals[self.y[i]][i] = self._s(self.a[self.y[i]], x, self.x[i], a_sum[self.y[i]])
            f = s_vals.max(1)
            y_pred.append(f.argmax())
        return y_pred

    @staticmethod
    def _s(a, x1, x2, a_sum):
        a_positive = a[x1 == x2]
        a_negative = a[x1 != x2]
        return (a_positive.sum() - a_negative.sum()) / a_sum
