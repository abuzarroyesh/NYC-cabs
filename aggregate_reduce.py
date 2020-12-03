#!/usr/bin/env python3

from operator import itemgetter
import sys
from datetime import datetime
from datetime import timedelta
from itertools import groupby

##TODO CHANGE T_OFFDUTY FROM MINUTES TO A FRACTION AND THEN TO T_ONDUTY

def read_mapper_output(file):
	for line in file:
		yield line.rstrip().split('\t', 1)

#format of values from mapper output from step4_mockdata.csv
#2013000004,0.2,0.1,1,1,12,6
#0: hack, 1: t_onduty, 2: t_occupied, 3: n_pass, 4: n_trip, 5: n_mile, 6: earnings

def main():
	data = read_mapper_output(sys.stdin)
	for key, group in groupby(data, itemgetter(0)):
		t_onduty = []
		t_occupied = []
		earnings = []
		n_pass = []
		n_trip = []
		n_mile = []
		# Each group is all the rides in that date / hour 
		# Each item in each group is one driver's rides for that date / hour
		for item in group: 
			line = item[1].split(" ")
			t_onduty.append(float(line[1]))
			t_occupied.append(float(line[2]))
			n_pass.append(float(line[3]))
			n_trip.append(float(line[4]))
			n_mile.append(float(line[5]))
			earnings.append(float(line[6]))
		drivers_onduty = len(t_onduty) #counting number of occurrances
		t_onduty = sum(t_onduty)
		t_occupied = sum(t_occupied)
		n_pass = sum(n_pass)
		n_trip = sum(n_trip)
		n_mile = sum(n_mile)
		earnings = sum(earnings)
		
		print(
			key[0:10] + "\t" +
			key[11:13] + "\t" +
			str(drivers_onduty) + "\t" + 
			str(t_onduty) + '\t' + 
			str(t_occupied) + '\t' + 
			str(n_pass) + '\t' + 
			str(n_trip) + '\t' + 
			str(n_mile) + '\t' + 
			str(earnings)
			)

if __name__ == "__main__":
	main()