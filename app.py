from flask import Flask, request
from flask_cors import CORS, cross_origin
import requests, json, random, csv
from rtree import index
import pandas as pd

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
global_co_ordinates = []
global_pd = pd.DataFrame()

def get_access_token():
    URL = 'https://api.iq.inrix.com/auth/v1/appToken?appId=yxjls34uih&hashToken=eXhqbHMzNHVpaHw1clJXZU1qNUoxNFFpUEVNVkRNemU3cU13dUtSZ01wcWE1dHRRTlJk'
    try:
        response = requests.get(URL)
        response_json = response.json()
        token = response_json.get("result").get("token")
        return token
    except Exception as e:
        print("Error while obtaining token", e)
        return ""
    
# https://rtree.readthedocs.io/en/latest/tutorial.html
# Args: source co-ordinate (top, left, bottom, right)
# Return: An array: [id, [lat, long]]
def nearest_point(lat=-122.4844171,long= 37.8587248, n=5):
    source=(lat, long, lat, long)
    global global_co_ordinates
    co_ordinates = []
    res = ''
    result = []
    idx = index.Index()
    with open("response.json", "r") as r:
        res = json.load(r)["result"]
        for co_ordinate in res:
            co_ordinates.append(co_ordinate["geometry"]["coordinates"])
        
        global_co_ordinates = co_ordinates

        for i, item in enumerate(co_ordinates):
            idx.insert(i, (item[1], item[0], item[1], item[0]))

        # Get the nearest 'n' co_ordinates  
        nearest = list(idx.nearest(source, n))
        #print(nearest)
        for i in nearest:
            result.append([i, co_ordinates[i][1], co_ordinates[i][0]])
        return result
        #print(result)

#args: Petrol Pump ID 
def get_wait_time(lng=-122.437817, lat=24.480877777777778):
    p_id=0
    global global_pd
    wait_time_dict = {}
    nearest_point()
    line_count = 0
    with open('waiting_time.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        global_pd = pd.read_csv("waiting_time.csv")
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                # print("printing headers", row)
            else:
                wait_time_dict[int(row[1])] = [row[2], row[3], row[4]]
                line_count += 1
    p_id += 1
    return wait_time_dict.get(p_id, [lng, lat, 9.478899])

def get_wait_time_v2(lng, lat):
    global global_pd
    nearest_pumps = nearest_point(lat,lng)
    df_pumps = pd.read_csv('final_output2.csv')
    df_final = pd.DataFrame()
    for item in nearest_pumps:
        item_lat = item[1]
        item_lng = item[2]
        if df_final.empty:
            df_final = df_pumps[(df_pumps['lat'] == item_lat) & (df_pumps['lng'] == item_lng)]
        else:
            df_1 = df_pumps[(df_pumps['lat'] == item_lat) & (df_pumps['lng'] == item_lng)]
            df_final = df_final.append(df_1)

    return df_final


def get_data_petrol(p_id=0):
    df = global_pd[global_pd['Petrol pump id'] == str(p_id)]
    #yet to complete
    df_1 = pd.read_json("response.json")
    df_1 = df_1[['result']]
    df_2 =  pd.io.json.json_normalize(df_1.result[:])
    df_2['Petrolpump_index']  =  df_2.index + 1
    return {'name': "Chevron", "openingHours":12, "address": "benton road", "Phone Number":7894555210}

@app.route('/hello')
def hello():
    print(get_access_token())
    nearest_point()
    print("******", get_wait_time())
    return 'Hello, World!'

@app.route("/dummy")
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def dummy():
    nearest_point()
    global global_co_ordinates
    data = []
    for i in global_co_ordinates:
        data.append( {"lat":i[1], "long":i[0], "wait":random.randrange(5, 50, 3)})
    
    data = {"result": data}
    return json.dumps(data)

@app.route("/getnearestwithwaittime")
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getnearestwithwaittime():
    args = request.args
    lat = args.get("lat", type=float)
    lng = args.get("lng", type=float)
    return get_wait_time_v2(lng,lat).to_json(orient = 'records')

if __name__ == '__main__':
 app.run(debug=True)

if __name__ == '__main__':
 app.run(debug=True)
 

