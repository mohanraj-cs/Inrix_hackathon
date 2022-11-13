from flask import Flask
import requests

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

@app.route('/hello')
def hello():
    print(get_access())
    return 'Hello, World!'




if __name__ == '__main__':
 app.run(debug=True)

