import pandas as pd
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('../../Dataset/dataset.csv', delimiter='\t')
test_df = pd.read_csv('../../Dataset/test.csv', delimiter='\t')

X = pd.DataFrame()
Y = pd.DataFrame()

X = df.ix[:, 2:len(df.columns) - 1]
Y = df.ix[:, len(df.columns) - 1: len(df.columns)]

X_test = test_df.ix[:, 2:]

print X_test

rf = RandomForestClassifier(n_estimators=100, max_features=7)
rf.fit(X, Y)

Y_Result = rf.predict(X_test)
print Y_Result


