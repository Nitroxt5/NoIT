import pandas as pd
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


def perform_testing(data: pd.DataFrame, target: pd.Series, algs: dict):
    x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=19)
    for name, alg in algs.items():
        model = alg()
        model.fit(x_train, y_train)
        y_pred = model.predict(x_test)
        print(f'{name}:')
        print(classification_report(y_test, y_pred))
