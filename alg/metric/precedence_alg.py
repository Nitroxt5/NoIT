import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin


class PrecedenceAlg(BaseEstimator, ClassifierMixin):
    def __init__(self, kernel='pos'):
        assert kernel in ('pos', 'neg', 'mean')
        self.kernel = kernel
        self.class_count = 0
        self.x = np.ndarray(0)
        self.y = np.ndarray(0)
        self.a = np.ndarray(0)
        self.d = 0
        self.x_test = np.ndarray(0)

    def _prepare_data_pd(self, x_train: pd.DataFrame, y_train: pd.Series):
        self.class_count = y_train.nunique()
        self.x = x_train.to_numpy()
        self.y = y_train.to_numpy()

    def _prepare_data_np(self, x_train: np.ndarray, y_train: np.ndarray):
        self.class_count = len(np.unique(y_train))
        self.x = x_train.copy()
        self.y = y_train.copy()

    def fit(self, x_train: [pd.DataFrame, np.ndarray], y_train: [pd.Series, np.ndarray]):
        if isinstance(x_train, pd.DataFrame) and isinstance(y_train, pd.Series):
            self._prepare_data_pd(x_train, y_train)
        elif isinstance(x_train, np.ndarray) and isinstance(y_train, np.ndarray):
            self._prepare_data_np(x_train, y_train)
        else:
            raise TypeError(f'x_train or y_train is of an unappropriate type: {type(x_train)}, {type(y_train)}')
        split_x = np.ndarray((self.class_count,), dtype=np.ndarray)
        for i in range(self.class_count):
            split_x[i] = self.x[self.y == i]

        # b = np.ndarray((self.class_count, len(self.x[0])))
        # for i in range(self.class_count):
        #     b[i] = split_x[i].sum(0) / len(split_x[i])
        # avg = b.sum(0) / self.class_count
        # avg = self.x.sum(0) / len(self.x)

        m1 = np.ndarray((self.class_count, len(self.x[0])))
        for i in range(self.class_count):
            m1[i] = split_x[i].sum(0)
        m = np.ndarray((self.class_count,))
        for i in range(self.class_count):
            m[i] = len(split_x[i])
        b = np.ndarray((self.class_count, len(self.x[0])))
        if self.class_count == 2:
            b[0] = (m[1] + m1[0] - m1[1]) / (m[0] + m[1])
            b[1] = (m[0] + m1[1] - m1[0]) / (m[0] + m[1])
            avg = np.full(b[0].shape, 0.5)
        else:
            for i in range(self.class_count):
                b[i] = (m.sum() - m[i] + m1[i] - m1.sum(0) + m1[i]) / m.sum()
            avg = ((self.class_count - 1) * m.sum() - (self.class_count - 2) * m1.sum(0)) / self.class_count / m.sum()

        self.a = np.abs(b - avg)
        if self.kernel == 'mean':
            a_sum = self.a.sum(1)
            s_vals = np.zeros((self.class_count, len(self.x), len(self.x)))
            for cls in range(self.class_count):
                for j in range(1, len(split_x[cls])):
                    for i in range(j + 1, len(split_x[cls])):
                        s_vals[cls][j][i] = self._s(self.a[cls], split_x[cls][j], split_x[cls][i], a_sum[cls])
            self.d = s_vals.max()

    def predict(self, x_test: [pd.DataFrame, np.ndarray]):
        if isinstance(x_test, pd.DataFrame):
            self.x_test = x_test.to_numpy()
        elif isinstance(x_test, np.ndarray):
            self.x_test = x_test.copy()
        else:
            raise TypeError(f'x_test is of an unappropriate type: {type(x_test)}')
        a_sum = self.a.sum(1)
        y_pred = []
        for x in self.x_test:
            if self.kernel == 'neg':
                s_vals = np.full((len(self.a), len(self.x)), 1000.)
            else:
                s_vals = np.zeros((len(self.a), len(self.x)))
            for i in range(len(self.x)):
                if self.kernel == 'mean':
                    s_vals[self.y[i]][i] = max(0,
                                               1 - self._s(self.a[self.y[i]], x, self.x[i], a_sum[self.y[i]]) / self.d)
                else:
                    s_vals[self.y[i]][i] = self._s(self.a[self.y[i]], x, self.x[i], a_sum[self.y[i]])
            if self.kernel == 'neg':
                f = s_vals.min(1)
                y_pred.append(f.argmin())
            else:
                f = s_vals.max(1)
                y_pred.append(f.argmax())
        return np.array(y_pred)

    def _s(self, a, x1, x2, a_sum):
        a_positive = a[x1 == x2]
        a_negative = a[x1 != x2]
        if self.kernel == 'pos':
            return (a_positive.sum() - a_negative.sum()) / a_sum
        return 1 - ((a_positive.sum() - a_negative.sum()) / a_sum)
