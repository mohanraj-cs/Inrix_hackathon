# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 16:17:22 2022

@author: HP
"""
import pandas as pd
import json
from pandas import json_normalize
from datetime import time, timedelta
from pathlib import Path 
import os



# df = pd.read_json(r"C:\Users\HP\Downloads\response (4).json")

def convert_datetime(dataframe, colname):
    
    dataframe[colname] = pd.to_datetime(dataframe[colname])
    
    return dataframe[colname]





def call_for_each_file(str_file_path_origin,str_file_path_destination, Petrolpump_index, str_longitude, str_latitiude):
    
    # str_file_path_origin = r""
    # str_file_path_destination = r""

    # print(pd.__version__)
    # print("******",str_file_path_origin, str_file_path_destination)

    df1_origin = pd.read_json(str_file_path_origin)
    df2_des = pd.read_json(str_file_path_destination)
    
    
    df1_origin['endDateTime'] = convert_datetime(df1_origin, 'endDateTime')
    df1_origin['startDateTime'] = convert_datetime(df1_origin, 'startDateTime')
    
    
    df1_origina = df1_origin.groupby(['deviceId'], sort=True)['endDateTime'].min().reset_index()
    
    # 3 destination end
    
   
    
    df2_des['endDateTime'] = convert_datetime(df2_des, 'endDateTime')
    df2_des['startDateTime'] = convert_datetime(df2_des, 'startDateTime')
    
    
    
    df2_desa = df2_des.groupby(['deviceId'], sort=True)['startDateTime'].max().reset_index()
    
    
    df3 = pd.merge(df1_origina,df2_desa,on = ['deviceId'], how = 'inner')
    
    
    # print("df3",len(df3))
    
    df3 = df3[df3['endDateTime'] > df3['startDateTime']]
    
    # print("df3 after comaprsioon",len(df3))
    
    df3['wait_time'] = (df3['endDateTime'] - df3['startDateTime']) /  pd.Timedelta(minutes=1)
    
    df3['Petrol_pump_address latitude'] = str_latitiude
    df3['Petrol_pump_address longitude'] = str_longitude
    df3['Petrol pump id'] = Petrolpump_index
    
    
    return df3
    
    # aa = df3[['endDateTime_y','startDateTime_x']]
    
    # list1 = list(df['deviceId'])
    
    # list2 = list(df1_origin['deviceId'])
    
    # filepath = Path('D:\Spyder codes\out1.csv')  
    # df_4 = df.head(1000)
    # df_4.to_csv(filepath)
    
    
    # list3 = list1 + list2
    
    # dd = pd.read_json('C:\Users\HP\Downloads\response.json', orient='index')
    
    # # Use json_normalize() to convert JSON to DataFrame
    # dict= json.loads(data)
    # df = json_normalize(dict['technologies']) 
    
    # # Convert JSON to DataFrame Using read_json()
    # df2_des = pd.read_json(jsonStr, orient ='index')
    
    # # Use pandas.DataFrame.from_dict() to Convert JSON to DataFrame
    # dict= json.loads(data)
    # df2_des = pd.DataFrame.from_dict(dict, orient="index")



df_1 = pd.read_json(r"C:\Users\HP\Downloads\fuel_station.json")
df_1 = df_1[['result']]

df_2 =  pd.io.json.json_normalize(df_1.result[:])
df_2['Longitude_fstation'] = df_2['geometry.coordinates'].apply(pd.Series)[0]

df_2['Latitude_fstation'] = df_2['geometry.coordinates'].apply(pd.Series)[1]

df_2['Petrolpump_index']  =  df_2.index + 1
df_2['Petrol pump id']  =  df_2.index + 1

df_final = pd.DataFrame()


for index, row in df_2.iterrows():
    
    str_longitude = row['Longitude_fstation']
    str_latitiude = row['Latitude_fstation']
    Petrolpump_index = row['Petrolpump_index']
    
    str_path = r"D:\Spyder codes\json_files"
    str_file_name_origin = "Api_json_" + "origin_" + str(Petrolpump_index) + ".json"
    str_file_name_destination = "Api_json_" + "destination_" + str(Petrolpump_index) + ".json"
    
    str_path_fin_origin   = os.path.join(str_path, str_file_name_origin)
    str_path_fin_destination   = os.path.join(str_path, str_file_name_destination)
    
    # print(str_path_fin_origin,str_path_fin_destination, index )
    
    
    try:
    
        df_op = call_for_each_file(str_path_fin_origin,str_path_fin_destination, Petrolpump_index, str_longitude, str_latitiude )
        
        print(Petrolpump_index)
        
        
        
        if df_final.empty:
            print('check')
            df_final = df_op.copy()
        else:
            df_final= df_final.append(df_op)
        
        print(len(df_op), len(df_final))
    
    except:
        print('check123')


df_final_2 = df_final.groupby(['Petrol pump id','Petrol_pump_address latitude','Petrol_pump_address longitude'], sort=True)['wait_time'].mean().reset_index()


df_final_3 = pd.merge(df_final_2,df_2, on = 'Petrol pump id', how = 'inner' )

list_col = ['Petrol pump id','Petrol_pump_address latitude','Petrol_pump_address longitude','wait_time'
            ,'name','address','phoneNumber','openingHours']

str_path = r"D:\Spyder codes\output\final_output2.csv"

df_final_3[list_col].to_csv(str_path)
        
        
    
        
    