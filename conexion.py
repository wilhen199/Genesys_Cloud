import requests
import base64
import json
from dotenv import load_dotenv
import os
load_dotenv()


def tokenization():
    region = os.getenv("PURECLOUD_REGION")
    client_id = os.getenv("PURECLOUD_CLIENT_ID")
    client_secret = os.getenv("PURECLOUD_CLIENT_SECRET")
    
    if not client_id or not client_secret or not region:
        print("Error: Las variables de entorno PURECLOUD_CLIENT_ID, PURECLOUD_CLIENT_SECRET o PURECLOUD_REGION no están definidas en el archivo .env")
        return None 

    url_token = f"https://login.{region}/oauth/token"
    auth_string = 'Basic ' + base64.b64encode(bytes((f"{client_id}:{client_secret}").encode('ascii'))).decode('ascii')
    Content = "grant_type=client_credentials"
    headers = {"Authorization": auth_string, "Accept": "application/json",
               "Content-Type": "application/x-www-form-urlencoded"}
    Response_AccessToken = requests.post(
        url_token, headers=headers, data=Content)
    Token = Response_AccessToken.json()
    return Token["access_token"]
