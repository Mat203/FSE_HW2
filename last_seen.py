import requests
from datetime import datetime, timedelta

def choose_language():
    languages = {
        "1": "en-US",
        "2": "uk-UA"
    }

    print("Please choose a language:")
    print("1. English")
    print("2. Ukrainian")
    choice = input("Enter the language: ")

    return languages.get(choice)

localizations = {
    "en-US": {
        "IsOnline": "is online",
        "JustNow": "was seen just now",
        "LessThanAMinuteAgo": "was seen less than a minute ago",
        "CoupleOfMinutesAgo": "was seen a couple of minutes ago",
        "AnHourAgo": "was seen an hour ago",
        "Today": "was seen today",
        "Yesterday": "was seen yesterday",
        "ThisWeek": "was seen this week",
        "LongTimeAgo": "was seen long time ago"
    },
    "uk-UA": {
        "IsOnline": "в мережі",
        "JustNow": "був у мережі прямо зараз",
        "LessThanAMinuteAgo": "був у мережіменше хвилини тому",
        "CoupleOfMinutesAgo": "був у мережі кілька хвилин тому",
        "AnHourAgo": "був у мережі годину тому",
        "Today": "був у мережі сьогодні",
        "Yesterday": "був у мережі вчора",
        "ThisWeek": "був у мережі на цьому тижні",
        "LongTimeAgo": "був у мережі давно"
    }
}


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

def format_time_diff(diff, lang):
    if diff is None:
        return "is online"
    
    seconds = diff.total_seconds()
    
    if seconds < 30:
        return localizations[lang]["JustNow"]
    elif seconds < 60:
        return localizations[lang]["LessThanAMinuteAgo"]
    elif seconds < 3600:
        return localizations[lang]["CoupleOfMinutesAgo"]
    elif seconds < 7200:
        return localizations[lang]["AnHourAgo"]
    elif diff.days == 0:
        return localizations[lang]["Today"]
    elif diff.days == 1:
        return localizations[lang]["Yesterday"]
    elif diff.days < 7:
        return localizations[lang]["ThisWeek"]
    else:
        return localizations[lang]["LongTimeAgo"]

def print_user_status(user_name, status):
    if status=="is online":
        status = localizations[lang]["IsOnline"]
        print(f"{user_name} {status}")
    else:
        print(f"{user_name} {status}")

data = get_all_data()
lang = choose_language()
for user in data:
    user_name, diff = format_last_seen(user)
    status = format_time_diff(diff, lang)
    print_user_status(user_name, status)
