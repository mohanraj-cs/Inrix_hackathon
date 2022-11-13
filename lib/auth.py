from . import constants as const
import requests

class Auth:
    def __init__(self) -> None:
        self.URL = 'https://api.iq.inrix.com/auth/v1/appToken?appId=yxjls34uih&hashToken=eXhqbHMzNHVpaHw1clJXZU1qNUoxNFFpUEVNVkRNemU3cU13dUtSZ01wcWE1dHRRTlJk' 
        

    def get_token(self):
        try:
            response = requests(self.URL)
            response_json = response.json()
            token = response_json.get("result").get("token")
            return token
        except Exception as e:
            print("Error while obtaining token", e)
            return ""