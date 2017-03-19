from sklearn.metrics import precision_recall_fscore_support

import pandas as pd
import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv('../../Dataset/dataset.csv', delimiter='\t')

'''
    Todo : Random Splitting
'''

dataset = df.values

mask = np.random.rand(len(df)) < .80

train = df[mask]
test = df[~mask]

X = pd.DataFrame()
Y = pd.DataFrame()

X = train.ix[:, 2:len(train.columns) - 1]
Y = train.ix[:, len(train.columns) - 1: len(train.columns)]

X_Test = pd.DataFrame()
Y_Test = pd.DataFrame()

X_Test = test.ix[:, 2:len(test.columns) - 1]
Y_Test = test.ix[:, len(test.columns) - 1: len(test.columns)]

print "Training Data Set Size : ", str(len(X))
print "Testing Data Set Size : ", str(len(X_Test))

# tune parameters here.
bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), n_estimators=200)

bdt.fit(X, Y)

# predict
Y_Result = bdt.predict(X_Test)

print precision_recall_fscore_support(Y_Test, Y_Result, average='micro')
