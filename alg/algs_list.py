from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from alg.metric.pos_alg import PosAlg
from alg.metric.neg_alg import NegAlg
from alg.metric.mean_alg import MeanAlg

algs = {
    'SVM': SVC,
    'KNN': KNeighborsClassifier,
    'DecisionTree': DecisionTreeClassifier,
    'RandomForest': RandomForestClassifier,
    'LogReg': LogisticRegression,
    'PosAlg': PosAlg,
    'NegAlg': NegAlg,
    'MeanAlg': MeanAlg
}
