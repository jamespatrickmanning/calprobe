# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 18:09:07 2021
Routine to process and plot calibration check using new "Fluke reference thermometer"
@author: James.manning
"""
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta as td
from datetime import datetime as dt
import glob
import numpy as np

#dt1=dt(2021,4,27,17,30) # GMT startime to compare
#dt2=dt(2021,4,27,18,30)  # endtime
#dt1=dt(2022,4,7,18,40) # GMT startime to compare
#dt2=dt(2022,4,7,20,12)  # endtime
#dt1=dt(2023,4,11,18,23) # GMT startime to compare
dt1=dt(2023,4,11,19,0) # GMT startime to compare w/time for pump to work
dt2=dt(2023,4,12,3,0)  # endtime
datadir=''  # data directory

# Read in VEMCO Miniloag data
count=0
for file in glob.glob(datadir+"Minilog*.csv"):
  #print(file)
  if file[13:19] not in ['356041','356015','356022']:  
    count=count+1
    if count==1:
        #dfv=pd.read_csv(file,skiprows=7,header=None,names=['date', 'time', 'temp'],encoding= 'unicode_escape')
        dfv=pd.read_csv(file,skiprows=8,header=None,names=['date', 'time', 'temp'],encoding='ISO-8859-1')
        dfv['sn']=file[13:19]#file[25:29]#[15:19]
        #dfv['dtime']=pd.to_datetime(dfv['date']+' '+dfv['time'])#+td(hours=4)# added 4 hours to get UTC
        dfv['dtime']=pd.to_datetime(dfv['date']+' '+dfv['time'])+td(hours=5)
        dfv.set_index('dtime')
    else:
        #if (file[15:19]!='8787') & (file[15:19]!='8788'):
            dfv1=pd.read_csv(file,skiprows=8,header=None,names=['date', 'time', 'temp'],encoding= 'ISO-8859-1')
            dfv1['sn']=file[13:19]#file[25:29]#15:19]
            dfv1['dtime']=pd.to_datetime(dfv1['date']+' '+dfv1['time'])+td(hours=5)#+td(hours=4)
            dfv1.set_index('dtime')
            print(file[13:19]+' '+str(dfv1[(dfv1['dtime']>dt1) & (dfv1['dtime']<dt2)]['temp'].mean()))
            frames=[dfv,dfv1]
            dfv=pd.concat(frames,sort=False)

# Read in Onset data
count=0
for file in glob.glob(datadir+"Test*.xlsx"):
    count=count+1
    if count==1:
        dfo=pd.read_excel(file,skiprows=1,header=None,names=['id','date_time', 'temp'])#,encoding='ISO-8859-1')
        dfo['sn']=str(count)#file[25:29]#[15:19]
        dfo['dtime']=pd.to_datetime(dfo['date_time'])+td(hours=4)
        dfo.set_index('dtime')
    else:
        dfo1=pd.read_excel(file,skiprows=1,header=None,names=['id','date_time', 'temp'])#,encoding= 'ISO-8859-1')
        dfo1['sn']=str(count)#file[25:29]#15:19]
        dfo1['dtime']=pd.to_datetime(dfo1['date_time'])+td(hours=4)#+td(hours=4)
        dfo1.set_index('dtime')
        print(str(count)+' '+str(dfo1[(dfo1['dtime']>dt1) & (dfo1['dtime']<dt2)]['temp'].mean()))
        frames=[dfo,dfo1]
        dfo=pd.concat(frames,sort=False)

# Read in Lowell Data
#dfl=pd.read_csv(datadir+'lowell_Temperature.csv')#,skiprows=8) #2022 case
dfl=pd.read_csv(datadir+'li_7ae6_20230412_152458.csv',skiprows=8)
#dfl['dtime']=pd.to_datetime(dfl['ISO 8601 Time'])
dfl['dtime']=pd.to_datetime(dfl['datet(GMT)'])
dfl.set_index('dtime')
dfl=dfl[dfl['dtime']>dt1]
dfl=dfl[dfl['dtime']<dt2]

# read in FLUKE readings
dff=pd.read_csv(datadir+'apr23_calprobe_fluke.csv')
#dff['date']='04/07/2022'
#2021 case dff['dtime']=pd.to_datetime(dff['date'] + ' ' + dff['UTC'])+td(hours=4)+td(minutes=5)
#2022 case dff['dtime']=pd.to_datetime(dff['date'] + ' ' + dff['UTC'])
dff['dtime']=pd.to_datetime(dff['date'] + ' ' + dff['local'])+td(hours=5)
dff.set_index('dtime')
dff.rename(columns={'Fluke':'Temp'},inplace=True)

# Calculate means at particular time ranges

mv=dfv[(dfv['dtime']>dt1) & (dfv['dtime']<dt2)]['temp'].mean()
#mo=dfo[(dfo['dtime']>dt1) & (dfo['dtime']<dt2)]['temp'].mean()
mf=dff[(dff['dtime']>dt1) & (dff['dtime']<dt2)]['Temp'].mean()
ml=dfl[(dfl['dtime']>dt1) & (dfl['dtime']<dt2)]['Temperature (C)'].mean()
mo=dfo[(dfo['dtime']>dt1) & (dfo['dtime']<dt2)]['temp'].mean()
print("VEMCO="+"{0:.2f}".format(mv)+"\nFluke="+"{0:.2f}".format(mf)+"\nLowell="+"{0:.2f}".format(ml)+"\nOnset="+"{0:.2f}".format(mo))


fig, ax = plt.subplots(figsize=(12,10))
for k in list(set(dfv['sn'])):
    dfv1=dfv[dfv['sn']==k]
    ax.plot(dfv1['dtime'],dfv1['temp'],linewidth=3,label=k)# plot VEMCO
for k in list(set(dfo['sn'])):
    dfo1=dfo[dfo['sn']==k]
    ax.plot(dfo1['dtime'],dfo1['temp'],linewidth=3,label=k)# plot VEMCO
ax.plot(dfl['dtime'],dfl['Temperature (C)'],linewidth=3,label='Lowell')    
ax.plot(dff['dtime'],dff['Temp'],linestyle='--',linewidth=3,label='Fluke') #plot Fluke
for jj in range(len(dff)):
    if type(dff.modification.values[jj])==str:  
        #print(dff.modification.values[jj])
        ax.text(dff.dtime.values[jj],7.,dff.modification.values[jj],size=12,fontweight='bold',horizontalalignment='center',rotation=90)
ax.text(dt2-td(.1),3.,"MEAN VALUES:\nVemco="+"{0:.2f}".format(mv)+"\nFluke="+"{0:.2f}".format(mf)+"\nLowell="+"{0:.2f}".format(ml)+"\nOnset="+"{0:.2f}".format(mo),size=16,fontweight='bold')
ax.set_xlim([dt1,dt2])
ax.set_ylim([min(dff['Temp'])-.5,12.])#max(dff['Temp'])+.5])
#plt.legend( title='SN', bbox_to_anchor=(1.1, 1), loc='upper right')
#plt.legend(title='SN', bbox_to_anchor=(.3, 1))#, loc='upper right')
plt.legend(title='SN', loc='best')
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.set(ylabel='degC',xlabel='11-12 April 2023 (UTC)')
ax.yaxis.get_label().set_fontsize(16)

#ax.set_title('Ice-Bath Calibration/Comparison of Fluke, Vemco (4-digit), Onset (3-digit), and Lowell Probes')
ax.set_title('Ice-Bath Calibration/Comparison of Fluke, Vemco (6-digit), Onset (1-digit), and Lowell Probe',fontsize=14)
fig.savefig('calprobe_with_fluke_apr2023.png')

