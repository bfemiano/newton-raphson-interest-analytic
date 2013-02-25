#!/usr/bin/env python
import sys
from math import *
from collections import namedtuple

# fake_data = \
# 'account-0	24125	0.0\n' + \
# 'account-0	19712	1.0\n' + \
# 'account-0	9059	0.57\n' + \
# 'account-0	-7067	0.37\n' +\
# 'account-0	-4326	0.28\n' +\
# 'account-0	6747	0.77\n' + \
# 'account-1	19705	0.0\n' + \
# 'account-1	16061	1.0\n' +\
# 'account-1	3120	0.58\n' +\
# 'account-1	-6646	0.23\n' +\
# 'account-1	8524	0.14\n' +\
# 'account-1	-1354	0.86\n' + \
# 'account-2	47354	0.0\n' + \
# 'account-2	37924	1.0\n' +\
# 'account-2	-222	0.83\n' +\
# 'account-2	3617	0.64\n' +\
# 'account-2	-2463	0.85\n' +\
# 'account-2	5082	0.64\n' +\
# 'account-2	3416	0.43\n' +\
# 'account-3\t8863.06\t0.0\n' +\
# 'account-3\t5382.48\t1.0\n' + \
# 'account-3\t400.0\t0.8904\n' + \
# 'account-3\t500.0\t0.7890\n' + \
# 'account-3\t500.0\t0.6767\n' + \
# 'account-3\t350.0\t0.5589\n' + \
# 'account-3\t-1000.0\t0.4795\n' + \
# 'account-3\t350.0\t0.4630\n' + \
# 'account-3\t350.0\t0.3781\n' + \
# 'account-3\t350.0\t0.2932\n' + \
# 'account-3\t350.0\t0.2100\n' + \
# 'account-3\t350.0\t0.1260\n' + \
# 'account-3\t350.0\t0.0438'
#investments = [[5382.48,1.0000], [400.00,0.8904],[500.00,0.7890], [500.00,0.6767],
#               [350.00,0.5589], [-1000.00,0.4795], [350.00,0.4630], [350.00,0.3781],
#              [350.00,0.2932], [350.00,0.2110], [350.00,0.1260], [350.00,0.0438]]
#year_end_value = 8863.06

# def get_for_key_fake():
#     investments = []
#     prevAccount = 'N/A'
#     for line in fake_data.split('\n'):
#         print line
#         (account, amount, per_year) = line.strip().split('\t')
#         if prevAccount != 'N/A' and account != prevAccount:
#             yield prevAccount, investments
#             investments = []
#         investments.append(Change._make([float(amount), float(per_year)]))
#         prevAccount = account
#     yield prevAccount, investments

Change = namedtuple("Change", ['amount', 'per_year'])

def get_for_key():
    investments = []
    prevAccount = 'N/A'
    for line in sys.stdin:
        (account, per_year, amount) = line.strip().split('\t')
        if prevAccount != 'N/A' and account != prevAccount:
            yield prevAccount, investments
            investments = []
        investments.append(Change._make([float(amount), float(per_year)]))
        prevAccount = account
    yield prevAccount, investments


def main():
    for account,investments in get_for_key():
        max_tries = 1
        starting = investments[0]
        investments.remove(starting)
        year_end_value = starting.amount
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
        print account + '\t' + str(x * 100.0)

if __name__ == "__main__":
    main()