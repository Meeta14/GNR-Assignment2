#this code plots different graphs for between features and delay 
#un-comment the savefig if you want to save the plots
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random

#importing data set
data = pd.read_csv('FlightDelays.csv')

#########################
#plotting % of flights ontime/delay
count_ontime = len(data[data['Flight Status']=='ontime'])
count_delayed = len(data[data['Flight Status']=='delayed'])

objects = ( 'ontime', 'Delayed')
per_ontime = count_ontime/(count_ontime+count_delayed)
per_delay = count_delayed/(count_ontime+count_delayed)
status = (per_ontime, per_delay)

fig1 = plt.figure()
ax1 = fig1.add_axes([0,0,1,1])
ax1.set_ylabel('number of Flights')
ax1.set_title('status of Flight')
ax1.bar(objects,status, width= .5)

#plt.savefig('%delay.png', bbox_inches='tight')
#################################
#plotting % of flights delay with week days

Day_of_Week = data[['DAY_WEEK','Flight Status']]
Day_Del = Day_of_Week.loc[Day_of_Week['Flight Status'] == 'delayed']
total_delay = len(Day_Del)

dayHeader2 = pd.get_dummies(Day_Del['DAY_WEEK'])
sum_5 = dayHeader2.sum(axis=0)
sum_5 = sum_5.multiply(other= 100/total_delay)
 
objects = ('Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun')

fig2 = plt.figure()
ax2 = fig2.add_axes([0,0,1,1])
ax2.set_ylabel('Percentage of Flights Delayed')
ax2.set_title('Flight Delays By Day')
ax2.bar(objects,sum_5)
#plt.savefig('%delay_by_week.png', bbox_inches='tight')

##################################
#plotting % of flights delay with day of month

Day_of_Month = data[['DAY_OF_MONTH','Flight Status']]
Date_Del = Day_of_Month.loc[Day_of_Month['Flight Status'] == 'delayed']

total_delay = len(Day_Del)

per_day_Month = np.zeros(31)
objects = np.zeros(31) 
for i in range(31):
    per_day_Month[i] = len(Date_Del[Date_Del['DAY_OF_MONTH']== i+1]) 
    per_day_Month[i] = (per_day_Month[i]*100)/total_delay    
    objects[i] = i+1
fig3 = plt.figure()
ax3 = fig3.add_axes([0,0,1,1])
ax3.set_ylabel('Percentage of Flights Delayed')
ax3.set_title('Flight Delays By Month')
ax3.bar(objects, per_day_Month)
#plt.savefig('%delay_by_month.png', bbox_inches='tight')

############################################
#plotting % of flights delay wrt carriers

Carrier = data[['CARRIER','Flight Status']]
Carrier_del = Carrier.loc[Carrier['Flight Status'] == 'delayed']
  
carrierHeader2 = pd.get_dummies(Carrier_del['CARRIER'])
sum_2 = carrierHeader2.sum(axis=0)
sum_2 = sum_2.multiply(other= 100/total_delay)

objects = ('CO','DH','DL','MQ','OH','RU','UA','US')

fig4 = plt.figure()
ax4 = fig4.add_axes([0,0,1,1])
ax4.set_ylabel('number of Flights Delayed')
ax4.set_title('Flight Delays By Carrier')
ax4.bar(objects, sum_2)
#plt.savefig('%delay_by_carrier.png', bbox_inches='tight')

##############################################
#plotting % of flights delay wrt weather

Weather = data[['Weather','Flight Status']]
Weather_del = Weather.loc[Weather['Flight Status'] == 'delayed']
  
weatherHeader2 = pd.get_dummies(Weather_del['Weather'])
sum_3 = weatherHeader2.sum(axis=0)
sum_3 = sum_3.multiply(other= 100/total_delay)

objects = ('bad','good')

fig5 = plt.figure()
ax5 = fig5.add_axes([0,0,1,1])
ax5.set_ylabel('Number of Flights Delayed')
ax5.set_title('Flight Delays By Weather')
ax5.bar(objects, sum_3,width = .5)
#plt.savefig('%delay_by_weather.png', bbox_inches='tight')

##############################################
#plotting % of flights delay wrt destination

DEST= data[['DEST','Flight Status']]
dest_del = DEST.loc[DEST['Flight Status'] == 'delayed']
  
destHeader2 = pd.get_dummies(dest_del['DEST'])
sum_4 = destHeader2.sum(axis=0)
objects = ('EWR','JFK','LGR')

sum_4 = sum_4.multiply(other= 100/total_delay)

fig6 = plt.figure()
ax6 = fig6.add_axes([0,0,1,1])
ax6.set_ylabel('Number of Flights Delayed')
ax6.set_title('Flight Delays By Destination')
ax6.bar(objects, sum_4)
#plt.savefig('%delay_by_destination.png', bbox_inches='tight')

##############################################
#plotting % of flights delay wrt origin

ORIGIN = data[['ORIGIN','Flight Status']]
ORIGIN_del = ORIGIN.loc[ORIGIN['Flight Status'] == 'delayed']
  
ORIGINHeader2 = pd.get_dummies(ORIGIN_del['ORIGIN'])
sum_6 = ORIGINHeader2.sum(axis=0)
objects = ('BWI','DCA','IAD')

sum_6 = sum_6.multiply(other= 100/total_delay)

fig7 = plt.figure()
ax7 = fig7.add_axes([0,0,1,1])
ax7.set_ylabel('Percentage of Flights Delayed')
ax7.set_title('Flight Delays By Origin')
ax7.bar(objects, sum_6)
#plt.savefig('%delay_by_origin.png', bbox_inches='tight')

##############################################
#plotting % of flights delay wrt crs_dept_time

crsdept = data[['CRS_DEP_TIME','Flight Status']]
crsdept_del = crsdept.loc[crsdept['Flight Status'] == 'delayed']
crsdept_del = crsdept_del.drop(['Flight Status'],axis=1)
crs_del = crsdept_del['CRS_DEP_TIME'].to_numpy()
crs_del = np.sort(crs_del)

num_delay = []
time_of_delay = []
time_of_delay.append(crs_del[0])
num_delay.append(1)
unique = True

for i in range(len(crs_del)):
    unique = True
    for j in range(len(time_of_delay)):
        if(crs_del[i] == time_of_delay[j]):
            num_delay[j] = num_delay[j]+1
            unique = False
            break
        #else:
           # time_of_delay.append(crs_del[])
    if(unique == True):
        time_of_delay.append(crs_del[i])
        num_delay.append(1)
        
fig8 = plt.figure()
ax8 = fig8.add_axes([0,0,1,1])
ax8.set_ylabel('Number of Flights Delayed')
ax8.set_title('Flight Delays By CRS Dept time')
ax8.plot(time_of_delay, num_delay)
#plt.savefig('%delay_by_crs_dept_time.png', bbox_inches='tight')

##############################################
#plotting % of flights delay wrt dept_time

ddept = data[['DEP_TIME','Flight Status']]
ddept_del = ddept.loc[ddept['Flight Status'] == 'delayed']
ddept_del = ddept_del.drop(['Flight Status'],axis=1)
ddept_del = ddept_del['DEP_TIME'].to_numpy()
ddept_del = np.sort(ddept_del)

num_delay2 = []
time_of_delay2 = []
time_of_delay2.append(ddept_del[0])
num_delay2.append(1)
unique = True

for i in range(len(ddept_del)):
    unique = True
    for j in range(len(time_of_delay2)):
        if(ddept_del[i] == time_of_delay2[j]):
            num_delay2[j] = num_delay2[j]+1
            unique = False
            break
    if(unique == True):
        time_of_delay2.append(ddept_del[i])
        num_delay2.append(1)

fig10 = plt.figure()
ax10 = fig10.add_axes([0,0,1,1])
ax10.set_ylabel('Number of Flights Delayed')
ax10.set_title('Flight Delays By Dept time')
ax10.plot(time_of_delay2, num_delay2)
#plt.savefig('%delay_by__dept_time.png', bbox_inches='tight')

##############################################
#plotting % of flights delay wrt distance

dist = data[['DISTANCE','Flight Status']]
dist_del = dist.loc[dist['Flight Status'] == 'delayed']
dist_del = dist_del.drop(['Flight Status'],axis=1)
dist_del = dist_del['DISTANCE'].to_numpy()
dist_del = np.sort(dist_del)

num_delay2 = []
time_of_delay2 = []
time_of_delay2.append(dist_del[0])
num_delay2.append(1)
unique = True

for i in range(len(dist_del)):
    unique = True
    for j in range(len(time_of_delay2)):
        if(dist_del[i] == time_of_delay2[j]):
            num_delay2[j] = num_delay2[j]+1
            unique = False
            break
        #else:
           # time_of_delay.append(crs_del[])
    if(unique == True):
        time_of_delay2.append(dist_del[i])
        num_delay2.append(1)

fig10 = plt.figure()
ax10 = fig10.add_axes([0,0,1,1])
ax10.set_ylabel('Number of Flights Delayed')
ax10.set_title('Flight Delays By Dept time')
ax10.plot(time_of_delay2, num_delay2)
#plt.savefig('%delay_by_distance.png', bbox_inches='tight')