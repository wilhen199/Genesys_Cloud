import pandas as pd
from rich.pretty import pprint
import src.helpers.conexiones_api as conexiones_api

# Read Excel file with users to update
df_users = pd.read_excel('./Files/Update_Users.xlsx', 'Sheet1')

# Get active users, divisions and and deleted users
users = conexiones_api.GetUsersActive()
divisions = conexiones_api.GetDivision()
restore = conexiones_api.GetUsersDeleted()

# Iterate for each user to update
for i, row in df_users.iterrows():
    # Filter active users by email
    user = users.loc[users["email"] == row['email']]
    # Filter division by division name
    division = divisions.loc[divisions['name'] == row['division']]
    divisionId = division.iloc[0]['id']
    
    if user.empty:
        userRestore = restore.loc[restore['email'] == row['email']]

        if not userRestore.empty:
            userRestoreId = userRestore.iloc[0]['id']
            userRestoreVersion = userRestore.iloc[0]['version']
            pprint('El usuario {} está eliminado'.format(df_users.iloc[i]['email']))

            # Restore user if it deleted
            response = conexiones_api.restoreUser(str(userRestoreId), int(userRestoreVersion))

            # Update roles and auto-answer
            conexiones_api.updateUser(userRestoreId, divisionId, conexiones_api.idRoleUser)
            conexiones_api.updateUser(userRestoreId, divisionId, conexiones_api.idRoleEmployee)
            conexiones_api.autoAns(userRestoreId)
            pprint('Usuario {} restaurado'.format(df_users.iloc[i]['email']))
        else:
            pprint('No se encontró ningún usuario eliminado con el correo electrónico {}'.format(row['email']))
    else:
        user_id = user.iloc[0]['id']
        user_email = user.iloc[0]['email']

        # Delete division home in role employee
        conexiones_api.removeEmpHome(user_id)

        # Update roles and auto-answer
        conexiones_api.updateUser(user_id, divisionId, conexiones_api.idRoleUser)
        conexiones_api.updateUser(user_id, divisionId, conexiones_api.idRoleEmployee)
        conexiones_api.autoAns(user_id)
        pprint('Usuario {} modificado satisfactoriamente'.format(df_users.iloc[i]['email']))




        
#        userRestore = restore.loc[restore['email'] == row['email']]
#        userRestoreId = userRestore.iloc[0]['id']
#        userRestoreVersion = userRestore.iloc[0]['version']
#        pprint('El usuario {} está eliminado'.format(df_users.iloc[i]['email']))
#
#        # Restore user if it deleted
#        response = conexiones_api.restoreUser(str(userRestoreId), int(userRestoreVersion))
#
#        # Update roles and auto-answer
#        conexiones_api.updateUser(userRestoreId, divisionId, conexiones_api.idRoleUser)
#        conexiones_api.updateUser(userRestoreId, divisionId, conexiones_api.idRoleEmployee)
#        conexiones_api.autoAns(userRestoreId)
#        pprint('Usuario {} restaurado'.format(df_users.iloc[i]['email']))
#    else:
#        user_id = user.iloc[0]['id']
#        user_email = user.iloc[0]['email']
#
#
#
#        # Delete division home in role employee
#        conexiones_api.removeEmpHome(user_id)
#
#        # Update roles and auto-answer
#        conexiones_api.updateUser(user_id, divisionId, conexiones_api.idRoleUser)
#        conexiones_api.updateUser(user_id, divisionId, conexiones_api.idRoleEmployee)
#        conexiones_api.autoAns(user_id)
#        pprint('Usuario {} modificado satisfactoriamente'.format(df_users.iloc[i]['email']))
#