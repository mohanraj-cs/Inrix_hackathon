from flask import Flask
import requests
import json
from rtree import index

app = Flask(__name__)


def get_access():
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
def nearest_point(source=(-122.4844171, 37.8587248, -122.4844171, 37.8587248), n=5):
    co_ordinates = []
    res = ''
    result = []
    idx = index.Index()
    with open("response.json", "r") as r:
        res = json.load(r)["result"]
        for co_ordinate in res:
            co_ordinates.append(co_ordinate["geometry"]["coordinates"])

        for i, item in enumerate(co_ordinates):
            idx.insert(i, (item[0], item[1], item[0], item[1]))

        # Get the nearest 'n' co_ordinates  
        nearest = list(idx.nearest(source, n))
        #print(nearest)
        for i in nearest:
            result.append([i, co_ordinates[i][0], co_ordinates[i][1]])
        return result
        #print(result)


@app.route('/hello')
def hello():
    print(get_access())
    nearest_point()
    return 'Hello, World!'

@app.route("/dummy")
def dummy():
    data = {"result": [
                {"lat":1.0000, "long":2.000, "wait":1.0},
                {"lat":2.0000, "long":3.000, "wait":1.5},
                {"lat":4.0000, "long":5.000, "wait":15},
    ]}
    return json.dumps(data)

if __name__ == '__main__':
 app.run(debug=True)

