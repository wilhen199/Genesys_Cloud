import src.helpers.conexiones_api as conexiones_api

df = conexiones_api.GetRoles()
df.to_excel("./Files/roles.xlsx")
print('Roles exportados')
print('Cantidad de filas {} '.format(df.shape[0]))