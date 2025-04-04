import requests
import pandas as pd
import conexion as cn
import src.helpers.conexiones_api as conexiones_api
from rich.pretty import pprint

df_update = pd.read_excel('./Files/DeleteUsersToQueue.xlsx')

queues = conexiones_api.GetQueues()
users = conexiones_api.GetUsersActive()


for i, row in df_update.iterrows():
	queue = queues.loc[queues['name'] == row['queue']]
	queueId = queue.iloc[0]['id']
	if queueId == '':
		pprint("Queue is not found")
	else:
		user = users.loc[users['email'] == row['email']]
		if user.empty:
			pprint("user is not exist or it was deleted")
		else:
			userId = user.iloc[0]['id']
			request = conexiones_api.DeleteUserToQueue(queueId, userId)
			if request.status_code == 200:
				pprint("User {} deleted successfully to queue {}".format(user.iloc[0]['email'], queue.iloc[0]['name']))