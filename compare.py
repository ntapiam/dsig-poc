#!/usr/bin/env python3
import argparse
parser = argparse.ArgumentParser(description='generate comparison against UCR Archive 2018')
parser.add_argument('results', type=argparse.FileType('r'), help='results file generated by main.py')
args=parser.parse_args()

with open('DataSummary.csv', 'r') as fp:
	fp.readline()
	benchmark = {}
	for line in fp:
		line = line.split(',')
		line[8] = line[8].split(' ')[0]
		benchmark[line[2]] = list(map(float,line[7:11]))

improvements = {}
args.results.readline()
args.results.readline()
for line in args.results:
	if line == '\n':
		break
	line = line.split('\t')
	name = line[0]
	dsig = float(line[1])/100.0
	improvements[name] = []
	for rate in benchmark[name]:
		if rate > 0:
			improv = (rate-dsig)/rate
		elif rate == 0 and dsig > 0:
			improv = float('-inf')
		else:
			improv = 0
		improvements[name].append(improv)

with open('improv.txt', 'w') as fp:
	fp.write('Dataset EUC DTW-learn DTW default\n')
	for name, rates in improvements.items():
		fp.write(name + ' ' + ' '.join(map(str,rates)) + '\n')

