# Importing Libraries
import pandas as pd
from sklearn.svm import SVC


# Loading the data
df = pd.read_csv("../../Dataset/dataset.csv",delimiter ='\t')


# Splitting the data
X = df.ix[:, 3:42]
print X
Y = df.ix[:, 42:43]
print Y

svm = SVC(gamma=0.001)


svm.fit(X,Y)

# TO BE DONE
'''

# Predicting class labels
eval_results = svm.predict(X_test)

# Score on test data (Accuracy)
acc = gb.score(X_test,Y_test)
print('Accuracy: %.4f' %acc)


'''
