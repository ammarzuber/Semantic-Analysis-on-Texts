#!/usr/bin/env python
# coding: utf-8

# In[81]:


import numpy 
import pandas as pd
import matplotlib.pyplot as plt


# In[82]:


position = pd.read_csv('data/31158_positions.csv')  # read csv file
fuel = pd.read_csv('data/31158_fuels.csv')  
position['tracked_at'] = pd.to_datetime(position['tracked_at'], errors='coerce')
fuel['tracked_at'] = pd.to_datetime(fuel['tracked_at'], errors='coerce')
position['speed'] = position['speed']* 1.852  # change speed into km/h


position = position.dropna(subset=['fuel_percentage'])   # remove null fuel percentage


timeframe = position[(position['tracked_at']>='2019-12-07 00:00:00')& (position['tracked_at']<='2019-12-07 23:00:00')]  # set time frame 


timeframe['fuel_used'] = (timeframe['distance']/1400)  # fuel efficiency 1.4km per percentage loss.




ok = {'Measurement':[],'Predictive_Measurement':[], 'tracked_at':[],'fuel_used':[],'old_state':[],'new_state':[]} # dataframe to store predicted measurements
ok = pd.DataFrame(ok)0
initial_state = 50                              # initial percentage of fuel / rough estimate of starting fuel before using kf (does not have to be accurate)
initial_errorv = 10000                          # variance error in the starting.
q = 0.001  
measurement_uncertainty = 10                    # estimate range of error

def kalman_filter(initial_state, initial_errorv, q,measurement_uncertainty,data):
    global ok
    #prediction
    current_state = initial_state
    estimate_uncertainty = initial_errorv + q 
    
    for row , row in data.iterrows():                                                      
        kalman_gain = estimate_uncertainty/(estimate_uncertainty+measurement_uncertainty)  # calculating the kalman gain
        new_estimate = current_state  +  kalman_gain*(row['fuel_percentage']-current_state)  # insert current fuel percentage 
        
        old_state = current_state
        
        new_uncertainty = (1-kalman_gain)*estimate_uncertainty
        current_state = new_estimate - row['fuel_used']
        estimate_uncertainty = new_uncertainty
        
        
       
        
        
        ok_row = pd.Series({"Measurement":row['fuel_percentage'],"Predictive_Measurement":new_estimate,"tracked_at":row['tracked_at'],"fuel_used":row['fuel_used'],"old_state":old_state,"new_state":current_state}) # store the new collected data into the dataframe
        ok= ok.append(ok_row,ignore_index=True)


        if refueling_detect(ok_row) =='changing':       
            current_state = initial_state
            estimate_uncertainty = initial_errorv + q
            measurement_uncertainty = 50
            
        if refueling_detect(ok_row) =='refueling':
            current_state = ok_row['Measurement']
            estimate_uncertainty = initial_errorv + q
            measurement_uncertainty = 50
            
        if refueling_detect(ok_row) =='siphoning':
            current_state = ok_row['Measurement']
            estimate_uncertainty = initial_errorv + q
            measurement_uncertainty = 50
        #print(kalman_gain)
        #print(new_estimate)
        
        
    

def refueling_detect (data):  # function to detect whether to algorithm is too far away from the measurement, therefore reset the algorithm
    diff = data['Predictive_Measurement'] - data['Measurement']
    if (diff>=10):
        return 'changing'
     
    if (diff<=-10):
        return 'changing'
    
    if (diff>=30):
        return 'refueling'
    
    if (diff<=-30):
        return 'siphoning'

    
        
    


kalman_filter(initial_state,initial_errorv,q,measurement_uncertainty,timeframe)  # call the function


# plot the measurement
plt.figure(figsize=(20,9))
plt.plot( 'tracked_at','Measurement', data=ok, markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4)


plt.plot('tracked_at' ,'Predictive_Measurement',  data=ok, color='olive', linewidth=2)

plt.legend()

