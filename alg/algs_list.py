from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from alg.metric.alg1 import Alg1
from alg.metric.alg2 import Alg2
from alg.metric.alg3 import Alg3

algs = {
    'SVM': SVC,
    'KNN': KNeighborsClassifier,
    'DecisionTree': DecisionTreeClassifier,
    'LogReg': LogisticRegression,
    'PosAlg': Alg1,
    'NegAlg': Alg2,
    'MeanAlg': Alg3
}
