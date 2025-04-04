import requests
import pandas as pd
import conexion as cn
import get_users_active


def deleteUser(userId):
    url = f"https://api.mypurecloud.com/api/v2/users/{userId}"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}

    request = requests.delete(url, headers=headers)
    return request.status_code


df = get_users_active.GetUsers()
dfDelete = pd.read_excel('./Files/Delete_Users.xlsx', 'Sheet1')
for i, row in dfDelete.iterrows():
    dfTemp = df[df["email"] == row['email']]
    id = dfTemp.iloc[0]['id']
    # print(dfTemp)
    respuesta = deleteUser(id)

print("Usuarios Eliminados...")
