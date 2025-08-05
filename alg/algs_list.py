from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from alg.metric.precedence_alg import PrecedenceAlg

algs = {
    'SVM': SVC,
    'KNN': KNeighborsClassifier,
    'DecisionTree': DecisionTreeClassifier,
    'RandomForest': RandomForestClassifier,
    'LogReg': LogisticRegression,
    'PosAlg': lambda: PrecedenceAlg('pos'),
    'NegAlg': lambda: PrecedenceAlg('neg'),
    'MeanAlg': lambda: PrecedenceAlg('mean')
}
