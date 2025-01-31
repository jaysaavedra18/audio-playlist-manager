import datetime

today_date = datetime.datetime.now(tz=datetime.timezone.utc).date()
DATE_STRING = today_date.strftime("%Y-%m-%d")
