import requests

def get_users(count):
    users = []
    offset = 0
    while len(users) < count:
        url = f"https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}"
        response = requests.get(url)
        data = response.json()
        users.extend(data['data'])
        offset += 20  
    return users[:count] 

data = get_users(160)

for user in data:
    print(user)