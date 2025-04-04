import pandas as pd
import src.helpers.conexiones_api as conexiones_api
from rich.pretty import pprint

df = conexiones_api.GetPhones()
dfDelete = pd.read_excel('./Files/Delete_Phones.xlsx', 'Sheet1')
for i, row in dfDelete.iterrows():
    dfTemp = df[df["id"] == row['id']]
    if dfTemp.shape[0] > 0:
        id = dfTemp.iloc[0]['id']
        pprint(id)
        name = dfTemp.iloc[0]['name']
        response = conexiones_api.deletePhone(id)
        pprint(response)
        if response:
            pprint("Usuario Eliminado id = {} user = {}".format(id, name))
        else:
            break
pprint('{} Usuarios en la lista'.format(dfDelete.shape[0]))
