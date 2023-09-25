import requests

def get_data(offset):
    url = f"https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}"
    response = requests.get(url)
    data = response.json()
    return data['data']

def get_all_data():
    offset = 0
    all_data = []

    while True:
        data = get_data(offset)

        if not data:
            break

        all_data.extend(data)
        offset += len(data)

    return all_data

i=0
data = get_all_data()
for user in data:
    print(user)
    i+=1
    print(i)