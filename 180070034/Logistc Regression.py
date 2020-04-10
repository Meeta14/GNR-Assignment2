import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('FlightDelays.csv')

############################
#applying one hot encoding to the dataset
Carrier = data[['CARRIER']]
carrierHeader = pd.get_dummies(Carrier['CARRIER'])
data = data.drop(['CARRIER'],axis=1)

DEST = data[['DEST']]
destHeader = pd.get_dummies(DEST['DEST'])
data = data.drop(['DEST'],axis=1)

ORIGIN = data[['ORIGIN']]
originHeader = pd.get_dummies(ORIGIN['ORIGIN'])
data = data.drop(['ORIGIN'],axis=1)

Tail_num = data[['TAIL_NUM']]
Tail_numHeader = pd.get_dummies(Tail_num['TAIL_NUM'])
data = data.drop(['TAIL_NUM'],axis=1)

fl_num = data[['FL_NUM']]
fl_numHeader = pd.get_dummies(fl_num.astype(str))
data = data.drop(['FL_NUM'],axis=1)

FL_DATE = data[['FL_DATE']]
FL_DATEHeader = pd.get_dummies(FL_DATE.astype(str))
data = data.drop(['FL_DATE'],axis=1)

DAY_WEEK = data[['DAY_WEEK']]
DAY_WEEKHeader = pd.get_dummies(DAY_WEEK.astype(str))
data = data.drop(['DAY_WEEK'],axis=1)

DAY_MONTH = data[['DAY_OF_MONTH']]
DAY_MONTHHeader = pd.get_dummies(DAY_MONTH.astype(str))
data = data.drop(['DAY_OF_MONTH'],axis=1)

################
#concatinating the data
data = pd.concat([data, destHeader, originHeader, DAY_WEEKHeader,carrierHeader],sort = False, axis = 1) 

#############################
##labeling delay as '1' and ontime as '0' 
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

###################################
#splitting the data set 
from sklearn.model_selection import train_test_split
y = data['Prob_delayed']
X = data.drop(['Flight Status','Prob_delayed'],axis=1)
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.4,random_state=1111)
X_train.head()
y = data['Prob_delayed']

############################
#training and testing the dataset
from sklearn.linear_model import LogisticRegression
LR = LogisticRegression(C=1, solver='liblinear').fit(X_train,y_train)
yhat = LR.predict(X_test)
yhat_prob = LR.predict_proba(X_test)

print('Accuracy of logistic regression classifier on test set on scale of 0-1 is: {:.3f}'.format(LR.score(X_test, y_test)))