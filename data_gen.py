__author__ = 'bfemiano'
import sys
import random

def main():
    out = open('data.txt', 'w')
    args = sys.argv[1:]
    total_records = int(args[0])
    for i in xrange(0, total_records):
        seed = random.randint(0, 100000)
        ran_adjs = random.randint(4, 5)
        j = 0
        out.write('account-'+str(i) + '\t1.0\t' + str(seed) + '\n')
        while j < ran_adjs:
            amount = random.randint(0, 10000)
            neg = random.randint(0, 100)
            if neg <= 5: #%5 chance we get a negative number
                amount = 0 - amount
            if seed + amount >= 0:
                j+=1
                per_of_year = float(random.randint(0, 100))/100.0
                out.write('account-' + str(i) + '\t' + str(per_of_year) + '\t' + str(amount) + '\n')
                seed += amount
        out.write('account-'+str(i) + '\t0.0\t' + str(seed) + '\n')
    out.close()
if __name__ == "__main__":
    main()