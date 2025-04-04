import src.helpers.conexiones_api as conexiones_api

df = conexiones_api.GetUsersActive()
df.to_excel("./Files/Users_Active.xlsx")
print('Usuarios exportados')
print('Cantidad de filas {} '.format(df.shape[0]))
