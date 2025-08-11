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
    'Precedence': PrecedenceAlg
}

hyperparams = {
    'SVM': {'kernel': ['linear', 'poly', 'rbf', 'sigmoid']},
    'KNN': {'n_neighbors': {'range': list(range(2, 101)), 'default': 5}},
    'DecisionTree': {'criterion': ['gini', 'entropy', 'log_loss'], 'max_depth': {'range': list(range(5, 1001, 5)),
                                                                                 'default': 100}},
    'RandomForest': {'n_estimators': {'range': list(range(50, 1001, 10)), 'default': 100},
                     'criterion': ['gini', 'entropy', 'log_loss'], 'max_depth': {'range': list(range(5, 1001, 5)),
                                                                                 'default': 100}},
    'LogReg': {},
    'Precedence': {'kernel': ['pos', 'neg', 'mean']}
}
