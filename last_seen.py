import requests
from datetime import datetime, timedelta

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

def format_last_seen(user):
    user_name = user['nickname']
    last_seen_str = user['lastSeenDate']
    if last_seen_str:
        last_seen_str = last_seen_str.replace('T', ' ')
        if '.' in last_seen_str:
            time_parts = last_seen_str.split('.')
            print(last_seen_str)
            time_parts[1] = time_parts[1][:6] if len(time_parts[1]) > 6 else time_parts[1]
            last_seen_str = '.'.join(time_parts)
        last_seen_str = last_seen_str.split('+')[0]
        last_seen = datetime.strptime(last_seen_str, '%Y-%m-%d %H:%M:%S.%f')
        tz_info = last_seen_str[-6:]
        sign = tz_info[0]
        hours = int(tz_info[1:3])
        last_seen_str = last_seen_str[:-6]
    
        if sign == '+':
            last_seen -= timedelta(hours=hours)
        elif sign == '-':
            last_seen += timedelta(hours=hours)
        print(last_seen)
    
    else:
        last_seen = None

    now = datetime.now()
    diff = now - last_seen if last_seen else None

    return user_name, diff

i=0
data = get_all_data()
for user in data:
    print(user)
    user_name, diff = format_last_seen(user)
    i+=1
    print(i)