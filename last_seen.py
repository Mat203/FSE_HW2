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

def parse_last_seen_date(last_seen_str):
    tz_info = last_seen_str[-6:]
    last_seen_str = last_seen_str.replace('T', ' ')
    if '.' in last_seen_str:
        time_parts = last_seen_str.split('.')
        time_parts[1] = time_parts[1][:6] if len(time_parts[1]) > 6 else time_parts[1]
        last_seen_str = '.'.join(time_parts)
    last_seen_str = last_seen_str.split('+')[0]
    return datetime.strptime(last_seen_str, '%Y-%m-%d %H:%M:%S.%f'), tz_info

def adjust_timezone(last_seen, tz_info):
    sign = tz_info[0]
    hours = int(tz_info[1:3])
    
    if sign == '+':
        return last_seen - timedelta(hours=hours)
    elif sign == '-':
        return last_seen + timedelta(hours=hours)
    
def format_last_seen(user):
    user_name = user['nickname']
    last_seen_str = user['lastSeenDate']
    
    if last_seen_str:
        last_seen, tz_info = parse_last_seen_date(last_seen_str)
        last_seen = adjust_timezone(last_seen, tz_info)
    else:
        last_seen = None

    now = datetime.now()
    diff = now - last_seen if last_seen else None

    return user_name, diff

def format_time_diff(diff):
    if diff is None:
        return "is online"
    
    seconds = diff.total_seconds()
    
    if seconds < 30:
        return "just now"
    elif seconds < 60:
        return "less than a minute ago"
    elif seconds < 3600:
        return "couple of minutes ago"
    elif seconds < 7200:
        return "an hour ago"
    elif diff.days == 0:
        return "today"
    elif diff.days == 1:
        return "yesterday"
    elif diff.days < 7:
        return "this week"
    else:
        return "long time ago"

data = get_all_data()
for user in data:
    user_name, diff = format_last_seen(user)
    status = format_time_diff(diff)
    print(user_name, status)
