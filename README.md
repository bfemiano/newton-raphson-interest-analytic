newton-rahpson-interest-analytic
=================================

Hadoop streaming application written in Python that calculates time-weighted interest using Newton-Rahpson method.
It considers the time of year for each adjustment, both positive and negative, that were made to each account to give a more accurate year-end interest rate. This particular implementation is designed to run in Hadoop streaming. 

Build the data using <code>python data_gen.py <num_accounts></code> where num_accounts equals how many 
unique account names to reproduce in the dataset. 

Data is in the form of (account# adjustment perc_year) where
* account# = unique account identifier,
* adjustment = +/- amount to account, 
* perc_year = days left in the year divided into 1 (ex: day 100 = (365-100)/365 = .72, day 0 = (365- 0)/365 = 1).
1.0 represents the accounts starting balance for the year. 
0.0 represents the accounts year-end balance. 

To use the default shell script first upload the data to hadoop at /fake_investments/in.

Then edit HADOOP_HOME in newton_rahpson.sh and run <code>./newton_rahspon.sh</code>. The partfile output will be under <code>/fake_investments/out</code>. 

The reducer groups by unique account, sorts by time ascending and calculates the time-weighted interest rate on the account using quadratic convergence. Each account gets 25 maximum attempts to converge the difference from the previous attempt below 0.0000001 before exiting. 
For an in-depth explaination of Newton-Rahpson method: http://www.sosmath.com/calculus/diff/der07/der07.html

Times for each account are assumed to be percentages of a common year. The analytic only works on a per-year basis for now. 
1.0 represents the beginning balance (Jan 01) and 0.0 represents the end of year (Dec 31). The reducer sorts by perc_year such that the year end entry appears first to the reducer for each account, and can be used to set the initial year-end value. Right now it's hardcode to only work with the testing dataset. Thus you'll see a hardcoded magic number of 8863.03. 
