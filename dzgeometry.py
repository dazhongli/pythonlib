import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from shapely.geometry import Point

def remove_close_points(gdf, threshold,column = False,how='average'):
    '''
    return a copy of gdf where points close are removed
    parameters:
        gdf - geopandas data frame holding the geometries
        column - values of the points to be processed
        how - average
    '''
    count = 0
    nrows = gdf.shape[0]
    flag = [False for i in np.arange(nrows)]
    gdf_copy = gdf.copy()
    gdf_copy['flag'] = pd.Series(flag,index = gdf_copy.index)
    for ix,x,y,flag in zip(gdf_copy.index,
                           gdf_copy.geometry.x,
                           gdf_copy.geometry.y,
                           gdf_copy.flag):
        print('{0:.2f}%'.format(count/nrows*100),end='\r', flush=True)
        count = count + 1
        if gdf_copy.flag[ix] == True: #if the points have been checked, no need to do anything
            continue
        valid_copy = gdf_copy[gdf_copy.flag == False]
        points_collection = valid_copy[valid_copy.distance(Point(x,y))<threshold]
        # get collect all points here
        pts_array = []
        #import pdb; pdb.set_trace()
        for east,north,val in zip(points_collection.geometry.x,
                                     points_collection.geometry.y,
                                     points_collection[column]):
            pts_array.append([east,north,val])
        pts_array = np.array(pts_array)
        avg_x,avg_y = pts_array[:,0].mean(),pts_array[:,1].mean()
        average_pt = Point([avg_x,avg_y])
        if column!= False:
            average_column = pts_array[:,2].mean()
        for pt in points_collection.iterrows():
            gdf_copy.loc[pt[0],'geometry']=average_pt
            gdf_copy.loc[pt[0],'flag']= True
            if column!=False:
                gdf_copy.loc[pt[0],column]= average_column
        gdf_copy.loc[ix,'flag']=False #itself is not flagged for removal
    return gdf_copy

def convert_timestamp(x):
    try:
        return x.timestamp()
    except:
        pass

def plot_gdf(gdf,fig = False,filename='Test',column_plot = False, label = False,
             labelsize=4,**kwargs):
    '''

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

