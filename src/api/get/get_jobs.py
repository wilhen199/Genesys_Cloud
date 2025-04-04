import requests
import pandas as pd
import conexion as cn
from rich.pretty import pprint
from dateutil import parser
from datetime import datetime, timezone, timedelta

zona_horaria = timezone(timedelta(hours=-5))

def GetJobs():
    url = f"https://api.mypurecloud.com/api/v2/recording/jobs?sortBy=dateCreated"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    jobs = requests.get(url, headers=headers)
    data = []
#    pprint(jobs.json())
    for entities in jobs.json()['entities']:
        item = {
#            'id': jobs.json()['entities'][i]['id'],
            'id_job': entities['id'],
            'state': entities['state'],
            'dateCreate': (parser.parse(entities['dateCreated'])).astimezone(zona_horaria).date(),
            'hourCreated': (parser.parse(entities['dateCreated'])).astimezone(zona_horaria).strftime('%H:%M:%S'),
        }
        data.append(item)

    df_job = pd.DataFrame(data)
    jobId = df_job['id_job']
    pprint(df_job)




GetJobs()

