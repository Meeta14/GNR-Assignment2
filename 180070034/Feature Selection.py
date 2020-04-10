import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv('FlightDelays.csv')

#################
#integrating origin and destination as a feature 
feature_d = data[['DEST']]
feature_o = data[['ORIGIN']]
dest = feature_d['DEST'].to_numpy()
origin = feature_o['ORIGIN'].to_numpy()

ori_des = []
for i in range(len(origin)):
    if(dest[i]=='JFK' and origin[i] == 'DCA'):
        ori_des.append(1)
    if(dest[i]=='LGA' and origin[i] == 'DCA'):
        ori_des.append(2)
    if(dest[i]=='EWR' and origin[i] == 'DCA'):
        ori_des.append(3)
    if(dest[i]=='JFK' and origin[i] == 'IAD'):
        ori_des.append(4)
    if(dest[i]=='LGA' and origin[i] == 'IAD'):
        ori_des.append(5)
    if(dest[i]=='EWR' and origin[i] == 'IAD'):
        ori_des.append(6)
    if(dest[i]=='JFK' and origin[i] == 'BWI'):
        ori_des.append(7)
    if(dest[i]=='LGA' and origin[i] == 'BWI'):
        ori_des.append(8)
    if(dest[i]=='EWR' and origin[i] == 'BWI'):
        ori_des.append(9)
       
df2 = pd.DataFrame(data=ori_des, columns=["ori_dest"])
data = df2.join(data)

#####################
#introducing a feature that represnts difference between scheduled and departure time
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

#####################
#appling one hot encoding
Carrier = data[['CARRIER']]
carrierHeader = pd.get_dummies(Carrier['CARRIER'])
data = data.drop(['CARRIER'],axis=1)

feature1 = data[['ori_dest']]
ori_destHeader = pd.get_dummies(feature1['ori_dest'])
data = data.drop(['ori_dest'],axis=1)

DAY_WEEK = data[['DAY_WEEK']]
DAY_WEEKHeader = pd.get_dummies(DAY_WEEK.astype(str))
data = data.drop(['DAY_WEEK'],axis=1)

DAY_MONTH = data[['DAY_OF_MONTH']]
DAY_MONTHHeader = pd.get_dummies(DAY_MONTH.astype(str))
data = data.drop(['DAY_OF_MONTH'],axis=1)

########
#dropping irrelevant features
data = data.drop(['DEP_TIME'],axis=1)
data = data.drop(['DEST'],axis=1)
data = data.drop(['ORIGIN'],axis=1)
data = data.drop(['TAIL_NUM'],axis=1)
data = data.drop(['FL_NUM'],axis=1)
data = data.drop(['FL_DATE'],axis=1)
data = data.drop(['DISTANCE'],axis=1)

################
#concatinating the data
data = pd.concat([data,carrierHeader,ori_destHeader, DAY_WEEKHeader,DAY_MONTHHeader],sort = False, axis = 1) 

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
print('Accuracy of logistic regression classifier on test set on scale of 0-1 is: {:.5f}'.format(LR.score(X_test, y_test)))