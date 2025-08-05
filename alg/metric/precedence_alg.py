import numpy as np
import pandas as pd


class PrecedenceAlg:
    def __init__(self, kernel='pos'):
        assert kernel in ('pos', 'neg', 'mean')
        self.kernel = kernel
        self.class_count = 0
        self.x = np.ndarray(0)
        self.y = np.ndarray(0)
        self.a = np.ndarray(0)
        self.d = 0
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
        if self.kernel == 'mean':
            a_sum = self.a.sum(1)
            s_vals = np.zeros((self.class_count, len(self.x), len(self.x)))
            for cls in range(self.class_count):
                for j in range(1, len(split_x[cls])):
                    for i in range(j + 1, len(split_x[cls])):
                        s_vals[cls][j][i] = self._s(self.a[cls], split_x[cls][j], split_x[cls][i], a_sum[cls])
            self.d = s_vals.max()
        self.is_fit = True

    def predict(self, x_test: pd.DataFrame):
        assert self.is_fit
        self.x_test = x_test.to_numpy()
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
