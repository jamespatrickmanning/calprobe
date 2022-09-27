# -*- coding: utf-8 -*-
"""
Created on Sep 29, 2021
Routine to process and plot calibration check in test tank
(Another routine processed using new "Fluke reference thermometer" called calprobe_with_fluke.py)
This generates both a time series plot and a temperature-depth profile.
@author: James.manning
"""
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from datetime import timedelta as td
from datetime import datetime as dt
import glob

dt1=dt(2021,9,28,17,50) #startime to compare
dt2=dt(2021,9,28,18,20)  # endtime
wowl_t='ambient_temperature' # which temp to use for WOWL

# Read in VEMCO Minilog data
count=0
for file in glob.glob("minilog_tank_test_2021*.csv"):
    #print(file)
    count=count+1
    if count==1:
        dfv=pd.read_csv(file,skiprows=8,header=None,names=['date', 'time', 'temp'])
        dfv['sn']=file[-8:-4]
        dfv['dtime']=pd.to_datetime(dfv['date']+' '+dfv['time'])+td(hours=4)# added 4 hours to get UTC
        dfv.set_index('dtime')
    else:
        #if (file[15:19]!='8787') & (file[15:19]!='8788'):
            dfv1=pd.read_csv(file,skiprows=8,header=None,names=['date', 'time', 'temp'])
            #dfv1['sn']=file[15:19]
            dfv1['sn']=file[-8:-4]
            dfv1['dtime']=pd.to_datetime(dfv1['date']+' '+dfv1['time'])+td(hours=4)
            dfv1.set_index('dtime')
            #print(file[15:19]+' '+str(dfv1[(dfv1['dtime']>dt1) & (dfv1['dtime']<dt2)]['temp'].mean()))
            frames=[dfv,dfv1]
            dfv=pd.concat(frames,sort=False)
dfv=dfv[dfv['dtime']>dt1]
dfv=dfv[dfv['dtime']<dt2] 
dfv=dfv[dfv['sn']=='3944']    # limiting in this test to one serial number       

# Read in Creare data
count=0
for file in glob.glob("wowl-data-2021-09-30T14*.csv"):
    #print(file)
    count=count+1
    if count==1:
        dfc=pd.read_csv(file)#,skiprows=8,header=None,names=['date', 'time', 'temp'])
        dfc['sn']=file[-8:-4]
        #dfc['dtime']=pd.to_datetime(dfc['date']+' '+dfc['time'])+td(hours=4)# added 4 hours to get UTC
        dtime=[]
        for j in range(len(dfc)):
            dtime.append(dt1+td(minutes=j))
        dfc['dtime']=dtime    
        dfc.set_index('dtime')
    else:
        #if (file[15:19]!='8787') & (file[15:19]!='8788'):
            dfc1=pd.read_csv(file)#,skiprows=8,header=None,names=['date', 'time', 'temp'])
            #dfc1['sn']=file[15:19]
            dfc1['sn']=file[-8:-4]
            #dfc1['dtime']=pd.to_datetime(dfc1['date']+' '+dfc1['time'])+td(hours=4)
            dtime=[]
            for j in range(len(dfc1)):
                dtime.append(dt1+td(minutes=j))
            dfc1['dtime']=dtime 
            dfc1.set_index('dtime')
            #print(file[15:19]+' '+str(dfc1[(dfc1['dtime']>dt1) & (dfc1['dtime']<dt2)]['temp'].mean()))
            frames=[dfc,dfc1]
            dfc=pd.concat(frames,sort=False)
dfc=dfc[dfc['dtime']>dt1]
dfc=dfc[dfc['dtime']<dt2] 
#dfc=dfc[dfc['sn']=='3944']    # limiting in this test to one serial number       

# Read in ONSET MX2204 data downloed from HoboLink
dfo=pd.read_csv('hobo_test_tank_2021_7037.csv',skiprows=3,header=None)
#dfo=dfo.iloc[:,:-13]# removes unnecessary columns
dfo['dtime']=pd.to_datetime(dfo[0])+td(hours=4)
dfo=dfo[dfo['dtime']>dt1]
dfo=dfo[dfo['dtime']<dt2]
dfo.set_index('dtime')


# Read in Aquatec
dfa=pd.read_csv('aquatec_test_tank_2021.csv',skiprows=21)
dfa.rename(columns={' degC    ':'degC',' bar    ':'bar'}, inplace=True)
dfa['dtime']=pd.to_datetime(dfa['datehour'])+td(hours=4) # where I have manually editted header line to read this
dfa.set_index('dtime')
dfa=dfa[dfa['dtime']>dt1]
dfa=dfa[dfa['dtime']<dt2]

# Read in MOANA
dfz=pd.read_csv('MOANA_test_tank_2021_0057_9.csv',skiprows=12)
dfz['dtime']=pd.to_datetime(dfz['Date']+' '+dfz['Time'])#+td(hours=4)
dfz.set_index('dtime')
#dfz=dfl[dfl['dtime']>dt1]
#dfz=dfl[dfl['dtime']<dt2]

'''
# Read in Lowell Data
dfl=pd.read_csv('li_750c_20210429_155000.csv',skiprows=8)
dfl['dtime']=pd.to_datetime(dfl['datet(GMT)'])
dfl.set_index('dtime')
dfl=dfl[dfl['dtime']>dt(2021,4,27,16,30,0)]
dfl=dfl[dfl['dtime']<dt(2021,4,27,21,0,0)]

# read in FLUKE readings
dff=pd.read_csv('apr21_calprobe_fluke_2.csv')
dff['date']='04/27/2021'
dff['dtime']=pd.to_datetime(dff['date'] + ' ' + dff['UTC'])+td(hours=4)+td(minutes=5)
dff.set_index('dtime')
dff.rename(columns={'Fluke':'Temp'},inplace=True)
'''

# Calculate means at particular time ranges

mv=dfv[(dfv['dtime']>dt1) & (dfv['dtime']<dt2)]['temp'].mean()# Vemco
mc=dfc[(dfc['dtime']>dt1) & (dfc['dtime']<dt2)][wowl_t].mean()# Creare
mo=dfo[(dfo['dtime']>dt1) & (dfo['dtime']<dt2)][1].mean()     # Onset
ma=dfa[(dfa['dtime']>dt1) & (dfa['dtime']<dt2)]['degC'].mean()# Aquatec
mz=dfz[(dfz['dtime']>dt1) & (dfz['dtime']<dt2)]['Temperature C'].mean()#ZebraTech
#mf=dff[(dff['dtime']>dt1) & (dff['dtime']<dt2)]['Temp'].mean()
#ml=dfl[(dfl['dtime']>dt1) & (dfl['dtime']<dt2)]['Temperature (C)'].mean()
#print("VEMCO="+"{0:.2f}".format(mv)+"\nFluke="+"{0:.2f}".format(mf)+"\nLowell="+"{0:.2f}".format(ml))
print("VEMCO="+"{0:.2f}".format(mv)+"\nCreare="+"{0:.2f}".format(mc)+"\nAquatec="+"{0:.2f}".format(ma)+"\nONSET="+"{0:.2f}".format(mo)+"\nMOANA="+"{0:.2f}".format(mz))


fig, ax = plt.subplots(figsize=(12,10))
for k in list(set(dfv['sn'])):
    dfv1=dfv[dfv['sn']==k]
    #ax.plot(dfv1['dtime'],dfv1['temp'],linewidth=3,label=k)# plot VEMCO
    ax.plot(dfv1['dtime'],dfv1['temp'],linewidth=3,label='Vemco_Minilog')# plot VEMCO
#ax.plot(dfc['dtime'],dfc['temperature_ntc'],linewidth=3,label='Creare_WOWL')    
ax.scatter(dfc['dtime'],dfc[wowl_t],label='Creare_WOWL')    
#for j in dfo.columns[2:10]:
ax.plot(dfo['dtime'],dfo[1],label='Onset_MX2204')   #plot ONSET
    #print(j[-3:]+' '+str(dfo[j].mean()))
#ax.plot(dfl['dtime'],dfl['Temperature (C)'],linewidth=3,label='Lowell')    
ax.plot(dfz['dtime'],dfz['Temperature C'],linewidth=3,label='Zebra_Tech_Moana')    
ax.plot(dfa['dtime'],dfa['degC'],linewidth=3,label='Aquatec_520')    
'''
ax.plot(dff['dtime'],dff['Temp'],linestyle='--',linewidth=3,label='Fluke') #plot Fluke
for jj in range(len(dff)):
    if type(dff.modification.values[jj])==str:  
        #print(dff.modification.values[jj])
        ax.text(dff.dtime.values[jj],12.,dff.modification.values[jj],size=16,horizontalalignment='center',rotation=90)
'''
plt.legend( title='Manufacturer_model', bbox_to_anchor=(.8, 1),fontsize=18, loc='upper right')
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
ax.set(ylabel='degC',xlabel='28 Sep 2021 (UTC)')
ax.set_title('Test Tank Comparison of Multiple Temperature Probes',fontsize=18)
fig.savefig('calprobe_test_tank_sep2021.png')

fig2, ax2 = plt.subplots(figsize=(12,10))
dt1p=dt(2021,9,28,18,15,30) #startime to compare
dt2p=dt(2021,9,28,18,18,30)  # endtime
dfa=dfa[dfa['dtime']>dt1p]
dfa=dfa[dfa['dtime']<dt2p]
dfz=dfz[dfz['dtime']>dt1p]
dfz=dfz[dfz['dtime']<dt2p]
ma=dfa[(dfa['dtime']>dt1p) & (dfa['dtime']<dt2p)]['degC'].mean()# Aquatec
mz=dfz[(dfz['dtime']>dt1p) & (dfz['dtime']<dt2p)]['Temperature C'].mean()#ZebraTech
ax2.plot(dfa['degC'],(dfa['bar']-.98)*-10,label='Aquatec_520')#'  mean='+'%0.2f' % ma)
ax2.scatter(dfa['degC'].values[0],(dfa['bar'].values[0]-.98)*-10,color='g',label='start')
ax2.plot(dfz['Temperature C'],dfz['Depth Decibar']*-1,label='ZebraTech_Moana')#' mean='+'%0.2f' % mz)
ax2.scatter(dfz['Temperature C'].values[0],dfz['Depth Decibar'].values[0]*-1,color='g',label='')
plt.legend( title='Manufacturer_model', bbox_to_anchor=(.4, 1),fontsize=18, loc='upper right')
ax2.set(xlabel='degC',ylabel='depth (meters)')
ax2.set_title('Temperature profiles',fontsize=18)
fig2.savefig('calprobe_test_tank_sep2021_profiles.png')
print("Moana="+"{0:.2f}".format(mz)+"\nAquatec="+"{0:.2f}".format(ma))
