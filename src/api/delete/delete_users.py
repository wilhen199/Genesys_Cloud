import pandas as pd
import src.helpers.conexiones_api as conexiones_api
from rich.pretty import pprint

# Get active users and webrtc
df_users_active = conexiones_api.GetUsersActive()
df_phones = conexiones_api.GetPhones()

# Rename columns from dataframes
df_users_active = df_users_active.rename(
    columns={'id': 'id_user', 'name': 'name_user', 'state': 'state_user'})
df_phones = df_phones.rename(
    columns={'id': 'id_phone', 'name': 'name_phone', 'state': 'state_phone'})

# Merge dataframes by column name id_user
df_all = pd.merge(df_users_active, df_phones, how='inner', on='id_user')

# Read Excel file with users to delete
df_delete = pd.read_excel('./Files/Delete_Users.xlsx', 'Sheet1')

# Iterate for each user to delete
for i, row in df_delete.iterrows():
    # Filter active users by email
    df_temp_all = df_all[df_all["email"] == row['email']]

    if df_temp_all.empty:
        df_temp_user = df_users_active[df_users_active["email"]
                                       == row['email']]

        if df_temp_user.empty:
            pprint("Usuario no se encuentra")
        else:
            idUser = df_temp_user.iloc[0]['id_user']
            email = df_temp_user.iloc[0]['email']
            # Delete user
            responseUser = conexiones_api.deleteUser(idUser)
            pprint("Usuario Eliminado id={} user={}".format(idUser, email))
    else:
        if df_temp_all.shape[0] > 0:
            idUser = df_temp_all.iloc[0]['id_user']
            email = df_temp_all.iloc[0]['email']
            idPhone = df_temp_all.iloc[0]['id_phone']

            # Delete user and webrtc
            responseUser = conexiones_api.deleteUser(idUser)
            if responseUser == 200:
                pprint("Usuario Eliminado id={} user={}".format(idUser, email))
                pprint("WebRTC Eliminado user={} id_phone={}".format(email, idPhone))
            else:
                break

pprint('{} Usuarios en la lista'.format(df_delete.shape[0]))
