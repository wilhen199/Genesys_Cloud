import src.helpers.conexiones_api as conexiones_api

df = conexiones_api.GetPhones()
df.to_excel("./Files/Phones.xlsx")
print('Telefonos exportados')
print('Cantidad de filas {} '.format(df.shape[0]))
