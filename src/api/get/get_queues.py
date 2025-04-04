import requests
import pandas as pd
import conexion as cn
from rich.pretty import pprint


def GetQueues():
    url = f"https://api.mypurecloud.com/api/v2/routing/queues?pageSize=100"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    queues = requests.get(url, headers=headers)

    data = []
#    total = queues.json()['total']
#    pprint(queues.json()['entities'])
#    for i in range(total):
    for entities in queues.json()['entities']:
        item = {
            'id': entities['id'],
            'name': entities['name']
        }
        data.append(item)

    df = pd.DataFrame(data)
    df.to_excel("./Files/Queues.xlsx")
    pprint(df)


GetQueues()
