import requests
import pandas as pd
import conexion as cn
from rich.pretty import pprint


def GetUsersActive():
    url = f"https://api.mypurecloud.com/api/v2/users?pageSize=1&state=active"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    UserGetGroups = requests.get(url, headers=headers)
    datos = []
    total = UserGetGroups.json()['total']
    url = f"https://api.mypurecloud.com/api/v2/users?pageSize={total}&state=active"
    UserGetGroups = requests.get(url, headers=headers)
    pageSize = UserGetGroups.json()['pageSize']
    for i in range(pageSize):
        item = {
            'email': UserGetGroups.json()['entities'][i]['email'],
            'id': UserGetGroups.json()['entities'][i]['id'],
            'name': UserGetGroups.json()['entities'][i]['name'],
            'username': UserGetGroups.json()['entities'][i]['username'],
            'version': UserGetGroups.json()['entities'][i]['version'],
            'auto_answer': UserGetGroups.json()['entities'][i]['acdAutoAnswer'],
            'id_division': UserGetGroups.json()['entities'][i]['division']['id'],
            'division': UserGetGroups.json()['entities'][i]['division']['name']
        }
        datos.append(item)

    df = pd.DataFrame(datos)
    pprint(df)


GetUsersActive()
