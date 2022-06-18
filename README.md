To run `python interest_calc.py`

Yup. That's it. The code checked in does an assertion as an inline unit test between this verison and the older_streaming_version. This was so I could verify
correctness as I refactored.

The new version uses SQLlite to create an in-memory database with fake account data of the form:

`account_id, date, balance`

Data is only over one year.

Our goal is to calculate the time weighted [rate of return](https://www.investopedia.com/terms/t/time-weightedror.asp#:~:text=The%20time%2Dweighted%20rate%20of,inflows%20and%20outflows%20of%20money.) (interest) of the year for the data, given a series of deposits and withdrawls. This script can work over any number of
accounts, but for clarity sake I only included one account in the fixture data.

We first use SQL to transform this dataset into a series of records of the form:

`account_id, percentage_year_remaining, balance adjustment +/-`

Where:

`percentage_year_remaining` = value between 0.0 and 1.0. Where 0.0 = Dec 31st and 1.0 = Jan 1st. We consider this the percentage of the year remaining, given the day of the year.

`balance adjustment` = the inflow or outflow of cash. This can be negative if a withdrawl occurred.

Once we have the data in this form, we want to group adjustments by account_id and collect a list of
two-element tuples `(perc_year_remaining, adjustment)`, sorted by `perc_year_remaining` ascending. This is
effectively reverse chronological ordering.

So if we had for example account with the following actions over 2022
```
perc_year_remaining   adjustment
0.01                    200
0.05                   -100
```

We'd put the (0.01, 200) ahead of the (0.05, -100) in the sorted list. This is because we want them in reverse chronological order, and 0.01 is closer to the end of the year (0.0) then 0.05 is.

Since SQLlite doesn't have list datatypes, we can instead use a delimited string with group concat.

Now we have the data in the form we need to calculate the true time-weighted interest growth for every account id using [newton rhapson method](http://www.sosmath.com/calculus/diff/der07/der07.html).