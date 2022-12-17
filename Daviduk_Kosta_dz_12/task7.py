data1 = {
    "action": "presence",
    "type": "status",
    "user": {
        "account_name": 'Kostia',
        "status": "Yep, I am here!"
    }
}

data2 = {
    "action": "presence",
    "type": "status",
    "user": {
        "account_name": 'Petia',
        "status": "Yep, I am here!"
    }
}
clients = []

login = {}
client1 = 1
client2 = 2
clients.append(client1)
clients.append(client2)

login[data1["user"]["account_name"]] = client1
login[data2["user"]["account_name"]] = client2
print(login)  # {'Kostia': 1, 'Petia': 2}

# print(login[data["user"]["account_name"]])  # 1
# clients.remove(login[data["user"]["account_name"]])
print(clients)  # []

# del login[data["user"]["account_name"]]
# print(login)


data = {
    "action": "msg",
    "from": 'Kostia',
    "to": 'Petia',
    "message": 'notice'
}

print(login[data["to"]])
clients.remove(login[data["to"]])

del login[data["to"]]
print(clients)
print(login)
