# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 20:32:23 2022

@author: HP
"""


from flask import Flask
import requests

import pandas as pd
import json
from pandas import json_normalize
from datetime import time, timedelta
from pathlib import Path

import os

app = Flask(__name__)


# def get_access():
#     URL = 'https://api.iq.inrix.com/auth/v1/appToken?appId=yxjls34uih&hashToken=eXhqbHMzNHVpaHw1clJXZU1qNUoxNFFpUEVNVkRNemU3cU13dUtSZ01wcWE1dHRRTlJk'
#     try:
#             response = requests.get(URL)
#             response_json = response.json()
#             token = response_json.get("result").get("token")
#             return token
#     except Exception as e:
#         print("Error while obtaining token", e)
#         return ""

# @app.route('/hello')
# def hello():
#     print(get_access())
#     return 'Hello, World!'






df_1 = pd.read_json(r"C:\Users\HP\Downloads\fuel_station.json")
df_1 = df_1[['result']]

df_2 =  pd.io.json.json_normalize(df_1.result[:])
df_2['Longitude_fstation'] = df_2['geometry.coordinates'].apply(pd.Series)[0]

df_2['Latitude_fstation'] = df_2['geometry.coordinates'].apply(pd.Series)[1]

df_2['Petrolpump_index']  =  df_2.index + 1

# df_2[['city','state']] = df_2['geometry.coordinates'].apply(pd.series)[1]

# print(df_1.columns)



str_api = f"https://trade-areas-api.inrix.com/v1/trips?accessToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXZpY2VJZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMCIsImNzVG9rZW4iOm51bGwsInVzZXJSb2xlIjoxLCJhcHBSb2xlIjo0LCJ1c2VySWQiOiIwY2ZkNzJjYi1kNjcyLTRjYTctYTllZi02Y2I3NzBlMTQ5MTIiLCJhcHBJZCI6ImFiOGViYWQwLTQ3MGQtNDY5Zi05ODI1LWQ1YjgxNmVlZWU1YSIsImRldmVsb3BlcklkIjoiYTk0ODRiZGEtY2MxZC00YTdiLTgzMGQtYjJhNDZiYjgwY2Y3IiwiZXhwaXJ5IjoiMjAyMi0xMS0xM1QxMTozMDoxMy4wNzA1MjFaIiwiZXhwIjoxNjY4MzM5MDEzLCJyb2xlIjoidXNlciJ9.bbz3cFRvSO4ZJvDWHx-gnAX5ooMonbiQ8scoP20cRsM&limit=10000&geoFilterType=circle&points=[[longitude__bb]]|[[latitude_aa]]&od=[[tag_when]]&radius=100m&startDateTime=>=2022-05-01T02:31&endDateTime=<=2022-05-02T02:31"
    

straa = "https://trade-areas-api.inrix.com/v1/trips?accessToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXZpY2VJZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMCIsImNzVG9rZW4iOm51bGwsInVzZXJSb2xlIjoxLCJhcHBSb2xlIjo0LCJ1c2VySWQiOiIwY2ZkNzJjYi1kNjcyLTRjYTctYTllZi02Y2I3NzBlMTQ5MTIiLCJhcHBJZCI6ImFiOGViYWQwLTQ3MGQtNDY5Zi05ODI1LWQ1YjgxNmVlZWU1YSIsImRldmVsb3BlcklkIjoiYTk0ODRiZGEtY2MxZC00YTdiLTgzMGQtYjJhNDZiYjgwY2Y3IiwiZXhwaXJ5IjoiMjAyMi0xMS0xM1QxMTozMDoxMy4wNzA1MjFaIiwiZXhwIjoxNjY4MzM5MDEzLCJyb2xlIjoidXNlciJ9.bbz3cFRvSO4ZJvDWHx-gnAX5ooMonbiQ8scoP20cRsM&limit=10000&geoFilterType=circle&points=37.7739233|-122.4373049&od=origin&radius=100m&startDateTime=>=2022-05-01T02:31&endDateTime=<=2022-05-02T02:31" 

print("1")

for index, row in df_2.iterrows():
    
    str_longitude = row['Longitude_fstation']
    str_latitiude = row['Latitude_fstation']
    Petrolpump_index = row['Petrolpump_index']
    
    str_api_2 = str_api.replace('[[longitude__bb]]',str(str_latitiude))
    str_api_2 = str_api_2.replace('[[latitude_aa]]',str(str_longitude))
    
    str_api_2 = str_api_2.replace('[[tag_when]]','origin')
    
    
    # [[tag_when]]
    
    y = {"Petrolpump_index":Petrolpump_index}
    str_path = r"D:\Spyder codes\json_files"
    str_file_name = "Api_json_" + "origin_" + str(Petrolpump_index) + ".json"
    
    str_path_fin   = os.path.join(str_path, str_file_name)
    
    # import json
    # with open(str_path + str_file_name, 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)
    
    
    try:
        response = requests.get(str_api_2, headers={"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXZpY2VJZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMCIsImNzVG9rZW4iOm51bGwsInVzZXJSb2xlIjoxLCJhcHBSb2xlIjo0LCJ1c2VySWQiOiIwY2ZkNzJjYi1kNjcyLTRjYTctYTllZi02Y2I3NzBlMTQ5MTIiLCJhcHBJZCI6ImFiOGViYWQwLTQ3MGQtNDY5Zi05ODI1LWQ1YjgxNmVlZWU1YSIsImRldmVsb3BlcklkIjoiYTk0ODRiZGEtY2MxZC00YTdiLTgzMGQtYjJhNDZiYjgwY2Y3IiwiZXhwaXJ5IjoiMjAyMi0xMS0xM1QxMTozMDoxMy4wNzA1MjFaIiwiZXhwIjoxNjY4MzM5MDEzLCJyb2xlIjoidXNlciJ9.bbz3cFRvSO4ZJvDWHx-gnAX5ooMonbiQ8scoP20cRsM"})
        response_json = response.json()
        token = response_json.get("data")
        
        with open(str_path_fin, 'w', encoding='utf-8') as f:
            json.dump(token, f, ensure_ascii=False, indent=4)
        
        print(index, token)
        
    except Exception as e:
        print("Error while obtaining token", e)
        
        
    str_api_2 = str_api_2.replace('[[tag_when]]','destination')
    str_file_name = "Api_json_" + "destination_" + str(Petrolpump_index) + ".json"
    
    str_path_fin   = os.path.join(str_path, str_file_name)
    
    try:
        response = requests.get(str_api_2, headers={"Authorization":"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkZXZpY2VJZCI6IjAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMCIsImNzVG9rZW4iOm51bGwsInVzZXJSb2xlIjoxLCJhcHBSb2xlIjo0LCJ1c2VySWQiOiIwY2ZkNzJjYi1kNjcyLTRjYTctYTllZi02Y2I3NzBlMTQ5MTIiLCJhcHBJZCI6ImFiOGViYWQwLTQ3MGQtNDY5Zi05ODI1LWQ1YjgxNmVlZWU1YSIsImRldmVsb3BlcklkIjoiYTk0ODRiZGEtY2MxZC00YTdiLTgzMGQtYjJhNDZiYjgwY2Y3IiwiZXhwaXJ5IjoiMjAyMi0xMS0xM1QxMTozMDoxMy4wNzA1MjFaIiwiZXhwIjoxNjY4MzM5MDEzLCJyb2xlIjoidXNlciJ9.bbz3cFRvSO4ZJvDWHx-gnAX5ooMonbiQ8scoP20cRsM"})
        response_json = response.json()
        token = response_json.get("data")
        
        with open(str_path_fin, 'w', encoding='utf-8') as f:
            json.dump(token, f, ensure_ascii=False, indent=4)
        
       
        print(index, token)
        
    except Exception as e:
        print("Error while obtaining token", e)
        
        

    
print("2")
    
    
# app.run(debug=True)
    
 
