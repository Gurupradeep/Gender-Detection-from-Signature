from sklearn.metrics import precision_recall_fscore_support

import pandas as pd
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import normalize


df = pd.read_csv('../../Dataset/dataset.csv', delimiter='\t')

X = pd.DataFrame()
Y = pd.DataFrame()

X = df.ix[:, 3:len(df.columns) - 1]
Y = df.ix[:, len(df.columns) - 1: len(df.columns)]

X = normalize(X)

k = 4
kf = KFold(n_splits=k)

average_accuracy = 0

for train, test in kf.split(X):
    X_train, X_test, Y_train, Y_test = X[train], X[test], Y.loc[train], Y.loc[test]
    rf = RandomForestClassifier(n_estimators=150, max_features=7, max_depth=1)
    rf.fit(X_train, Y_train)
    Y_Result = rf.predict(X_test)
    prf = precision_recall_fscore_support(Y_test, Y_Result, average='binary')
    average_accuracy += prf[2]

average_accuracy /= k
print "Average Accuracy using Random Forest Classifier = ", str(average_accuracy)

average_accuracy = 0
for train, test in kf.split(X):
    X_train, X_test, Y_train, Y_test = X[train], X[test], Y.loc[train], Y.loc[test]
    gb = GradientBoostingClassifier(n_estimators=250)
    gb.fit(X_train, Y_train)
    Y_Result = gb.predict(X_test)
    prf = precision_recall_fscore_support(Y_test, Y_Result, average='micro')
    average_accuracy += prf[2]

average_accuracy /= k
print "Average Accuracy Gradient Boosting Classifier= ", str(average_accuracy)

average_accuracy = 0
for train, test in kf.split(X):
    X_train, X_test, Y_train, Y_test = X[train], X[test], Y.loc[train], Y.loc[test]
    bdt = AdaBoostClassifier(GradientBoostingClassifier(n_estimators=250), n_estimators=250)
    bdt.fit(X_train, Y_train)
    Y_Result = bdt.predict(X_test)
    prf = precision_recall_fscore_support(Y_test, Y_Result, average='micro')
    average_accuracy += prf[2]

average_accuracy /= k
print "Average Accuracy Adaptive Boosting (with Gradient Boosting) = ", str(average_accuracy)


average_accuracy = 0
for train, test in kf.split(X):
    X_train, X_test, Y_train, Y_test = X[train], X[test], Y.loc[train], Y.loc[test]
    bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=3), n_estimators=250)
    bdt.fit(X_train, Y_train)
    Y_Result = bdt.predict(X_test)
    prf = precision_recall_fscore_support(Y_test, Y_Result, average='micro')
    average_accuracy += prf[2]

average_accuracy /= k
print "Average Accuracy Adaptive Boosting (With Decision Trees) = ", str(average_accuracy)


average_accuracy = 0
for train, test in kf.split(X):
    X_train, X_test, Y_train, Y_test = X[train], X[test], Y.loc[train], Y.loc[test]
    clf = MLPClassifier(alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(X_train, Y_train)
    Y_Result = clf.predict(X_test)
    prf = precision_recall_fscore_support(Y_test, Y_Result, average='micro')
    average_accuracy += prf[2]

average_accuracy /= k
print "Average Accuracy Using Multi Layer Perceptron = ", str(average_accuracy)





