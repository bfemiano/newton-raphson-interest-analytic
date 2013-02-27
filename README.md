newton-rahpson-interest-analytic
=================================

Hadoop streaming application written in Python that calculates time-weighted interest using Newton-Rahpson method.
Taking into account the time of year any adjustments (positive and negative) that were made to each account. 

Build the data using 'python data_gen.py <num_accounts>' where num_accounts equals how many 
unique account names to reproduce in the dataset. 

Data is in the form of (account# adjustment perc_year) where
'account#'= unique account identifier,
'adjustment' = +/- amount to account, and 
'perc_year' = days left in the year divided into 1 (example day 100 = (365-100)/365 = .72, day 0 = (365- 0)/365 = 1)
1.0 represents the accounts starting balance for the year. 
0.0 represents the accounts year-end balance. 

Upload the data to hadoop at /fake_investments/in.

Edit HADOOP_HOME in newton_rahsphon.sh and run ./newton_rahspon.sh. The partfile output will be under /fake_investments/out. 

The reducer groups by unique account and calculates the time-weighted interest rate on the account using quadratic convergence. Each account gets 25 maximum attempts to converge the difference from the previous attempt below 0.0000001 before exiting. 
See: http://www.sosmath.com/calculus/diff/der07/der07.html

times for each account are assumed to be percentages of a common year. The analytic only works on a per-year basis for now. 
1.0 represents the beginning balance (Jan 01) and 0.0 represents the end of year (Dec 31). The reducer sorts by perc_time such that
the year end entry appears first to the reducer for each account, and can be used to set the year-end value.
