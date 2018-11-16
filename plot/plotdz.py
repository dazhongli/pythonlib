## last modified by Dazhong

from geopandas import gpd
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import datetime
import warning

__author__ = 'Dazhong Li'
__version__= '1.0'

def convert_timestamp(x):
    '''
    This fucntion is to convert a pandas timestamp to actual timestamp and ignore
    the error. It is
    '''
    warning.warn('convert_timestamp is deprecated, please use the pandas \
                 timestamp directly')
    try:
        return x.timestamp()
    except:
        pass

def plot_gdf(gdf,fig = False,filename='Test',column_plot = False, label = False,
             labelsize=4,**kwargs):
    '''
    This function is an extension of the geopandas's plot function and could plot
    labels and works on dates
    Parameters:
        gdf: - a geopandas object that holds the data
        fig: - pass the pointer to the figure object
        filename - name of the file to be ouput
        column_plot - the columns to be plotted
        label - label of the mnarker
        labelsize
    Return:
        tuple (fig, ax)
    '''
    if fig == False:
        fig = plt.figure(figsize=(16.53,11)) # we do A3 plot
        ax = fig.add_subplot(111)
    else:
        ax = fig.get_axes()[0]
    ax.set_aspect('equal')
    ax.set_xlabel('Easting')
    ax.set_ylabel('Northing')
    if column_plot != False:
        #import pdb
        #pdb.set_trace()
        vmin = gdf[column_plot].min()
        vmax = gdf[column_plot].max()
        cax = fig.add_axes([0.9,0.1,0.03,0.8])
        sm = plt.cm.ScalarMappable(cmap ='gnuplot2_r',norm=plt.Normalize(vmin=vmin,vmax=vmax))
        sm._A=[]
        cbar =  fig.colorbar(sm,cax=cax)
        time_delta = np.timedelta64(1,'D')*30.5/np.timedelta64(1,'s')*3 # we use 3 month as the tick
        #import pdb
        #pdb.set_trace()
        i, ticks = 1,[cbar.vmin]
        while ticks[-1] <cbar.vmax:
           ticks.append(cbar.vmin+time_delta*i)
           i = i+1
        cbar.set_ticks(ticks)
        cbar.set_ticklabels([datetime.datetime.fromtimestamp(t).strftime('%d-%b-%Y') for t in ticks])
        print(cbar.vmin)
        gdf.plot(ax=ax,column=column_plot,**kwargs)
        fig.suptitle(filename)
    else:
        gdf.plot(**kwargs,ax=ax)

    if label!=False:
        gdf['coords'] = gdf.centroid
        for index,row in gdf.iterrows():
            ax.annotate(s=str(row[label]),xy=(row['coords'].x,
                                              row['coords'].y)
                                              ,horizontalalignment='center',
                        size=labelsize)
    return fig, ax

