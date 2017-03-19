# Importing Libraries
import pandas as pd
from sklearn.ensemble import  RandomForestClassifier


# Loading the data
df = pd.read_csv("../../Dataset/dataset.csv",delimiter ='\t')


# Splitting the data
X = df.ix[:,2:42]
print X
Y = df.ix[:,42:43]
print Y

''''
X = []
Y = []

for x in df:
    X.append(x[2:(len(x)-1)])
    Y.append(x[len(x)-1])

#print X
print Y
'''

# print results.head()
# print train.head()

# Classifier
# max_features = sqrt(no_of_features)
rf = RandomForestClassifier(n_estimators=100,max_features=7)

rf.fit(X,Y)


print rf.feature_importances_
print rf.oob_score

eval_results = rf.predict(test)

df.to_csv("../../Dataset/randomforest_results.csv",sep = '\t')





