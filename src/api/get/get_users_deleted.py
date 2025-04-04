import requests
import pandas as pd
import conexion as cn
from rich.pretty import pprint


def GetUsersDeleted():
    url = f"https://api.mypurecloud.com/api/v2/users?pageSize=100&state=deleted"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    UserGetGroups = requests.get(url, headers=headers)
    pprint(UserGetGroups.json())
    datos = []
    pageCount = UserGetGroups.json()['pageCount']
    for i in range(pageCount):
        url = f"https://api.mypurecloud.com/api/v2/users?pageSize=100&pageNumber={str(i)}&state=deleted"
        UserGetGroups = requests.get(url, headers=headers)
        pprint(url)
        if UserGetGroups:
            for entities in UserGetGroups.json()['entities']:
                item = {
                    'email': entities['email'],
                    'id': entities['id'],
                    'name': entities['name'],
                    'username': entities['username'],
                    'version': entities['version'],
                    'state': entities['state']
                }
                datos.append(item)
    df = pd.DataFrame(datos)
    pprint(df)


GetUsersDeleted()
