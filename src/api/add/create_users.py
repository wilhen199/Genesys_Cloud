import requests
from rich.pretty import pprint
import pandas as pd
import conexion as cn
import src.helpers.conexiones_api as conexiones_api


# Read Excel file with users to create
df_users = pd.read_excel('./Files/Create_Users.xlsx', 'Sheet1')

# Get divisions, users deleted and users actives
divisions = conexiones_api.GetDivision()
restore = conexiones_api.GetUsersDeleted()
active = conexiones_api.GetUsersActive()

# Iterate for each user to create
for i, row in df_users.iterrows():
    division = divisions.loc[divisions['name'] == row['division']]
    divisionId = division.iloc[0]['id']

    user = {
        "name": df_users.iloc[i]['name'],
        "email": df_users.iloc[i]['email'],
        "divisionId": divisionId,
        "state": "active",
        "enabled": True
    }

    # Create a new user with the specified email
    request = conexiones_api.createUser(user)
    response = request.status_code
    extracId = request.json()

    if response == 200:
        # Delete division home in role employee
        conexiones_api.removeEmpHome(extracId['id'])
        # Update roles and auto-answer
        conexiones_api.updateUser(extracId['id'], divisionId, conexiones_api.idRoleUser)
        conexiones_api.updateUser(extracId['id'], divisionId, conexiones_api.idRoleEmployee)
        conexiones_api.autoAns(extracId['id'])
        pprint('Usuario {} creado satisfactoriamente'.format(df_users.iloc[i]['email']))
        
    elif response == 400:
        userRestore = restore.loc[restore['email'] == row['email']]

        if userRestore.empty:
            pprint('El usuario {} está activo'.format(df_users.iloc[i]['email']))
            userActive = active.loc[active['email'] == row['email']]
            user_id = userActive.iloc[0]['id']
            # Delete division home in role employee
            conexiones_api.removeEmpHome(user_id)
            # Update roles and auto-answer
            conexiones_api.updateUser(user_id, divisionId, conexiones_api.idRoleUser)
            conexiones_api.updateUser(user_id, divisionId, conexiones_api.idRoleEmployee)
            conexiones_api.autoAns(user_id)

        else:
            pprint('El usuario {} está eliminado'.format(df_users.iloc[i]['email']))
            userRestoreId = userRestore.iloc[0]['id']
            userRestoreVersion = userRestore.iloc[0]['version']
            # Restore user if it deleted
            response = conexiones_api.restoreUser(str(userRestoreId), int(userRestoreVersion))
            conexiones_api.updateUser(userRestoreId, divisionId, conexiones_api.idRoleUser)
            conexiones_api.updateUser(userRestoreId, divisionId, conexiones_api.idRoleEmployee)
            conexiones_api.autoAns(userRestoreId)
            pprint('Usuario {} restaurado'.format(df_users.iloc[i]['email']))
    else:
        pprint('revisa el archivo xlsx')
