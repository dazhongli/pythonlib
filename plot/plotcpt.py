# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 16:56:05 2017
Modeified on 15 March 2018
    - yticks of the axis is changed to 1.0
    - minor bugs of the file name is fixed

@author: dz.li
"""

import os
from os.path import basename
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

def main():
    files_ags = []
    path = r'G:\Actual Job\211036\11-00 Calculations\11-02 Seawall Design\Post 2016 GI\02 Sections\CH 3260 P_E1 C07879\00-1 GI\From site\TMCLKL' 
    os.chdir(path)
    files = os.listdir('./')
    files_ags = [files[i] for i in np.arange(len(files)) if files[i].endswith('ags')]
    df = read_ags_file(files_ags)
    pdf_path = r"./"
    plot_cpt_data(df, pdf_path=pdf_path)

def plot_cpt_data(ags_df,Nkt=12,pdf_path=False):
    os.chdir(os.getcwd())
    pdf_file_name = '' # this the pdf file name we will use for the print out
    key = 'Data table:' #this is the key indicating the start of table
    df = pd.DataFrame()
    cwd = os.getcwd()
    for subdir, dirs, files in os.walk('./'):
        files_A00 = [files[i] for i in np.arange(len(files)) if files[i].endswith('A00')]
        for file in files_A00:
            test_name = os.path.splitext(file)[0]
            try:
                ground_level = float(ags_df.loc[test_name,'*HOLE_GL'])
            except:
                ground_level = float(input('The ground level of {}:'.format(test_name)))
            #print(pdf_file_name)
            with open(file) as f:
                for line in f:
                    if 'Date of testing' in line:
                        date_of_test=line.split(':')[1].strip()
                        date_of_test = datetime.strptime(date_of_test,'%d-%b-%Y')
                        pdf_file_name = test_name + '_' +date_of_test.strftime('%Y%m%d')
                        print(pdf_file_name)
                        f.close()
                        break
            data_file = test_name+'_PORE3XP.asc'
            with open(data_file) as f:
                for line_number,line in enumerate(f):
                    if key in line:
                        f.close()
                        break
                fig = plt.figure()
                fig.suptitle(pdf_file_name + ' (Nkt = 12)',fontsize=40)
                fig.set_size_inches(18.5, 30)
                ax = fig.add_subplot(121)
                ax2 = fig.add_subplot(122)
                df = pd.read_table(data_file,sep = '\s+', skiprows = line_number+1)
                df = df.drop(df.index[[0]]) # drop the first row ,which contains Unit
                df = df.astype(float,copy = True)
                # a temp function to reduce the ground level
                df.Depth = ground_level - df.Depth
                df = df.set_index(['Rec'])
                df.replace(r'\s+',np.nan, regex = True)
                df.dropna(subset=['Qnet'], how='all', inplace=True, axis=0)
                Cu = df.Qnet.apply(float)/Nkt*1000
                df['Cu']= Cu
                ax.plot(df['Cu'].tolist(),df['Depth'].tolist())
                ax.grid(True)
                ax2.plot(np.array(df['Pore']),df['Depth'].tolist())
                ax.set_xlim([-50,300])
                xstart,xend = ax.get_xlim()
                ystart,yend = ax.get_ylim()
                ax.xaxis.set_ticks(np.arange(-10,xend,20))
                ax.yaxis.set_ticks(np.arange(-35, 11.5, 2))
                ax2.set_ylim([-35,11.5])
                ax.set_ylim([-35,11.5])
                ax.set_yticks(np.arange(df.Depth.min(),df.Depth.max()+1,1.0))
                ax.set_xlabel('Cu (kPa)',fontsize=12)
                ax.set_ylabel('Elevation(mPD)',fontsize=12)
                ax2.set_xlabel('PWP(MPa)',fontsize=12)
                ax2.set_ylabel('Elevation(mpd)',fontsize=12)
                ax2.grid(True)
                pdf_file_name = pdf_file_name + '_' + '[{:.2f}mPD]'.format(df['Depth'].min()) +'.pdf'
                plt.savefig(os.path.join(pdf_path,pdf_file_name),format='pdf')
                df.to_excel(pdf_file_name.split('.')[0] +'.xlsx')
                #plt.show()

#this function read the ags files and return the basic information of the file
# return - return the combined dataframe generated with multiple ags files
# passed in
#as a Pandas data frame;
#filename - a list of files
def read_ags_file(file_names):
    line_key_upper = r'"**HOLE"'
    line_key_lower = r'"**DICT"'
    dfs = pd.DataFrame()
    for file_index, file_name in enumerate(file_names):
        upper_line_number = 0
        lower_line_number = 0
        with open(file_name) as f:
            for index,line in enumerate(f):
                if line_key_upper in line:
                    upper_line_number = index
                if line_key_lower in line:
                    lower_line_number = index
                    f.close()
                    break
        n_rows = lower_line_number - upper_line_number - 3
        df = pd.read_csv(file_name,skiprows=upper_line_number+1,nrows=n_rows)
        df.set_index(df.columns[0],inplace=True)
        df = df.drop(df.index[[0]])
        if file_index ==0:
            dfs = df
        else:
            dfs = dfs.append(df)
    dfs.to_excel('ags.xlsx')
    return dfs

if __name__ == '__main__':
    main()
