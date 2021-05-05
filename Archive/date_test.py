from datetime import datetime as dt, date, timedelta

def test(x):
    today = date.today()
    start = today - timedelta(days=today.weekday())
    print(start)
    test_date = dt.strptime(x, "%Y-%m-%d").date()
    return test_date > start

print(test("2021-04-30"))