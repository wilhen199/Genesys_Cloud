import src.helpers.conexiones_api as conexiones_api

df = conexiones_api.GetDivision()
df.to_excel("./Files/divisions.xlsx")
