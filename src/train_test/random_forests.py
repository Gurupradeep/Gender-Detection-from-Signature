from sklearn.metrics import precision_recall_fscore_support

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler, normalize

df = pd.read_csv('../../Dataset/dataset.csv', delimiter='\t')

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

# After Normalising
X_standard = normalize(X)
print X_standard.shape


X_Test = test.ix[:, 2:len(test.columns) - 1]
Y_Test = test.ix[:, len(test.columns) - 1: len(test.columns)]

X_Test_standard = normalize(X_Test)
print X_Test_standard.shape

print "Training Data Set Size : ", str(len(X))
print "Testing Data Set Size : ", str(len(X_Test))

# tune parameters here.
rf = RandomForestClassifier(n_estimators=150, max_features=20)

rf.fit(X_standard, Y)
# predict
Y_Result = rf.predict(X_Test_standard)

print precision_recall_fscore_support(Y_Test, Y_Result, average='micro')





