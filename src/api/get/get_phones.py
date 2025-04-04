import requests
import pandas as pd
import conexion as cn
from rich.pretty import pprint


def GetPhones():
    url = f"https://api.mypurecloud.com/api/v2/telephony/providers/edges/phones?pageSize=100&fields=webRtcUser"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    UserGetGroups = requests.get(url, headers=headers)
    datos = []
    pageCount = UserGetGroups.json()['pageCount']
    total = UserGetGroups.json()['total']
    for i in range(1, pageCount + 1):
        url = f"https://api.mypurecloud.com/api/v2/telephony/providers/edges/phones?fields=webRtcUser&pageNumber={str(i)}&pageSize=100"
        UserGetGroups = requests.get(url, headers=headers)
        if UserGetGroups:
            for entities in UserGetGroups.json()['entities']:
                item = {
                    'id': entities['id'],
                    'name': entities['name'],
                    'state': entities['state'],
                    'id_user': entities['webRtcUser']['id']
                }
                datos.append(item)
    df = pd.DataFrame(datos)
    pprint(df)

GetPhones()
