from sklearn.metrics import precision_recall_fscore_support

import pandas as pd
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('../../Dataset/dataset.csv', delimiter='\t')

X = pd.DataFrame()
Y = pd.DataFrame()

X = df.ix[:, 2:len(df.columns) - 1]
Y = df.ix[:, len(df.columns) - 1: len(df.columns)]

kf = KFold(n_splits=4)

for train, test in kf.split(X):
    X_train, X_test, Y_train, Y_test = X.loc[train], X.loc[test], Y.loc[train], Y.loc[test]
    rf = RandomForestClassifier(n_estimators=100, max_features=7)
    rf.fit(X_train, Y_train)
    Y_Result = rf.predict(X_test)
    print rf.feature_importances_
    print precision_recall_fscore_support(Y_test, Y_Result, average='micro')





