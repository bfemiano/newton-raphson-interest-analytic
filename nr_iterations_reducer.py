#!/usr/bin/env python
import sys
from math import *
from collections import namedtuple

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
        year_end_value = 8863.03
        sys.stdout.flush()
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