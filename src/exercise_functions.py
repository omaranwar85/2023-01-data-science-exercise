# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 20:52:40 2023

@author: omar
"""


import os
import os.path
import glob
import pandas as pd
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.axes._axes import _log as matplotlib_axes_logger
from matplotlib.ticker import LinearLocator
from scipy import signal

################### Function to convert sting features in CSV files to floats or NaNs ################### 
def convert_to_NaN_if_not_float(val: str):
    try:
        return np.float64(val) 
    except:
        return np.nan


################### Function to clean CSV files and generate a CSV per month ################### 
################### Brief explaination provided in README #####
def clean_csv_files(months = [6,7,8,9]): # input is a list of month(s) for cleaning and conversion. By default all of the files will be cleaned
        
    year = "2022"
    for month in months:                # Loop thorough months
        
        
        # Format month number as a proper two digit string
        month = int(month)
        if(month<10 and month>0):
            month = "0"+str(month)
        elif(month<13 and month>9):
            month = str(month)
        else:
            print("Invalid month:", month)
            continue
        
        #Path for source csv files in database
        parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        CSV_month_path = os.path.join(parent_path, "data",year+"-"+month) 
        if(os.path.isdir(CSV_month_path) == False):
            print("Following directory does not exist: ",CSV_month_path)
            continue
        
        CSV_files = glob.glob(os.path.join(CSV_month_path, "*.csv")) # List of all the csv files in the folder
        print("Generating clean CSV for month:", month)
        
        
        new_CSV_path = os.path.join(parent_path, year+"-"+month+".csv") # Path for destination csv file
        
        dataframe_collection = []
        
        for file_name in CSV_files: #Loop through the files in a folder
              
            try:
                drop_rows = [] # List of Indexes of rows with NaN or invalid data to be dropped
                df = pd.read_csv(file_name,index_col=False, converters={'dspec_28': convert_to_NaN_if_not_float}, on_bad_lines=lambda x: x[:-1], engine='python')
                # 'on_bad_lines=lambda x: x[:-1]' trims the rows with more columns than the header. This is based on assumption that invalid data is at the end of row
                for k in range(df.shape[0]): # loop through all the 'observe_time' values to check for proper date/time, and a1_0 for any NaN rows
                    obs_time_integrity_check = df.iloc[k,0]
                    try:
                        a,b=obs_time_integrity_check.split(" ")
                    except Exception:
                        print("Ignoring data with incorrect obs time in file:",file_name, ", Row:",k)
                        drop_rows.append(k)
                        continue    
                    year_check,month_check,day = a.split("-")
                    if(year_check != year and month_check!= month):
                        print("Ignoring data with incorrect obs time in file:",file_name, ", Row:",k)
                        drop_rows.append(k)
                        continue
                    if(np.isnan(df.iloc[k,1])):
                        print("Ignoring row with NaN data in file:",file_name, ", Row:",k)
                        drop_rows.append(k)
                        continue
                if(len(drop_rows)<df.shape[0]):    
                    df=df.drop(drop_rows)
                    dataframe_collection.append(df) #A dataframe with all the rows with proper timestamp and feature data
            except pd.errors.ParserError:
                print("Ignoring following file because of parsing error: ",file_name)
                continue
        
        month_df = pd.concat(dataframe_collection, join='outer', axis=0, ignore_index =True)
        month_df = month_df.sort_values(by=['observe_time'])
        month_df = month_df.reset_index(drop=True) # A sorted datafram with all the data for a month and correct index
        month_df['keep'] = 'No' # An extra 'kee' column in the dataframe with a default 'No'
        time_stamps_counter=0
        
        for k in range(month_df.shape[0]): # Loop through the dataframe to search for data with required timestamps.
            if(k==0):
                ref_obs = year+"-"+month+"-01 01:00:00"  # first valid timestamp for this month
                ref_datetime_object = datetime.strptime(ref_obs, '%Y-%m-%d %H:%M:%S')
                final_stamp_object =  ref_datetime_object + relativedelta(months=1) # first valid timestamp for the next month (end limit)
                
                NaNDataFrame = pd.DataFrame(np.zeros([1, 702])*np.nan) # a row of NaNs
                NaNDataFrame.columns = month_df.columns # same column names as the month_df
                NaNDataFrame.at[0,'keep']= 'yes' # 'keep' for NaNs set to yes
                
            obs_time = month_df.iloc[k,0] # read observe_time
            date_time , junk = obs_time.split("+") # get rid of fraction of sec details
            datetime_object = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
            
            
            #print(ref_datetime_object,datetime_object)
            # For the following block, print statement summarize what is happening
            if(datetime_object == ref_datetime_object): 
                print(ref_datetime_object, "-> Exact timestamp match")
                month_df.at[k,'keep']= 'yes'
                time_stamps_counter+=1
                ref_datetime_object = ref_datetime_object + timedelta(hours=1)

            elif(datetime_object > ref_datetime_object):
                if(k>0 and datetime_object_prev == ref_datetime_object - timedelta(minutes=10)):
                    print(ref_datetime_object, "-> -10 min data")
                    month_df.at[k-1,'keep']= 'yes'
                    ref_datetime_string = ref_datetime_object.strftime("%Y-%m-%d %H:%M:%S")
                    month_df.at[k-1,'observe_time']= ref_datetime_string+"+00:00"
                    time_stamps_counter+=1
                    ref_datetime_object = ref_datetime_object + timedelta(hours=1)

                elif(k>0 and datetime_object == ref_datetime_object + timedelta(minutes=10)):
                    print(ref_datetime_object, "-> +10 min data")
                    month_df.at[k,'keep']= 'yes'
                    ref_datetime_string = ref_datetime_object.strftime("%Y-%m-%d %H:%M:%S")
                    month_df.at[k,'observe_time']= ref_datetime_string+"+00:00"
                    time_stamps_counter+=1
                    ref_datetime_object = ref_datetime_object + timedelta(hours=1)
                    
                else:
                    while(ref_datetime_object < (datetime_object- timedelta(minutes=10))):
                        print(ref_datetime_object, "-> NaN as required data not available")
                        ref_datetime_string = ref_datetime_object.strftime("%Y-%m-%d %H:%M:%S")
                        NaNDataFrame.at[0,'observe_time']= ref_datetime_string+"+00:00"
                        month_df = pd.concat([month_df,NaNDataFrame])#.reset_index(drop=True)
                        time_stamps_counter+=1
                        ref_datetime_object = ref_datetime_object + timedelta(hours=1)
                    
            datetime_object_prev = datetime_object
        
        # In case data is missing for the end of month, this will fill the rows with NaNs
        while(ref_datetime_object < final_stamp_object):
            print(ref_datetime_object, "-> NaN as required data not available")
            ref_datetime_string = ref_datetime_object.strftime("%Y-%m-%d %H:%M:%S")
            NaNDataFrame.at[0,'observe_time']= ref_datetime_string+"+00:00"
            month_df = pd.concat([month_df,NaNDataFrame])#.reset_index(drop=True)
            time_stamps_counter+=1
            ref_datetime_object = ref_datetime_object + timedelta(hours=1)
            #print("______________________________________C")
        
        print("Entries in the file for month", month, "->",time_stamps_counter)    
        print("__________________________________________________________")
        
        month_df = month_df.sort_values(by=['observe_time']) # Sort dataframe using observe_time
        month_df_final = month_df[month_df['keep'] == 'yes'].reset_index(drop=True).drop(['keep'], axis=1) # keep rows marked with 'Yes' and then drop the keep column
        
        
        if(os.path.exists(new_CSV_path)): # remove any existing final CSV for the month
            os.remove(new_CSV_path)
        
        month_df_final.to_csv(new_CSV_path,index=False,na_rep='NaN') #Write to CSV


################### Function to generate visulisations of desired month(s) (defaults to 6th month) ###################  
################### Brief explaination provided in README ##### 
def visulize_data(months = [6], filter_size=5):
    plt.close('all')
    
    # limit the filter size between 3 and 21
    if(filter_size<3):
        filter_size = 3
    elif (filter_size>21):
        filter_size = 21
        
    #Generate the 2-D filter matrix as per user specifications 
    filter_array=np.ones((filter_size,filter_size))*(1/(filter_size*filter_size))
        
    for month in months: # loop through month(s) to visulalize
        month = int(month)
        # format the month number as two difgit string
        if(month<10 and month>0):
            month = "0"+str(month)
        elif(month<13 and month>9):
            month = str(month)
        else:
            print("Invalid month:", month)
            continue
        
        # Configure path for new CSVs
        parent_path = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        new_CSV_path = os.path.join(parent_path, "2022-"+month+".csv")
        
        if(os.path.isfile(new_CSV_path) == False):
            print("Following file does not exist: ",new_CSV_path)
            continue
        

        print("Generating visulisations for month:",month)
        print("Filter size for 2D surface smoothing:",filter_size,"x",filter_size )
        
        
        matplotlib_axes_logger.setLevel('ERROR')
        # Configure CMAP
        cmap_range = range(0,100) 
        cmap=cm.rainbow(np.array(cmap_range))
        
        
        # Read the CSV fo the selected month
        df_all = pd.read_csv(new_CSV_path)     
        
        df_all = df_all.drop(['observe_time'], axis=1) # dropping the 'observe_time' column as we will be using day numbers (instead of hours) as ticks
        
        feature_names = ["a1","a2","b1","b2","hspec","dspec","sprspec"] # features in the data
        feature_offsets = [0,100,200,300,400,500,600] # starting index of subfeatures for each respective feature above
        
        for f in range(7): # loop through all 7 features
            feature_name = feature_names[f]
            feature_offset = feature_offsets[f]
            list_2D = []
            plt.figure()
            for kk in range(feature_offset,feature_offset+100,1): # loop through each subfeature in a feature for entire month
                col_name = feature_name+"_"+str(kk-feature_offset)
                list_temp=df_all[col_name].tolist()
                list_float=np.array(list_temp,dtype=float)     
                list_2D.append(list_float)   # a 2-D list of all the subfeatures for a feature for the surface plot later
                plot_range=np.arange(0, int(len(list_float)/24), (len(list_float)/24)/len(list_float))
                plt.plot(plot_range,list_float, c=cmap[kk-feature_offset], alpha=0.2) #2-D projection for this sub-feature on a shared plot
            
            # Labels for the 2D projection of sub features
            plt.title(feature_name+" data for month: "+month)    
            plt.xlabel("days")
            plt.tight_layout()
            plt.show
            
            list_2D = np.asarray(list_2D) # The unfiltered features for the entire month           
            list_2D_filtered = signal.convolve2d(list_2D, filter_array, boundary='symm', mode='same') #The Filtered features for the entire month  
                
            # Following block projects the unfiltered and filtered data for the selected feature as a interactive 3D surface
            fig, axs = plt.subplots(1,2,subplot_kw={"projection": "3d"})
            
            X = np.arange(0, (len(list_float)/24), (len(list_float)/24)/len(list_float))
            Y = np.arange(0, 100, 1)
            X, Y = np.meshgrid(X, Y)
            
            surf = axs[0].plot_surface(X, Y, list_2D, cmap=cm.coolwarm)#,linewidth=0, antialiased=False)
            axs[0].zaxis.set_major_locator(LinearLocator(10))
            axs[0].zaxis.set_major_formatter('{x:.02f}')
            axs[0].set_xlabel("days")
            axs[0].set_ylabel(feature_name+" features")
            plt.tight_layout()
            
            surf = axs[1].plot_surface(X, Y, list_2D_filtered, cmap=cm.coolwarm)#,linewidth=0, antialiased=False)
            axs[1].zaxis.set_major_locator(LinearLocator(10))
            axs[1].zaxis.set_major_formatter('{x:.02f}')
            
            axs[1].set_xlabel("days")
            axs[1].set_ylabel("Filtered "+feature_name+" features with size "+str(filter_size)+"x"+str(filter_size))
            plt.tight_layout()
            fig.suptitle('Month: '+month)
            fig.colorbar(surf, ax=axs.ravel().tolist(), shrink=0.5,location="bottom")
            
            plt.show()    

        print("Done.")
    
    