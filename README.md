newton-rahpson-interest-analytict
=================================

Hadoop streaming application written in Python capable of calculating time-weighted interest using Newton-Rahpson method. 

Build the data using 'python data_gen.py <num_accounts> where num_accounts equals how many 
unique account names to reproduce in the dataset. 

Data is in the form of (account-# adjustment perc_of_year) where
'account#'= unique account identifier,
'adjustment' = +/-1 amount to account, and 
'perc_year' = day of the year divided into 1 (example day 100 = 100/365 = .27).

Upload the data to hadoop at /fake_investments/in.

Edit HADOOP_HOME in newton_rahsphon.sh and run ./newton_rahspon.sh. The partfile output will be under /fake_investments/out. 

The reducer groups by unique account and calculates the time-weighted interest rate on the account using quadratic convergence. Each account gets 25 maximum attempts to converge the weighted interest rate below 0.0000001 before exiting. 
See: http://www.sosmath.com/calculus/diff/der07/der07.html

Time intervals are a % assumed to be a common year. The analytic only works on a per-year basis for now. 
0.0 represents the beginning (Jan 01) and 1.0 represents the end (Dec 31). The reducer sorts by perc_time such that
0.0 entry appears first to the reducer for each accont, and can be used to set the year-end value.
