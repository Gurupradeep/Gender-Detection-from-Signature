# Importing Libraries
import pandas as pd
from sklearn.ensemble import  GradientBoostingClassifier


# Loading the data
df = pd.read_csv("../../Dataset/dataset.csv",delimiter ='\t')


# Splitting the data
X = df.ix[:,2:42]
print X
Y = df.ix[:,42:43]
print Y


# print results.head()
# print train.head()

# Classifier
# max_features = sqrt(no_of_features)
gb = GradientBoostingClassifier(n_estimators=100,max_features=7)

gb.fit(X,Y)


print gb.feature_importances_
print gb.oob_improvement_
print gb.train_score_

# TO BE DONE
'''

# Predicting class labels
eval_results = gb.predict(X_test)

# Score on test data (Accuracy)
acc = gb.score(X_test,Y_test)
print('Accuracy: %.4f' %acc)


'''

df.to_csv("../../Dataset/randomforest_results.csv",sep = '\t')





