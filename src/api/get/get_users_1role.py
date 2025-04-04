import requests
import pandas as pd
import conexion as cn
import src.helpers.conexiones_api as conexiones_api 
from rich.pretty import pprint

users = conexiones_api.GetUsersActive()
roles = conexiones_api.GetRoles()

roleInput = str(input('Ingresa rol: ')).title()
if roleInput == 'Admin' or roleInput == 'Employee':
	roleInput = roleInput.lower()
role = roles.loc[roles["name"] == roleInput]
roleId = role.iloc[0]['id']

idUsers = conexiones_api.GetUsersFromRole(roleId)
idUsers.to_excel('./Files/users_temp.xlsx')

df_usersId = pd.read_excel('./Files/users_temp.xlsx', 'Sheet1')
data = []
for i, row in df_usersId.iterrows():
    userId = users.loc[users['id'] == row['idUser']]
    userEmail = userId.iloc[0]['email']
    userName = userId.iloc[0]['name']
    item = {
			'name': users.iloc[i]['name'],
			'id': users.iloc[i]['id'],
      'email': users.iloc[i]['email']
                  }
    data.append(item)
    final = pd.DataFrame(data)
pprint(final)
#pprint(type(users))
#pprint(type(idUsers))
#pprint(users)
pprint(idUsers)


	#idUsers = UserGetRoles.json()['entities']
	#pprint(type(idUsers))



#usersFromRole = idUsers.loc[idUsers["idUser"] == users["id"]]

#userId = usersFromRole.iloc[0]['id']
#userName = usersFromRole.iloc[0]['name']
#userEmail = usersFromRole.iloc[0]['email']
#pprint(userEmail)
#pprint(idUsers)
#pprint(users['id'])

#email = input('Ingresa correo del usuario: ' )
#user = users.loc[users["email"] == email]
#idUser = user.iloc[0]['id']
#data = conexiones_api.GetRoleUser(idUser)
#pprint(data)
