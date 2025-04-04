import requests
import pandas as pd
import conexion as cn
from rich.pretty import pprint
from dateutil import parser
from datetime import datetime, timezone, timedelta
import json


idRoleEmployee = '47ac4c54-f0d1-44a2-87fd-460623305aff'
idRoleUser = 'f3860d64-e11d-425f-b6a8-e74ed76dcc5e'
idDivHome = 'b36d45d0-6c20-4461-9094-c4f71ad78ad7'
idRoleSuperv = '8da548df-cde2-4e6a-8f96-ba9aba4aa526'
zona_horaria = timezone(timedelta(hours=-5))


def GetUsersActive():
    url = f"https://api.mypurecloud.com/api/v2/users?pageSize=1"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"","Accept": "application/json", "Content-Type": "application/json"}
    UserGetGroups = requests.get(url, headers=headers)

    datos = []
    total = UserGetGroups.json()['total']
    url = f"https://api.mypurecloud.com/api/v2/users?pageSize={total}&state=active"
    UserGetGroups = requests.get(url, headers=headers)
    pageSize = UserGetGroups.json()['pageSize']
    for i in range(pageSize):
        item = {
            'email': UserGetGroups.json()['entities'][i]['email'],
            'id': UserGetGroups.json()['entities'][i]['id'],
            'name': UserGetGroups.json()['entities'][i]['name'],
            'username': UserGetGroups.json()['entities'][i]['username'],
            'version': UserGetGroups.json()['entities'][i]['version'],
            'auto_answer': UserGetGroups.json()['entities'][i]['acdAutoAnswer'],
            'id_division': UserGetGroups.json()['entities'][i]['division']['id'],
            'division': UserGetGroups.json()['entities'][i]['division']['name'],
            'state': UserGetGroups.json()['entities'][i]['state']
        }
        datos.append(item)

    df = pd.DataFrame(datos)
    return df


def deleteUser(userId):
    url = f"https://api.mypurecloud.com/api/v2/users/{userId}"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}

    request = requests.delete(url, headers=headers)
    return request.status_code


def GetDivision():
    url = f"https://api.mypurecloud.com/api/v2/authorization/divisions?expand=null,null"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    divisions = requests.get(url, headers=headers)

    data = []
    total = divisions.json()['total']
    for i in range(total):
        item = {
            'id': divisions.json()['entities'][i]['id'],
            'name': divisions.json()['entities'][i]['name']
        }
        data.append(item)

    df = pd.DataFrame(data)
    return df


def GetRoles():
    url = f"https://api.mypurecloud.com/api/v2/authorization/roles"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    roles = requests.get(url, headers=headers)

    data = []
    total = roles.json()['total']
    for i in range(total):
        item = {
            'id': roles.json()['entities'][i]['id'],
            'name': roles.json()['entities'][i]['name']
        }
        data.append(item)

    df = pd.DataFrame(data)
    return df


def updateUser(userId, divisionId, roleId):
    url = f"https://api.mypurecloud.com/api/v2/authorization/subjects/{userId}/divisions/{divisionId}/roles/{roleId}"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    request = requests.post(url, headers=headers)
    return request.status_code


def autoAns(userId):
    data = [{'id': userId, 'acdAutoAnswer': True}]
    url = f"https://api.mypurecloud.com/api/v2/users/bulk"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    request = requests.patch(url, headers=headers, json=data)
    return request.status_code


def removeEmpHome(userId):
    data = {"grants": [{"roleId": idRoleEmployee, "divisionId": idDivHome}]}
    url = f"https://api.mypurecloud.com/api/v2/authorization/subjects/{userId}/bulkremove"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    request = requests.post(url, headers=headers, json=data)
    return request.status_code


def GetUsersDeleted():
    url = f"https://api.mypurecloud.com/api/v2/users?pageSize=100&state=deleted"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    UserGetGroups = requests.get(url, headers=headers)

    datos = []
    pageCount = UserGetGroups.json()['pageCount']  # 11
    for i in range(pageCount):
        url = f"https://api.mypurecloud.com/api/v2/users?pageSize=100&pageNumber={str(i)}&state=deleted"
        UserGetGroups = requests.get(url, headers=headers)
        if UserGetGroups:
            for entities in UserGetGroups.json()['entities']:
                item = {
                    'email': entities['email'],
                    'id': entities['id'],
                    'name': entities['name'],
                    'username': entities['username'],
                    'version': entities['version'],
                    'state': entities['state']
                }
                datos.append(item)
    df = pd.DataFrame(datos)
    return df


def restoreUser(userId, version):
    data = {"state": "active", "version": version}
    url = f"https://api.mypurecloud.com/api/v2/users/{userId}/state"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    request = requests.put(url, headers=headers, json=data)
    return request


def createUser(user):
    url = f"https://api.mypurecloud.com/api/v2/users"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    request = requests.post(url, headers=headers, json=user)
    return request


def GetPhones():
    url = f"https://api.mypurecloud.com/api/v2/telephony/providers/edges/phones?pageSize=100&fields=webRtcUser"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    UserGetGroups = requests.get(url, headers=headers)

    datos = []
    pageCount = UserGetGroups.json()['pageCount']
    for i in range(1, pageCount + 1):
        url = f"https://api.mypurecloud.com/api/v2/telephony/providers/edges/phones?fields=webRtcUser&pageNumber={str(i)}&pageSize=100"
        UserGetGroups = requests.get(url, headers=headers)
        if UserGetGroups:
            for entities in UserGetGroups.json()['entities']:
                item = {
                    'id': entities['id'],
                    'name': entities['name'],
                    'state': entities['state'],
                    'id_user': entities['webRtcUser']['id']
                }
                datos.append(item)
    df = pd.DataFrame(datos)
    return df


def deletePhone(phoneId):
    url = f"https://api.mypurecloud.com/api/v2/telephony/providers/edges/phones/{phoneId}"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}

    request = requests.delete(url, headers=headers)
    return request.status_code


def GetRoleUser(idUser):
    url = f"https://api.mypurecloud.com/api/v2/users/{idUser}/roles"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    UserGetRoles = requests.get(url, headers=headers)

    data = []
    roles = UserGetRoles.json()['roles']
    for i in range(len(roles)):
        item = {
            'id_role': UserGetRoles.json()['roles'][i]['id'],
            'name_role': UserGetRoles.json()['roles'][i]['name']
        }
        data.append(item)

    df = pd.DataFrame(data)
    return df


def GetUsersFromRole(roleId):
	url = f"https://api.mypurecloud.com/api/v2/authorization/roles/{roleId}/users"
	token = cn.tokenization()
	headers = {"Authorization": "Bearer "+token+"","Accept": "application/json", "Content-Type": "application/json"}
	UserGetRoles = requests.get(url, headers=headers)
	
	data = []
	total = UserGetRoles.json()['total']
	for i in range(total):
		item = {
			'idUser': UserGetRoles.json()['entities'][i]['id']
		}
		data.append(item)
	df = pd.DataFrame(data)
	return df


def GetQueues():
    url = f"https://api.mypurecloud.com/api/v2/routing/queues?pageSize=100"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    queues = requests.get(url, headers=headers)

    data = []
    for entities in queues.json()['entities']:
        item = {
            'id': entities['id'],
            'name': entities['name']
        }
        data.append(item)

    df = pd.DataFrame(data)
    return df


def AddUserToQueue(queueId, userId):
    data = [{"id":userId}]
    url = f"https://api.mypurecloud.com/api/v2/routing/queues/{queueId}/members?delete=false"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    routing = requests.post(url, headers=headers, json=data)
    return routing

def DeleteUserToQueue(queueId, userId):
    data = [{"id":userId}]
    url = f"https://api.mypurecloud.com/api/v2/routing/queues/{queueId}/members?delete=true"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    routing = requests.post(url, headers=headers, json=data)
    return routing


def GetJobs():
    url = f"https://api.mypurecloud.com/api/v2/recording/jobs?sortBy=dateCreated"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    jobs = requests.get(url, headers=headers)
    data = []
    total = jobs.json()['total']
    for entities in jobs.json()['entities']:
        item = {
            'id_job': entities['id'],
            'state': entities['state'],
            'dateCreated': parser.parse(entities['dateCreated']).date(),
            'hourCreated': parser.parse(entities['dateCreated']).strftime('%H:%M:%S'),
        }
        data.append(item)

    df_job = pd.DataFrame(data)
    jobId = df_job['id_job']
    return df_job


def GetJob_Int(jobId):
    url = f"https://api.mypurecloud.com/api/v2/recording/jobs/{jobId}"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    jobs = requests.get(url, headers=headers)
    data = []
    #print(jobs.json())
    item = {
#        'id': jobs.json()['id'],
        'action': jobs.json()['recordingJobsQuery']['action'],
        'interval': jobs.json()['recordingJobsQuery']['conversationQuery']['interval'],
        'totalRecordings': jobs.json()['totalRecordings'],
}
    data.append(item)
    df_job = pd.DataFrame(data)
    return df_job


def GetRoleDivUser(idUser):
    url = f"https://api.mypurecloud.com/api/v2/authorization/subjects/{idUser}"
    token = cn.tokenization()
    headers = {"Authorization": "Bearer "+token+"",
               "Accept": "application/json", "Content-Type": "application/json"}
    UserGetDivRoles = requests.get(url, headers=headers)

    data = []
    grants = UserGetDivRoles.json()['grants']
    for i in range(len(grants)):
        item = {
            #'division': UserGetDivRoles.json()['grants'][i]['division']['name'],
            'id_role': UserGetDivRoles.json()['grants'][i]['role']['id'],
            'name_role': UserGetDivRoles.json()['grants'][i]['role']['name'],
            'id_division': UserGetDivRoles.json()['grants'][i]['division']['id']

        }
        data.append(item)

    df = pd.DataFrame(data)
    return df