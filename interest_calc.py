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

def get_data():
    return [
        [1, '2013-01-01', 5382.48], 
        [1, '2013-02-10', 5782.48],
        [1, '2013-03-18', 6282.48],
        [1, '2013-04-28', 6782.48], 
        [1, '2013-06-10', 7132.48], 
        [1, '2013-07-08', 6132.48], 
        [1, '2013-07-15', 6482.48],
        [1, '2013-08-14', 6832.48], 
        [1, '2013-09-14', 7182.48],
        [1, '2013-10-14', 7532.48], 
        [1, '2013-11-15', 7882.48], 
        [1, '2013-12-15', 8232.48], 
        [1, '2013-12-31', 8863.06],
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

def newton_raphson_converage_old():
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

def time_weighted_interest(investments):
    """
        Uses Newton-Raphson method. Use quadratic convergance
        to arrive at the true interest rate over the year,
        given all +/- adjustments to the account balance.

        Input: semi-colon delimited string of 
            pipe-delimited pairs (perc_of_year, adjustment)
        Output: time-weighted interest accrued over the year.
    """
    # converts perc1|adj1;perc2|adj2 into [[perc1, adj1], [per2, adj2]]
    investments = [r.split('|') for r in investments.split(';')]
    # convert floating point values.
    investments = list(map(lambda x: [float(x[0]), float(x[1])], 
        investments))
    year_end_value = sum(map(lambda x: x[1], investments))
    investments.remove(investments[0])
    max_tries = 1
    x = 0.1
    f = 0 - year_end_value
    f_prime = 0
    while max_tries < 25:
        for inv in investments:
            f += inv[1] * (1 + x) ** inv[0]
            f_prime += inv[0] * inv[1] * (1 + x) ** (-1 + inv[0])
        if fabs(f/f_prime) <= 0.0000001:
            break
        x -= f/f_prime
        max_tries += 1
        f = 0 - year_end_value
        f_prime = 0
    return x * 100.0

def get_query():
    return """
        WITH prior_balances AS (
            SELECT
                account_id,
                date, 
                balance,
                LAG(balance, 1) 
                    OVER (PARTITION BY account_id ORDER BY date) 
                    AS prior_balance
            FROM account_balance
        ),
        adjustments AS (
            SELECT 
                account_id,
                date,
                CASE 
                    WHEN prior_balance IS NULL THEN balance
                    ELSE balance - prior_balance
                END as adjustment
            FROM prior_balances
        ),
        adjs_and_perc_year_remaining AS (
            SELECT
                account_id, 
                ROUND((365 - CAST(STRFTIME('%j', date) AS INT)) / 365.0, 2) 
                    AS perc_year_remaining,
                ROUND(adjustment, 2) as adjustment
            FROM adjustments
        ),
        concatted AS (
            SELECT 
                account_id, 
                perc_year_remaining || '|' || adjustment as perc_adj_pair
            FROM adjs_and_perc_year_remaining
            ORDER BY account_id, perc_year_remaining ASC
        ),
        group_concatted AS (
            SELECT
                account_id,
                GROUP_CONCAT(perc_adj_pair, ";") as adjustments
            FROM concatted
            GROUP BY account_id
        )
        SELECT 
            account_id, 
            TIME_WEIGHTED_INTEREST(adjustments) 
        FROM group_concatted 
    """
def calc_time_weighted_interest():
    # load the data into an in-memory table.
    try:
        con = sqlite3.connect(':memory:')
        cur = con.cursor()
        cur.execute("CREATE TABLE account_balance " 
           + "(account_id int, date text, balance real)")
        con.commit()
        cur.executemany("INSERT INTO account_balance values " 
        + "(?, ?, ?)", get_data())

        con.create_function("TIME_WEIGHTED_INTEREST", 
           1, time_weighted_interest)
        cur.execute(get_query())
        results = cur.fetchall()
        if len(results) > 0:
            (account_id, interest) = results[0]
            return interest
        else:
            raise Exception("No results in query. Something went wrong.")
    finally:
        con.close()

old_interest = newton_raphson_converage_old()
interest = calc_time_weighted_interest()
print(interest)
print(old_interest)
assert round(old_interest, 2) == round(interest, 2)