import requests
import pandas as pd
import conexion as cn
import src.helpers.conexiones_api as conexiones_api 
from rich.pretty import pprint

#idUser = "4b9b63f7-da25-4bda-92f9-2e5ca2dfa69e"

users = conexiones_api.GetUsersActive()
email = str(input('Ingresa cuenta NT del usuario: ')) + "@falabella.com"

if email == '':
	pprint("email is required")
else:
	user = users.loc[users["email"] == email]
	if user.empty:
		pprint("user is not exist or it was deleted")
	else:
		idUser = user.iloc[0]['id']
		data = conexiones_api.GetRoleDivUser(idUser).sort_values(by='id_role')
		pprint("User id  " + idUser)
		pprint(data)

