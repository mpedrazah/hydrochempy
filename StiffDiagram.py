# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 12:11:41 2021

@author: mpedrazas
"""

import streamlit as st
import numpy as np
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import os
import math
import seaborn as sns
import pandas as pd
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import FuncFormatter
#%%
#st.title('Plotting App')

#st.write('The following data has been imported from Data.csv in meq/L')

#%%water levels


#%%

# Change default settings for figures
# -------------------------------------------------------------------------------- #
mpl.rc('savefig', dpi = 330)
mpl.rc('xtick', labelsize = 14)
mpl.rc('ytick', labelsize = 14)
mpl.rc('font', size = 14)
mpl.rc('legend', fontsize = 14)

markersize = 12
linewidth = 2

def roundup(x):
    return int(math.ceil(x / 10.0)) * 10

#%%
aq_color_names={'Edwards-Trinity Plateau':'#69c97e','Edwards-Trinity':'#69c97e',
                   'Rustler':'#4fc4db','Capitan Reef Complex':'#a2b1b3','Capitan Limestone':'grey',
                   'Pecos Valley':'#e6b010','Dockum':'#c426c9','Other':'orange','Pecos Valley/Dockum':'pink',
                   'Pecos Valley/Edwards-Trinity Plateau':'yellow'}

tool = st.radio("Select Tool: ", ('Water Quality', 'Water Levels'))
if tool=='Water Quality':
    obs=pd.read_csv("TWDB_MPGCD_WQs_Clipped.csv")
    st.write('Which well would you like to plot a Stiff Diagram for:')
    if st.checkbox('MPGCD Well'):
        mpgcd_obs=obs[obs.Source=='MPGCD'].sort_values(by=['Station'])
        option = st.selectbox(
        'MPGCD Well:',
        mpgcd_obs['Station'])
        obs=mpgcd_obs[mpgcd_obs.Station==option]
        nosamples = len(obs) # # number samples
        ncol = 1 # number of columns of subplot
        nrow = 1 #
        print_ID=option
    elif st.checkbox('TWDB Well'):
        twdb_obs=obs[obs.Source=='TWDB'].sort_values(by=['Station'])
        option = st.selectbox(
        'TWDB Well:',
        twdb_obs['Station'])
        obs=twdb_obs[twdb_obs.Station==option]
        nosamples = len(obs) # # number samples
        ncol = 1 # number of columns of subplot
        nrow = 1 #
        print_ID=option
    try:
        
        obs_edit=obs[['Station','Aquifer','Date','Cl','HCO3','SO4','NaK','Ca','Mg','TDS','Source']]
        obs_edit.rename(columns={'Station' :'Well ID'},inplace=True)
        
        
        fig=plt.figure(figsize=(12,8))
        
        left_max=roundup(max([obs.NaK.max(),obs.Ca.max(),obs.Mg.max()]))
        right_max=roundup(max([obs.SO4.max(),obs.Cl.max(),obs.HCO3.max()]))
        
        if left_max >= right_max:
            max_val=left_max
        else:
            max_val=right_max
        
        for sID in range(0, nosamples):
                
            ind=obs.index[obs['Station'] == (obs['Station'].iloc[sID])].tolist()[0]
            plt.subplot(nrow,ncol,sID+1)
            # plt.hold(True)
            # define x coordinates of fill
            x=[-obs['NaK'].iloc[sID], -obs['Ca'].iloc[sID], -obs['Mg'].iloc[sID],obs['SO4'].iloc[sID] , obs['HCO3'].iloc[sID], obs['Cl'].iloc[sID], -obs['NaK'].iloc[sID]]
            y=[3,2,1,1,2,3,3]
        
            # Stiff plots with color depending on water type
            h1=plt.fill(x, y,c=aq_color_names[obs.Aquifer.loc[ind]], alpha=0.35)
            plt.plot([0,0], [1,3],'--w')
            plt.title('Well ID: ' + str(int(obs['Station'].iloc[sID])) + ' Aquifer: ' + obs['Aquifer'].iloc[sID] +'\n Collection Date: ' + str(obs['Date'].iloc[sID][0:10]))
            
            plt.tick_params(top='off', bottom='off', left='off', right='off', labelleft='on', labelright='on', labelbottom='on')
            minor_ticks = np.arange(-50, 50, 5)
          
            ax=plt.gca()
            ax.xaxis.set_major_locator(plt.MaxNLocator(7))
            ax.xaxis.set_minor_locator(plt.MaxNLocator(14)) 
            ax.grid(alpha=0.35, b=True, which='major',axis='both')
            ax.grid(b=True, which='minor', alpha=0.25, linestyle='--')
            
           
            if sID == len(obs)-1:
                plt.xlabel('(meq/L)')
        
            plt.ylim(0.8, 3.2)
        
            ax.yaxis.set_label_position("left")
            plt.yticks([3,2,1],{'Mg','Ca','Na+K'})
            plt.xlim([-35,35])
            #plt.xlim([-max_val,max_val])
            ax2 = ax.twinx()
            #ax2.yaxis.set_label_position("right")
            # ax2.yaxis.tick_right()
            
            plt.ylim(-0.1,1.1)
            ax2.set_yticks([0.5,0,1])
            ax2.set_yticklabels({r'$HCO_{3}$',r'$SO_{4}$','Cl'})
        
            # for spine in plt.gca().spines.values():
            #     spine.set_visible(False)
        
        # adjust position subplots
        plt.subplots_adjust(left=0.1, bottom=0.2, right=1, top=0.95, wspace=0.35, hspace=0.40)
        plt.tight_layout()  
        st.pyplot(fig)
        obs_edit
        #outputs and saves the diagram
        #if st.checkbox('Save figure to computer'):
         #   plt.savefig("Stiff_Diagrams"+ "_" + print_ID +".png",dpi=350,bbox_inches='tight')

    except NameError:
        st.write('')
    
    
elif tool=='Water Levels':
    wl_wells=pd.read_csv("TWDB_MPGCD_WLs_Clipped.csv")
    twdb_wl=pd.read_csv('WaterLevelsByCounty.csv')
    twdb_wl['MeasurementDate'] = pd.to_datetime(twdb_wl.Date, dayfirst=False)
    twdb_wl.StateWellNumber=twdb_wl.StateWellNumber.astype(dtype='int32')
    wl=pd.read_csv("WaterLevel_FOIA.csv")
    wl.MeasurementDate=pd.to_datetime(wl.MeasurementDate)
    st.write('Which well would you like to plot a Hydrograph for:')
    if st.checkbox('MPGCD Well'):
        mpgcd_obs=wl_wells[wl_wells.Source=='MPGCD'].sort_values(by=['DistrictId'])
        option = st.selectbox(
        'MPGCD Well:',
        mpgcd_obs['DistrictId'])
        obs=mpgcd_obs[mpgcd_obs.DistrictId==option]
        dep=obs.WellDepth.iloc[0]
        wellname=option
        ownername=obs.OwnerName.iloc[0]
        if (dep)>0:
            depth=dep
        else:
            depth='NAN'
        wl_plot=wl[wl.WellId==obs.FID_.iloc[0]]
        fig=plt.figure(figsize=(9, 3))
        sns.set_style("darkgrid")
        elev=obs.Elevation.iloc[0]
        aq_name=obs.AquiferNam.iloc[0]
        plt.scatter(wl_plot.MeasurementDate,elev-wl_plot.FinalDepthToWaterFeet, c=aq_color_names[aq_name],alpha=0.7,label='Well ' + option[:-2] + '-' + aq_name + ' Depth ' +str(depth))
        plt.legend(ncol=2,bbox_to_anchor=(1, -0.3))
        plt.title('MPGD Well ID: ' + option[:-2] , fontsize=14)
        plt.ylabel('Water Elevation (ft amsl)',fontsize=14)
        plt.tick_params(labelsize=14)
        plt.xlabel('Year', fontsize=14)
        #plt.savefig('../Figures/WaterLevel_'+ str(wellname) +'.png', dpi=400,bbox_inches='tight')
        st.pyplot(fig)
        new=wl_plot[['MeasurementDate','FinalDepthToWaterFeet','MeasurementMethod','MeasurementAgency']]
        new['WaterElevation']=elev-new.FinalDepthToWaterFeet
        new
    elif st.checkbox('TWDB Well'):
        twdb_obs=wl_wells[wl_wells.Source=='TWDB'].sort_values(by=['StateWellN'])
        option = st.selectbox(
        'TWDB Well:',
        twdb_obs['StateWellN'])
        obs=twdb_obs[twdb_obs.StateWellN==option]
        wellname=option
        ownername=obs.OwnerName.iloc[0]
        wl_plot=twdb_wl[twdb_wl.StateWellNumber==int(option)]
        fig=plt.figure(figsize=(9, 3))
        sns.set_style("darkgrid")
        aq_name=obs.AquiferNam.iloc[0]
        depth2=obs.WellDepth.iloc[0]
        plt.scatter(wl_plot.MeasurementDate,wl_plot.WaterElevation, alpha=0.5,marker='s',c=aq_color_names[aq_name],label='Well ' + str(option) + '-' + aq_name+ ' Depth ' +str(depth2))
        plt.legend(ncol=2,bbox_to_anchor=(1, -0.3))
        plt.title('TWDB State Well Number: ' + str(wellname) , fontsize=14)
        plt.ylabel('Water Elevation (ft amsl)',fontsize=14)
        plt.tick_params(labelsize=14)
        plt.xlabel('Year', fontsize=14)
        #  plt.savefig('../Figures/WaterLevel_'+ str(wellname) +'.png', dpi=400,bbox_inches='tight')
        st.pyplot(fig)
        new=wl_plot[['MeasurementDate','WaterElevation','MeasuringAgency','MethodOfMeasurement']]
        new


#%%
