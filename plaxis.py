# coding: utf-8

__version__= '1.0'
__author__ = 'DazhongLi'

import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import shapely.geometry as geo
from IPython.display import clear_output
from matplotlib.patches import Circle, Polygon
from matplotlib.collections import PatchCollection
from scipy.spatial import Voronoi, voronoi_plot_2d
import seaborn as sns
import sys
import os
sys.path.append(os.path.expanduser(r'~\OneDrive\05Research\00Codes\01Python\PythonLibrary'))
from dzgeometry import remove_close_points
sns.set_style("whitegrid")


title = {'Phase 2': 'Stage 2 - $\sigma^{\prime}_v$ with Fill Level at  +6.0mPD',
        'Phase 8' : 'Stage 1 - $\sigma^{\prime}_v$ with Fill Level at +2.25mPD',
        'Phase 9' : 'Stage 3 - $\sigma^{\prime}_v$ with Fill Level at +6.0mPD without cell',
        'Phase 9-2': '$\Delta\sigma^{\prime}_v$ from Stage 2 to Stage 3',
        'Phase 9-8': '$\Delta\sigma^{\prime}_v$ from Stage 1 to Stage 3'}

def main():
    os.chdir(r'Z:\Actual Job\211036\11-00 Calculations\11-02 Seawall Design\Cellular Cofferdam Plaxis\02 Construction\Plaxis 3D\Cell Arching\3D Data Porcessing')
    print('Data process working, please wait.....')
    #filepath = r'../K035/Output/Half Model/Rinter=0.65'
    filepath = r'../K035/Output/Half Model/Rinter = 0.65 for all'
    #filepath = r'../K035/Full model/Output'
    #filepath = r'../C108/Output/Rinter = 0.65'
    #filepath = r'../C083/Output/Rinter = 0.65'
    #filepath = r'../C083/Output/Rinter = 0.65 for all'
    #levels = [-8.51,-14.31,-20.11,-25.9]
    #levels = [-14.2,-18.2,-22.2,-24.8] #C083
    levels = [-6.8,-10.7,-14.6,-18.4]  #K035
    #levels = [-14.6]
    #levels = [-11.90, -18.50,-24.50,-30.70] #K108
    Phases = ['Phase 2', 'Phase 8', 'Phase 9', 'Phase 9-8', 'Phase 9-2'] 
    #Phases = ['Phase 2']
    #Phases = ['Phase 2', 'Phase 8', 'Phase 9']
    #read teh stone columns in
    #import pdb; pdb.set_trace()
    xy_sc = pd.read_excel(r'./Input/Stone Column Centre.xlsx',skiprows=6,parse_cols =[1,2])
    xy_sc.columns = ['x','y']
    geometry = [Point(xy) for xy in zip(xy_sc.x,xy_sc.y)]
    stone_column = gpd.GeoDataFrame(xy_sc,geometry = geometry)
    large_cell = read_cell(r'./Input/Large Cell.xlsx')
    small_cell = read_cell(r'./Input/Small Cell.xlsx')
    average_stress = {}
    for level in levels:
        for phase in Phases:
            mean,std = generate_pdf(filepath,level,phase,stone_column,large_cell,small_cell)
            average_stress[phase] = {level:mean}
            print('{:.2f}mPD '.format(level) + phase)
    #with open('result.txt','w') as f:
    #    for key, value in average_stress:
    #        f.write('{}'.format(key))
    #        for level,stress in value:
    #            f.write('{:.2f} {.2f}'.format(level,stress))

def generate_pdf(filepath,level,phasename,stone_column,large_cell,small_cell):
    figuretitle =title[phasename] + ' (z = {:.1f}mPD)'.format(level)
    figurename = phasename +' @{:.2f}mPD'.format(level)
    stress_gdf = read_stress_data(filepath,level,phasename)
    element_stress = get_element_stress(stress_gdf)
    soil_stress = get_soil_stresses(element_stress,stone_column)
    return plot_pdf(large_cell,small_cell,stone_column, soil_stress,
             figuretitle,filepath,figurename)

def read_stress_data(filepath,level,phasename):
    filename = 'Sigma_zz({:.2f}mPD).xlsx'.format(level)
    stress_df = pd.read_excel(os.path.join(filepath,filename),sheetname=phasename,
                            parse_cols= [0,1,2,3,5],skiprows = 1)
    stress_df.columns = ['material','nodeid','x','y','sz']
    stress_df.sz = -1*stress_df.sz
    geometry = [Point(xy) for xy in zip(stress_df.x,stress_df.y)]
    stress_gdf = gpd.GeoDataFrame(stress_df,geometry = geometry)
    #we want to make sure that the index starts with 1
    if stress_df.index[0] == 0:
        stress_df.index = stress_df.index + 1
    return stress_gdf

def get_element_stress(stress_gdf):
    count = 0
    element_stress = stress_gdf[stress_gdf.nodeid==2]
    for ix,row in element_stress.iterrows():
        start_ix = ix - 1
        if count + 1 >= len(element_stress.index):
            end_ix = element_stress.index[-1]
        else:
            end_ix = element_stress.index[count+1]-2
        count = count + 1
        # loop over the elelement and calculate average
        points_collection = stress_gdf.iloc[start_ix:end_ix,:]
        pts_array = []
        for east,north,column in zip(points_collection.geometry.x,
                                        points_collection.geometry.y,
                                        points_collection['sz']):
            pts_array.append([east,north,column])
        pts_array = np.array(pts_array)
        avg_x,avg_y = pts_array[:,0].mean(),pts_array[:,1].mean()
        average_pt = Point([avg_x,avg_y])
        average_column = pts_array[:,1].mean()
        row.geometry = average_pt
        row.sz = average_column
    return element_stress

#------------------get the soil element by comparing the stone columns----kk
def get_soil_stresses(element_stress_bar,stone_column,buffer=0.6):
    buffer = 0.6
    flag = []
    for ix, pt in zip(element_stress_bar.index,element_stress_bar.geometry):
        dist = stone_column.distance(pt).values
        mask = dist > buffer
        flag.append(np.all(mask))
    return element_stress_bar[flag]
#------------------------------------------------------
#draw the stone columns on the plot
def read_cell(filename):
    ##import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
    xy = pd.read_excel(filename, parse_cols=[2,3], skiprows=16)
    xy.dropna(inplace = True)
    xy.columns=['x','y']
    cell = geo.Polygon([[x,y] for x, y in zip(xy.x, xy.y)])
    return cell

def draw_geometry(large_cell, small_cell,stone_column,ax = False):
    #import ipdb; ipdb.set_trace()  # XXX BREAKPOINT
    if ax == False:
        figure = plt.figure(figsize=(20,10))
        ax = figure.add_subplot(111)
    radius = 0.5
    patches = []
    # draw the stone column
    for x,y in zip(stone_column.geometry.x, stone_column.geometry.y):
        circle = Circle((x, y), radius=radius)
        patches.append(circle)
    xy_large = np.array(large_cell)
    xy_small = np.array(small_cell)
    xy_large = [[x,y]for x,y in large_cell.exterior.coords]
    xy_small = [[x,y]for x,y in small_cell.exterior.coords]
    patches.append(Polygon(xy_small,True))
    patches.append(Polygon(xy_large,True))
    p = PatchCollection(patches, alpha=1,edgecolor='k',facecolor='None')
    ax.add_collection(p)
    return ax

def plot_pdf(large_cell, small_cell,stone_column,soil_stress,figuretitle,
             filepath,figurename):
    fig = plt.figure(figsize = (16.53,11.59))
    ax = fig.add_subplot(121)
    ax.set_aspect('equal')
    #import pdb; pdb.set_trace()
    soil_stress_cell = soil_stress[soil_stress.within(large_cell)|
                                   soil_stress.within(small_cell)]
    #-----------do the sampling -------------------------------------------------------------------------
    x = soil_stress_cell.geometry.x.values
    y = soil_stress_cell.geometry.y.values
    val = soil_stress_cell.sz.values
    xmin, xmax,ymin,ymax = 0,50,-50,50
    xi = np.linspace(xmin,xmax,100)
    yi = np.linspace(ymin,ymax,100)
    xx,yy = np.meshgrid(xi,yi)
    inter_val = griddata((x,y),val,(xx.flatten(),yy.flatten()),method = 'linear')
    geometry = [Point(xy) for xy in zip(xx.flatten(),yy.flatten())]
    soil_stress_cell = gpd.GeoDataFrame(dict(x=xx.flatten(),y=yy.flatten(),
                                             sz=inter_val),geometry = geometry)
    #soil_stress_cell = soil_stress_cell[soil_stress_cell.within(large_cell)|
    #                                    soil_stress_cell.within(small_cell)]
    soil_stress_cell = soil_stress_cell[soil_stress_cell.within(large_cell)|
                                        soil_stress_cell.within(small_cell)]

    #soil_stress_cell = soil_stress_cell[soil_stress_cell.y >=-7.5] #seaside
    #soil_stress_cell = soil_stress_cell[soil_stress_cell.y <-7.5] #Landside
    #----------------------------------------------------
    #soil_stree_in_large_cell.plot(ax = ax,edgecolor='k',vmin=0,vmax =200,column ='sz',s=300,cmap='gnuplot2',alpha=0.7)

    if soil_stress_cell.sz.max()<100:
        vmax = 100
    elif soil_stress_cell.sz.max()>250:
        vmax = 300
    else:
        vmax = 300
    sc = ax.scatter(x=soil_stress_cell.geometry.x,y=soil_stress_cell.geometry.y,
            c=soil_stress_cell.sz,cmap='gnuplot2_r',vmin=0,vmax=vmax,s =20,marker='s')
    ax.set_xlabel('x')
    ax.set_ylabel('y --> seaward')
    ax.set_ylim([-16,16])

    draw_geometry(large_cell,small_cell,stone_column,ax=ax)
    cbar = plt.colorbar(sc,fraction=0.064,pad=0.04)
    cbar.ax.set_ylabel('Vertical effective stresses $\sigma^{\prime}_v (kPa)$')
    fig.suptitle(figuretitle,fontsize=20,y=0.95)
    soil_stress_cell.sz.mean()
    ax2 = fig.add_subplot(122)
    soil_stress_cell.dropna(inplace=True)
    axes = sns.distplot(soil_stress_cell.sz,ax=ax2,color='b',rug=True,bins = 100)
    axes.set_xlim([0,vmax])
    ax2.set_xlabel(r'$\sigma^{\prime}_v$(kPa)')
    ax2.set_ylabel('Density')
    ax2.set_title(r'mean $\sigma^{\prime}_v$' +' = {:.1f}kPa with standard deviation ={:.2f}kPa'.format(soil_stress_cell.sz.mean(),
                                                                                soil_stress_cell.sz.std()))
    plt.subplots_adjust(left=0.1,wspace=0.3)
    fig.savefig(os.path.join(filepath,figurename +'.pdf'))
    #let's return the mean and the std
    return soil_stress_cell.sz.min(), soil_stress_cell.sz.std()

if __name__=='__main__':
    main()
