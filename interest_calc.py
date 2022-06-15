from datetime import date, timedelta
from math import fabs
import sqlite3

def get_old_data_format():
    return [
        [1, 0.0, 8863.06],
        [1, 0.8904, 400.0],
        [1, 0.7890, 500.0],
        [1, 0.6767, 500.0],
        [1, 0.5589, 350.0],
        [1, 1.000, 5382.48],
        [1, 0.4795, -1000.0],
        [1, 0.4630, 350.0],
        [1, 0.3781, 350.0],
        [1, 0.2932, 350.0],
        [1, 0.2110, 350.0],
        [1, 0.1260, 350.0],
        [1, 0.0438, 350.0]
    ]

def get_new_data_format():
    return [
        [1, '2012-01-01', 5382.48], 
        [1, '2012-02-10', 5782.48],
        [1, '2012-03-18', 6282.48],
        [1, '2012-04-28', 6782.48], 
        [1, '2012-06-10', 7132.48], 
        [1, '2012-07-08', 6132.48], 
        [1, '2012-07-15', 6482.48], 
        [1, '2012-08-14', 6832.48], 
        [1, '2012-09-14', 7182.48],
        [1, '2012-10-14', 7532.48], 
        [1, '2012-11-15', 7882.48], 
        [1, '2012-12-15', 8232.48], 
        [1, '2012-12-31', 8863.06]
    ]

def convert_to_date(perc):
    d1 = date(year=2012, month=1, day=1)
    d2 = d1 + timedelta(days=(365 - (perc * 365)))
    return "{date:%F}".format(date=d2)


def transform(): 
    new_data = list(map(lambda x: [x[0], convert_to_date(x[1]), x[2]], sorted(get_old_data_format(), key=lambda x: x[1], reverse=True)))
    balance = 0
    inc_to_balance = []
    for i, r in enumerate(new_data): 
        if i == len(new_data) -1:  # since the last record is the final balance, we don't add the previous balance
            inc_to_balance.append([r[0], r[1], r[2]])
        else:
            balance += r[2]
            inc_to_balance.append([r[0], r[1], balance])
    return inc_to_balance

def newton_rhapson_converage_old():
    old_data = get_old_data_format()
    investments = list(map(lambda x: [x[2], x[1]], sorted(old_data, key=lambda x: x[1])))
    max_tries = 1
    starting = investments[0]
    investments.remove(starting)
    year_end_value = 8863.03
    x = 0.1
    f = 0 - year_end_value
    f_prime = 0
    while max_tries < 25:
        for inv in investments:
            f += inv[0] * (1 + x) ** inv[1]
            f_prime += inv[1] * inv[0] * (1 + x) ** (-1 + inv[1])
        if fabs(f/f_prime) <= 0.0000001:
            break
        x -= f/f_prime
        max_tries += 1
        f = 0 - year_end_value
        f_prime = 0
    return x * 100.0

def newton_rhapson_converge(investments):
    year_end_value = investments[0][0]
    investments.remove(investments[0])
    max_tries = 1
    x = 0.1
    f = 0 - year_end_value
    f_prime = 0
    while max_tries < 25:
        for inv in investments:
            f += inv[0] * (1 + x) ** inv[1]
            f_prime += inv[1] * inv[0] * (1 + x) ** (-1 + inv[1])
        if fabs(f/f_prime) <= 0.0000001:
            break
        x -= f/f_prime
        max_tries += 1
        f = 0 - year_end_value
        f_prime = 0
    return x * 100.0

def get_query():
    return """
        SELECT TODO_BUILD_WINDOWS_QUERY
    """

def calc_time_weighted_interest():
    # load the data into an in-memory table
    con = sqlite3.connect(':memory:')
    cur = con.cursor()
    cur.execute("CREATE TABLE account_balance (account int, date text, balance real)")
    con.commit()
    cur.executemany("insert into account_balance values (?, ?, ?)", get_new_data_format())

    cur.execute(get_query())
    output = cur.fetchall()
    print(output)
    con.close()

#print(transform())
old_data = list(map(lambda x: [x[2], x[1]], sorted(get_old_data_format(), key=lambda x: x[1])))
new_interest = newton_rhapson_converge(old_data)
old_interest = newton_rhapson_converage_old()

assert round(old_interest, 2) == round(new_interest, 2)
calc_time_weighted_interest()