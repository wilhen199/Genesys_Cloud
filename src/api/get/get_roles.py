import requests
import pandas as pd
import conexion as cn
from rich.pretty import pprint


def GetRoles():
    url = f"https://api.mypurecloud.com/api/v2/authorization/roles"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    roles = requests.get(url, headers=headers)

    data = []
    total = roles.json()['total']
    for i in range(total):
        item = {
            'id': roles.json()['entities'][i]['id'],
            'name': roles.json()['entities'][i]['name']
        }
        data.append(item)

    df = pd.DataFrame(data)
    pprint(df)


GetRoles()
