#!/usr/bin/env python3

import sys
from datetime import datetime

#1/1/2013,1,2013000004,0.2,0.1,1,1,12,6
#format of step4_mockdata.csv

#0: date, 1: hour, 2: hack, 3: t_onduty, 4: t_occupied, 5: n_pass, 6: n_trip, 7: n_mile, 8: earnings

for line in sys.stdin: 
	line = line.rstrip().split(" ")
	current_date = line[0]
	current_hour = line[1]
	key = str(current_date) + " " + str(current_hour)
	value = line[2] + " " + line[3] + " " + line[4] + " " + line[5] + " " + line[6] + " " + line[7] + " " + line[8] 
	print(key + "\t" + value)

