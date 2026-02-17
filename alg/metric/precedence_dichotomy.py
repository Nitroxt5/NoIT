import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin


class Node:
    def __init__(self, L: int, R: int):
        self.L = L
        self.R = R
        self.mid = (self.L + self.R) // 2
        self.x = np.ndarray(0)
        self.y = np.ndarray(0)
        self.split_x = np.ndarray(0)
        self.m1 = np.ndarray(0)
        self.m = np.ndarray(0)
        self.a = np.ndarray(0)
        self.a_sum = np.ndarray(0)
        self.d = 0
        self.left = None
        self.right = None


class PrecedenceDichotomyAlg(BaseEstimator, ClassifierMixin):
    def __init__(self, kernel='pos'):
        assert kernel in ('pos', 'neg', 'mean')
        self.kernel = kernel
        self.class_count = 0
        self.x = np.ndarray(0)
        self.y = np.ndarray(0)
        self.x_test = np.ndarray(0)
        self.root = None
        self.res = 0

    def _prepare_data(self, x_train: pd.DataFrame, y_train: pd.Series):
        self.class_count = y_train.nunique()
        self.x = x_train.to_numpy()
        self.y = y_train.to_numpy()

    def _build_tree(self, root: Node):
        if root is None:
            return
        self._fit_node(root)
        if root.R - root.L == 1:
            return
        if root.mid - root.L > 0:
            root.left = Node(root.L, root.mid)
        if root.R - root.mid - 1 > 0:
            root.right = Node(root.mid + 1, root.R)
        self._build_tree(root.left)
        self._build_tree(root.right)

    def _split_data(self, node: Node):
        node.split_x = np.ndarray((2,), dtype=np.ndarray)
        node.split_x[0] = self.x[(self.y >= node.L) & (self.y <= node.mid)]
        node.split_x[1] = self.x[(self.y > node.mid) & (self.y <= node.R)]
        node.x = self.x[(self.y >= node.L) & (self.y <= node.R)]
        node.y = self.y[(self.y >= node.L) & (self.y <= node.R)]
        node.y[node.y <= node.mid] = 0
        node.y[node.y > node.mid] = 1
        node.m1 = np.ndarray((2, len(node.x[0])))
        for i in range(2):
            node.m1[i] = node.split_x[i].sum(0)
        node.m = np.ndarray((2,))
        for i in range(2):
            node.m[i] = len(node.split_x[i])

    def _fit_node(self, node: Node):
        self._split_data(node)

        b = np.ndarray((2, len(node.x[0])))
        b[0] = (node.m[1] + node.m1[0] - node.m1[1]) / (node.m[0] + node.m[1])
        b[1] = (node.m[0] + node.m1[1] - node.m1[0]) / (node.m[0] + node.m[1])
        avg = np.full(b[0].shape, 0.5)

        node.a = np.abs(b - avg)
        node.a_sum = node.a.sum(1)
        if self.kernel == 'mean':
            a_sum = node.a.sum(1)
            s_vals = np.zeros((2, len(node.x), len(node.x)))
            for cls in range(2):
                for j in range(1, len(node.split_x[cls])):
                    for i in range(j + 1, len(node.split_x[cls])):
                        s_vals[cls][j][i] = self._s(node.a[cls], node.split_x[cls][j], node.split_x[cls][i], a_sum[cls])
            node.d = s_vals.max()

    def fit(self, x_train: pd.DataFrame, y_train: pd.Series):
        self._prepare_data(x_train, y_train)
        self.root = Node(0, self.class_count - 1)
        self._build_tree(self.root)

    def _predict_el(self, node: Node, x: np.ndarray):
        if node is None:
            return
        if self.kernel == 'neg':
            s_vals = np.full((2, len(node.x)), 1000.)
        else:
            s_vals = np.zeros((2, len(node.x)))
        for i in range(len(node.x)):
            if self.kernel == 'mean':
                s_vals[node.y[i]][i] = max(0,
                                           1 - self._s(node.a[node.y[i]], x, node.x[i], node.a_sum[node.y[i]]) / node.d)
            else:
                s_vals[node.y[i]][i] = self._s(node.a[node.y[i]], x, node.x[i], node.a_sum[node.y[i]])
        if self.kernel == 'neg':
            f = s_vals.min(1)
            turn = f.argmin()
        else:
            f = s_vals.max(1)
            turn = f.argmax()
        if turn == 0:
            if node.R - node.L == 1:
                self.res = node.L
            self._predict_el(node.left, x)
        else:
            if node.R - node.L == 1:
                self.res = node.R
            self._predict_el(node.right, x)

    def predict(self, x_test: pd.DataFrame):
        self.x_test = x_test.to_numpy()
        y_pred = []
        for x in self.x_test:
            self._predict_el(self.root, x)
            y_pred.append(self.res)
        return np.array(y_pred)

    def _s(self, a, x1, x2, a_sum):
        a_positive = a[x1 == x2]
        a_negative = a[x1 != x2]
        if self.kernel == 'pos':
            return (a_positive.sum() - a_negative.sum()) / a_sum
        return 1 - ((a_positive.sum() - a_negative.sum()) / a_sum)