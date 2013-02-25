newton-rahpson-interest-analytict
=================================

Hadoop streaming application written in python capable of calculating time-weighted interest using Newton-Rahpson method. 

Build the data using 'python data_gen.py <num_accounts>'. 

Upload the data to hadoop at /fake_investments/in.

Run the script ./newton_rahspon.sh. The partfile output will be under /fake_investments/out. 

The reducer groups by unique account and calculates the time-weighted interest using quadratic convergence on each investment amount. 
http://www.sosmath.com/calculus/diff/der07/der07.html

time intervals are a % assumed to be a common year. The analytic only works on a per-year basis for now. 

0.0 represents the beginning (Jan 01) and 1.0 represents the end (Dec 31).
