import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

le = preprocessing.LabelEncoder()
data = pd.read_csv('FlightDelays.csv')

###################################
#making a column for delay timning in minutes (scheduled - departure time)
dept_time = data['DEP_TIME'].to_numpy()
crs_dept_time = data['CRS_DEP_TIME'].to_numpy()

time_diff_hr = (dept_time//100)-(crs_dept_time//100)
time_diff_mins = (dept_time%100) - (crs_dept_time%100)
time_diff=(time_diff_hr*60)+time_diff_mins

for i in range(0, len(time_diff)):
    if time_diff[i] < 1200:
        time_diff[i] = time_diff[i] + (24*60)
    if time_diff[i] > 1200:
        time_diff[i] = time_diff[i] - (24*60)
        
df1 = pd.DataFrame(data = time_diff, columns= ["hour_block"])
data = pd.concat([df1, data], axis=1)

###########################
#dropping the redundant features
data = data.drop(['DEP_TIME'],axis=1)
data = data.drop(['FL_DATE'],axis=1)

########################
#applying label encoder
data['CARRIER'] = le.fit_transform(data['CARRIER'])
data['DEST'] = le.fit_transform(data['DEST'])
data['FL_NUM'] = le.fit_transform(data['FL_NUM'])
data['ORIGIN'] = le.fit_transform(data['ORIGIN'])
data['TAIL_NUM'] = le.fit_transform(data['TAIL_NUM'])

##################
#labeling delay as '1' and ontime as '0' 
y_del = data['Flight Status'].to_numpy()
y_arr=[]
for k in y_del:
    if k == 'ontime':
      y_arr.append(0)
    else:
      y_arr.append(1)
np.unique(y_arr)

## concatenating in dataframe
df2 = pd.DataFrame(data=y_arr, columns=["Prob_delayed"])
data = df2.join(data)

################
#deviding the dataset into 60:40 = train:test ratio
from sklearn.model_selection import train_test_split
y = data['Prob_delayed']
X = data.drop(['Flight Status','Prob_delayed'],axis=1)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.4,random_state=1111)
X_train.head()
y = data['Prob_delayed']

#####################
#applying decision tree
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(random_state = 0)
clf.fit(X_train, y_train)
y_pred_dt = clf.predict(X_test)

print('With Decision Tree')
print('Depth of the Decision Tree is:-')
print(clf.get_depth())
print('Accuracy of Decision Tree regression classifier on test set: {:.4f}'.format(clf.score(X_test, y_test)))