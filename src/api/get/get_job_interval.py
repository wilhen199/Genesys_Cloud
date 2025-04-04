import requests
import pandas as pd
import conexion as cn
import src.helpers.conexiones_api as conexiones_api
from rich.pretty import pprint
from dateutil import parser
from datetime import datetime, timezone, timedelta


zona_horaria = timezone(timedelta(hours=-5))
df_jobs = conexiones_api.GetJobs()
#jobId = df_jobs['id_job']

#print(jobId)
#jobId = "72a9cef1-da89-4ddb-86dd-8b04406ee8fc"
#pprint(conexiones_api.GetJobs[])

df_jobs['action'] = ''
#df_jobs['interval'] = ''
df_jobs['totalRecordings'] = ''
df_jobs['interval_start'] = ''
df_jobs['interval_end'] = ''

for i, row in df_jobs.iterrows():
#  print(row)
  jobId = row['id_job']
  df_detail = conexiones_api.GetJob_Int(jobId)
#  print(df_detail['action'][0])
  df_jobs.at[i, 'action'] = df_detail['action'][0]
  #df_jobs.at[i, 'interval'] = df_detail['interval'][0]
  df_jobs.at[i, 'interval_start'] = str(df_detail['interval'][0]).split('/')[0]
  df_jobs.at[i, 'interval_end'] = str(df_detail['interval'][0]).split('/')[1]
  df_jobs.at[i, 'totalRecordings'] = df_detail['totalRecordings'][0]

pprint(df_jobs)

