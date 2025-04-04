import pandas as pd
from rich.pretty import pprint
import src.helpers.conexiones_api as conexiones_api


dfUsers = pd.read_excel('./Files/Update_Users.xlsx', 'Sheet1')
users = conexiones_api.GetUsersActive()
divisions =  conexiones_api.GetDivision()
for i, row in dfUsers.iterrows():
    user = users.loc[users["email"] == row['email']]
    user_id = user.iloc[0]['id']
    division = divisions.loc[divisions['name'] == row['division']]
    divisionId = division.iloc[0]['id']
    conexiones_api.updateUser(user_id, divisionId, conexiones_api.idRoleUser)
    conexiones_api.updateUser(user_id, division, conexiones_api.idRoleEmployee)
    conexiones_api.autoAns(user_id)
