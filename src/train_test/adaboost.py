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

mask = np.random.rand(len(df)) < 0.75

train = df[mask]
test = df[mask]

X = []
Y = []

for x in train:
    X.append(x[2: len(x) - 1])
    Y.append(x[len(x)-1])

X_Test = []
Y_Test = []

for x_test in test:
    X_Test.append(x_test[2: len(x_test) - 1])
    Y_Test.append(x_test[len(x_test) - 1])

# tune parameters here.
bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), algorithm="SAMME", n_estimators=200)

bdt.fit(X, Y)

# predict
Y_Result = bdt.predict(X_Test)

precision_recall_fscore_support(Y_Test, Y_Result, average='micro')
