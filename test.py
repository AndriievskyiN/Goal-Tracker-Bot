import datetime
from dateutil.parser import parse

dt = parse("12.1.2023", dayfirst=True).date()


date = datetime.date(2023, 1, 10)


def week_number_of_month(date_value):
    return (date_value.isocalendar()[1] - date_value.replace(day=2).isocalendar()[1] + 1)

print(week_number_of_month(date))
print(week_number_of_month(dt))
