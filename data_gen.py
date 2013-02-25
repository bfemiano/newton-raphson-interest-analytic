__author__ = 'bfemiano'
import sys

def main():
    out = open('data.txt', 'w')
    args = sys.argv[1:]
    total_records = int(args[0])
    for i in xrange(0, total_records):
        out.write('account' + str(i) +  '\t0.0\t8863.06\n')
        out.write('account' + str(i) + '\t0.8904\t400.00\n')
        out.write('account' + str(i) + '\t0.7890\t500.00\n')
        out.write('account' + str(i) + '\t0.6767\t500.00\n')
        out.write('account' + str(i) + '\t0.5589\t350.00\n')
        out.write('account' + str(i) + '\t1.0000\t5382.48\n')
        out.write('account' + str(i) + '\t0.4795\t-1000.00\n')
        out.write('account' + str(i) + '\t0.4630\t350.00\n')
        out.write('account' + str(i) + '\t0.3781\t350.00\n')
        out.write('account' + str(i) + '\t0.2932\t350.00\n')
        out.write('account' + str(i) + '\t0.2110\t350.00\n')
        out.write('account' + str(i) + '\t0.1260\t350.00\n')
        out.write('account' + str(i) + '\t0.0438\t350.00\n')
    out.close()

if __name__ == "__main__":
    main()