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
st.title('Stiff Diagram App')

st.write('The following data has been imported from Data.csv in meq/L')
obs=pd.read_csv("TWDB_MPGCD_WQs_Clipped.csv")
obs

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
st.sidebar.write('Which station would you like to plot a Stiff Diagram for:')
c=sns.color_palette("colorblind", len(obs))
    
if st.sidebar.checkbox('MPGCD Well'):
    mpgcd_obs=obs[obs.Source=='MPGCD']
    option = st.sidebar.selectbox(
    'MPGCD Well:',
    mpgcd_obs['Station'])
    obs=mpgcd_obs[mpgcd_obs.Station==option]
    nosamples = len(obs) # # number samples
    ncol = 1 # number of columns of subplot
    nrow = 1 #
    print_ID=option
elif st.sidebar.checkbox('TWDB Well'):
    twdb_obs=obs[obs.Source=='TWDB']
    option = st.sidebar.selectbox(
    'TWDB Well:',
    twdb_obs['Station'])
    obs=twdb_obs[twdb_obs.Station==option]
    nosamples = len(obs) # # number samples
    ncol = 1 # number of columns of subplot
    nrow = 1 #
    print_ID=option
try:
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
        h1=plt.fill(x, y, c=c[ind],alpha=0.35)
        plt.plot([0,0], [1,3],'--w')
        plt.title(obs['Station'].iloc[sID])
        
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
    #outputs and saves the diagram
    if st.checkbox('Save figure to computer'):
        plt.savefig("Stiff_Diagrams"+ "_" + print_ID +".png",dpi=350,bbox_inches='tight')

except NameError:
    st.write('')

st.write('Thanks for using the Stiff Diagram App!')