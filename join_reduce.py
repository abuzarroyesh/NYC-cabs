#!/usr/bin/env python3
from itertools import groupby
from operator import itemgetter
import sys
from datetime import datetime

def read_mapper_output(file, separator='\t'):
	for line in file:
		yield line.rstrip().split(separator, 1)
		#returns list where key = line[0] and value = line[1]

#From opensource Github code
def parseUtc(dateStr):
	return datetime(year = int(dateStr[0:4]), month = int(dateStr[5:7]), day = int(dateStr[8:10]), hour = int(dateStr[11:13]), minute = int(dateStr[14:16]), second = int(dateStr[18:]))

def check_time(time):
	if time < 10:
		return False
	if time > 7200:
		return False
	return True

def check_dist(dist):
	if dist < 0.001:
		return False
	if dist > 20:
		return False
	return True

def check_pace(pace):
	#in seconds/mile
	if pace < 10:
		return False
	if pace > 7200:
		return False
	return True

def main(separator='\t'):
	data = read_mapper_output(sys.stdin, separator=separator)
	for key, group in groupby(data, itemgetter(0)):
		trip = []
		fare = []
		for item in group:
			value = item[1].split(",") #get the second element in each item (each item)
			if len(value) > 11: #line from trip
				trip.extend(value)
			else: # line from fare
				fare.extend(value[4:])
		#not both trip and fare data
		if len(trip) == 0 or len(fare) == 0:
			continue
		#check reasonable time, distance, pace
		dist = float(trip[9])
		pickup_time = parseUtc(trip[5])
		dropoff_time = parseUtc(trip[6])
		duration = dropoff_time - pickup_time
		time = int(duration.total_seconds())
		if dist == 0:
			pace = 0
		else:
			pace = float(time)/dist		
		#reasonable time length journey
		if check_time(time) and check_dist(dist) and check_pace(pace):
			entry = []
			entry.extend(trip)
			entry.extend(fare)
			print(str(entry) + "\t")


if __name__ == "__main__":
	main()
#
		
