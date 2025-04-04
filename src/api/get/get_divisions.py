import requests
import pandas as pd
import conexion as cn
from rich.pretty import pprint


def GetDivision():
    url = f"https://api.mypurecloud.com/api/v2/authorization/divisions?expand=null,null"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    divisions = requests.get(url, headers=headers)

    data = []
    total = divisions.json()['total']
    print(total)
    for i in range(total):
        item = {
            'id': divisions.json()['entities'][i]['id'],
            'name': divisions.json()['entities'][i]['name']
        }
        data.append(item)

    df = pd.DataFrame(data)
    pprint(df)


GetDivision()
