# -*- coding: utf-8 -*-
"""
Created on Sat May 23 22:43:59 2020

@author: zchen
"""

import numpy as np
import pandas as pd 
import os
import shutil

# read high water level peaks
HW = pd.read_csv("stormtide_HWp_1920_2019.csv",header=0,index_col=None)
HW.columns= ['hwt','hw']
HW['hwt']= pd.to_datetime(HW['hwt'])


# Aprproximate SLR from 1992 (mid point of 1983-2001) to 2020
sealevelrise =  -0.0896

# datum offset between NAVD88 and MSL at the Battery
datumoffset = 0.063

HW.hw = HW.hw - datumoffset - sealevelrise 

# Gate closure trigger water level
floodlevel=[]
# Number of Gate closure events
events=[]

# Exceedance frequency (frequency for the flood events equal or greater than N semidiurnal tide cycles) for flood events with various durationsfor flood events with various durations (ranging from 1 semidiurnal tide cycle to 10 semidiurnal tide cycles).
freq =[]  #Exceedance frequency for 1 semidiurnal tide duration OR # Gate closure frequnecy
dur2=[]
dur3=[]
dur4=[]
dur5=[]
dur6=[]
dur7=[]
dur8=[]
dur9=[]
dur10=[]
dur_max=[]


dur_freq = 'dur_freq/'
if not os.path.exists(dur_freq):
    os.makedirs(dur_freq)
else:
    shutil.rmtree(dur_freq)
    os.makedirs(dur_freq)
    
    
interannual_freq = 'interannual_freq/'
if not os.path.exists(interannual_freq):
    os.makedirs(interannual_freq)
else:
    shutil.rmtree(interannual_freq)
    os.makedirs(interannual_freq)

# Different Gate closure trigger water level OR Constant Gate closure trigger water level with different SLR
for thr in np.arange(2.64, -1.24,-0.01):
    tep = HW[HW.hw>=thr]
    

# Obtain gate closure duartion    
    indiv_stack = [tep.index[0]]
    t= []
    h = []
    tide_cyc = []
    peak_num = []
    
    for j in range(1,len(tep)):
        if tep.index[j] - indiv_stack[-1] ==1:
            indiv_stack.append(tep.index[j])
            
        else:
            
            
            tep_fra= tep.loc[indiv_stack[0]:indiv_stack[-1]]
            tep_n = tep.loc[indiv_stack[0]:indiv_stack[-1]]['hw'].idxmax()
            h.append(tep_fra.loc[tep_n]['hw'])
            t.append(tep_fra.loc[tep_n]['hwt'])
            tide_cyc.append(len(tep_fra))
            peak_num.append(indiv_stack.index(tep_n)+1)
            
            indiv_stack = [tep.index[j]]
            
    tep_fra= tep.loc[indiv_stack[0]:indiv_stack[-1]]
    tep_n = tep.loc[indiv_stack[0]:indiv_stack[-1]]['hw'].idxmax()
    h.append(tep_fra.loc[tep_n]['hw'])
    t.append(tep_fra.loc[tep_n]['hwt'])
    tide_cyc.append(len(tep_fra))
    peak_num.append(indiv_stack.index(tep_n)+1)    
    
    
    t =  (pd.to_datetime(np.asarray(t))).ravel()
    h =  (np.asarray(h)).ravel()
    tide_cyc =  (np.asarray(tide_cyc)).ravel()
    peak_num =  (np.asarray(peak_num)).ravel()
    
    all_table_thr = pd.DataFrame({'t' : t, 'h' : h, 'tide_cyc':tide_cyc, 'peak_num' : peak_num})
    all_table_thr.to_csv(dur_freq+str(thr)+'.csv')  




# Obtain gate closure interannual variability
    tep_table= all_table_thr
    yr= []
    num=[]

    tidecycle_table = tep
    tidecycle_num = []
    
    
    for index in range(1920,2020):  
                          
        index_min = str(index)+'-01-01 00:00:00'
        i_min=pd.to_datetime(index_min)
        index_max = str(index+1)+'-01-01 00:00:00'      
        i_max=pd.to_datetime(index_max) 
        extract = (tep_table.t>=i_min)&(tep_table.t<i_max)
        year_tep_table=tep_table[extract]  
        
        yr.append(index)
        num.append(len(year_tep_table))
        
	#
        year_tidecycle_table =tidecycle_table[(tidecycle_table.hwt>=i_min)&(tidecycle_table.hwt<i_max)] 
        tidecycle_num.append(len(year_tidecycle_table))


    yr =  (np.asarray(yr)).ravel()
    num =  (np.asarray(num)).ravel()
    #
    tidecycle_num =  (np.asarray(tidecycle_num)).ravel()
    #
    freq_table = pd.DataFrame({'year' : yr, 'num' : num , 'tidecycle_num' : tidecycle_num })
    freq_table.to_csv(interannual_freq + '/freq_'+str(thr)+'.csv') 
    


    floodlevel.append(thr)
    events.append(len(all_table_thr))
    freq.append(len(all_table_thr)/100)
    dur2.append(len(tide_cyc[tide_cyc>=2])/100)
    dur3.append(len(tide_cyc[tide_cyc>=3])/100)
    dur4.append(len(tide_cyc[tide_cyc>=4])/100)
    dur5.append(len(tide_cyc[tide_cyc>=5])/100)
    dur6.append(len(tide_cyc[tide_cyc>=6])/100)    
    dur7.append(len(tide_cyc[tide_cyc>=7])/100)
    dur8.append(len(tide_cyc[tide_cyc>=8])/100)
    dur9.append(len(tide_cyc[tide_cyc>=9])/100)
    dur10.append(len(tide_cyc[tide_cyc>=10])/100)
    #dur_max.append(tide_cyc.max())
    
    B=np.array([1])
    tide_cyc = np.append(tide_cyc,B)
    dur_max.append(tide_cyc.max())





#%%

floodlevel =  (np.asarray(floodlevel)).ravel()
events =  (np.asarray(events)).ravel()
freq =  (np.asarray(freq)).ravel()
dur2 =  (np.asarray(dur2)).ravel()
dur3 =  (np.asarray(dur3)).ravel()
dur4 =  (np.asarray(dur4)).ravel()
dur5 =  (np.asarray(dur5)).ravel()
dur6 =  (np.asarray(dur6)).ravel()
dur7 =  (np.asarray(dur7)).ravel()
dur8 =  (np.asarray(dur8)).ravel()
dur9 =  (np.asarray(dur9)).ravel()
dur10=  (np.asarray(dur10)).ravel()
dur_max =  (np.asarray(dur_max)).ravel()



all_table = pd.DataFrame({'floodlevel' : floodlevel, 'events' : events, 'freq':freq ,'dur2' : dur2, 'dur3':dur3  ,'dur4':dur4  ,'dur5':dur5  ,'dur6':dur6  ,'dur7':dur7  ,'dur8':dur8  ,'dur9':dur9  ,'dur10':dur10,'dur_max' : dur_max })
all_table.to_csv('summary_table.csv')  

