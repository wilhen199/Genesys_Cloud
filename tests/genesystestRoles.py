import requests
import base64
import json
import pandas as pd
from rich.pretty import pprint
import conexion as cn
import get_users_active


def updateUser(userId):
    url = f"https://api.mypurecloud.com/api/v2/users/{userId}/roles"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    request = requests.delete(url, headers=headers)
    return request.status_code


df = get_users_active.GetUsers()
dfUpdate = pd.read_excel('Update_Users.xlsx', 'Sheet1')
for i, row in dfUpdate.iterrows():
    dfTemp = df[df["email"] == row['email']]
    id = dfTemp.iloc[0]['id']
    # print(id)
    respuesta = updateUser(id)


# get_users()
# userId = "ec6d922e-b00a-4158-9cda-5c5a34339109"
# url = f"https://api.mypurecloud.com/api/v2/users/{userId}"
# urlRole = f"https://api.mypurecloud.com/api/v2/authorization/roles"

# user = json.dumps({"name": "Maria321", "version": 1})

# pprint(user)
# UserGetGroups = requests.patch(url, data=user, headers=headers)

# pprint(UserGetGroups.json())


'''
datos = []
pageCount = UserGetGroups.json()['pageCount']
total = UserGetGroups.json()['total']

url = f"https://api.mypurecloud.com/api/v2/users?pageSize={total}"
UserGetGroups = requests.get(url, headers=headers)
pageSize = UserGetGroups.json()['pageSize']
for i in range(pageSize):
    item = {
        'id': UserGetGroups.json()['entities'][i]['id'],
        'name': UserGetGroups.json()['entities'][i]['name'],
        'email': UserGetGroups.json()['entities'][i]['email'],
        'username': UserGetGroups.json()['entities'][i]['username'],
        'auto_answer': UserGetGroups.json()['entities'][i]['acdAutoAnswer'],
        'id_division': UserGetGroups.json()['entities'][i]['division']['id'],
        'division': UserGetGroups.json()['entities'][i]['division']['name']
    }
    datos.append(item)

df = pd.DataFrame(datos)
df.to_excel("prueba1.xlsx")
'''
