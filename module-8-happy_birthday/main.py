from datetime import timedelta, datetime, date
from collections import defaultdict

#users = [{'name': 'Max', 'birthday': datetime(year=2004, month=9, day=10)}, 
#{'name': 'Jack', 'birthday': datetime(year=2004, month=9, day=9)}, 
#{'name': 'Kate', 'birthday': datetime(year=2004, month=9, day=11)}]


def get_birthdays_per_week(users):
    current_day = date.today()
    date_dict=defaultdict(list)
    for user in users:
        month = user['birthday'].month
        day = user['birthday'].day
        hb_this_year = date(year=current_day.year, month=month, day=day)
        if hb_this_year.weekday() == 5:
            hb_this_year = hb_this_year + timedelta(days=2)
        elif hb_this_year.weekday() == 6:
            hb_this_year = hb_this_year + timedelta(days=1)
        if 0 <= (hb_this_year - current_day).days < 7:
            date_dict[hb_this_year.strftime('%A')].append(user['name'])
    for key, value in date_dict.items():
        print(key+':', ', '.join(value))


#get_birthdays_per_week(users)