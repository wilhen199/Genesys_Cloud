import requests
import pandas as pd
from dateutil import parser
import conexion as cn
import json
from rich.pretty import pprint
from datetime import datetime, timezone, timedelta, time
import numpy as np

zona_horaria = timezone(timedelta(hours=-5))
with open("time_data.json") as data_json:
    datos = json.load(data_json)

def GetTime():
    url = f"https://api.mypurecloud.com/api/v2/analytics/conversations/details/query"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    data = []
    intervalos = [
        "2023-01-01T00:00:01/2023-01-31T23:59:59",
        "2023-02-01T00:00:01/2023-02-28T23:59:59",] 
#        "2023-03-01T00:00:01/2023-03-31T23:59:59",
#        "2023-04-01T00:00:01/2023-04-30T23:59:59",
#        "2023-05-01T00:00:01/2023-05-31T23:59:59",
#        "2023-06-01T00:00:01/2023-06-30T23:59:59",
#        "2023-07-01T00:00:01/2023-07-31T23:59:59",
#        "2023-08-01T00:00:01/2023-08-31T23:59:59",
#        "2023-09-01T00:00:01/2023-09-30T23:59:59"]
    for nuevo in intervalos:
        datos['interval'] = nuevo
        interactions = requests.post(url, headers=headers, json=datos)
        total = (interactions.json()['totalHits'] // 100) + 1
        for i in range(1, total + 1):
            datos['paging']['pageNumber'] = i
            interactions = requests.post(url, headers=headers, json=datos)

            for conversations in interactions.json()['conversations']:
                item = {
                    'Date': (parser.parse(conversations['conversationStart']).astimezone(zona_horaria)).strftime("%Y-%m-%d"),
                    'Start_Time': (parser.parse(conversations['conversationStart']).astimezone(zona_horaria)).strftime('%H:%M:%S'),
                    'End_Time': (parser.parse(conversations['conversationEnd']).astimezone(zona_horaria)).strftime('%H:%M:%S'),
##                    'Start_Time': conversations['conversationStart'],
##                    'End_Time': conversations['conversationEnd'],
                    'ConversationId': conversations['conversationId'],
                    'DNIS': conversations['participants'][0]['sessions'][0]['dnis'],
                    }
                data.append(item)

        df = pd.DataFrame(data)

    pprint(df)
#    df.to_excel("./Files/Llamadas_Salientes_Celulares_2023_.xlsx")
#        pprint(df.head())
#        pprint(df.dtypes)

GetTime()



