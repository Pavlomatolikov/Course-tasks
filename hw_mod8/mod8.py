from collections import defaultdict
from datetime import datetime, timedelta
from locale import currency

"""user_list = [{'name': 'John', 'birthday': datetime(
    year=2012, month=9, day=17)}, {'name': 'John', 'birthday': datetime(
        year=2012, month=9, day=17)}]"""


def get_birthdays_per_week(users):
    # today = datetime.now().date()
    today = datetime(
        year=2022, month=9, day=19).date()
    current_year = today.year
    current_week_number = today.isocalendar().week
    result = defaultdict(list)
    for i in users:
        birthday = i['birthday'].date().replace(year=current_year)
        day_name = birthday.strftime('%A')
        delta = i['birthday'].date().replace(year=current_year) - today
        if birthday.isocalendar().week == current_week_number and birthday.weekday() not in (5, 6) and delta.days >= 0:
            result[day_name].append(i['name'])
            print(result)
        elif birthday.isocalendar().week - current_week_number == -1 and birthday.weekday() in (5, 6) and today.weekday() == 0:
            result['Passed ' + day_name].append(i['name'])
            print(result)
        for key in result:
            print(f"{key}:", ", ".join(result[key]))
