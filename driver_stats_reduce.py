#!/usr/bin/env python3

from operator import itemgetter
import sys
from datetime import datetime
from datetime import timedelta
from itertools import groupby

#TODO sanity check all trips: stuff except t_occ is off

def read_mapper_output(file, separator = '\t'):
	for line in file:
		yield line.rstrip().split(separator, 1)

def main(separator='\t'):
	data = read_mapper_output(sys.stdin, separator = separator)
	for key, group in groupby(data, itemgetter(0)):
		this_driver = []
		#key is both the hack_license and the year, so each group is a unique driver's records for that year
		for item in group:
			value = item[1]
			value = value.replace("'","")
			value = value.split()
			value[1] = value[1] + " " + value[2]
			value.pop(2)
			value[2] = value[2] + " " + value[3]
			value.pop(3)
		#0: hack license, 1: start date and start time, 2: end date and end time, 3: passenger count, 4:trip in seconds, 5:trip in miles, 6:fare amount, 7:tip amount
			this_driver.append(value)
		#now we perform operations on this list
		#sort this by the date
		this_driver = sorted(this_driver, key = lambda x: x[1])
		for i in range(len(this_driver)):
			this_driver[i][1] = datetime.strptime(this_driver[i][1], '%Y-%m-%d %H:%M:%S') 
			this_driver[i][2] = datetime.strptime(this_driver[i][2], '%Y-%m-%d %H:%M:%S')
		
		#initialize list of stats for the first hour of this driver's driving time
		this_hour  = this_driver[0][1].hour 
		this_date = this_driver[0][1].date().strftime("%Y-%m-%d")
		hack = this_driver[0][0]
		#we are still reading in the first line, so will get this info when we do
		t_offduty = 0
		t_occupied = 0
		n_pass = 0
		n_trip = 0
		n_mile = 0
		earnings = 0

		for i in range(0,len(this_driver)):
			#if anything is in mangled form, skip it
			if len(this_driver[i]) != 8:
				continue
			try: 
				x = float(this_driver[i][6])
				x = float(this_driver[i][7])
			except ValueError:
				continue
				
		#	print(this_driver[i]) #the current trip
			if this_driver[i][1].hour == this_hour and this_driver[i][2].hour == this_hour: # if the start hour and end hour of this trip is the same as the current hour we are keeping track of (which is the start time of the last trip-- i.e. this_driver[i-1][1].hour)
				#checks if this trip starts before last ends (an error in the data); changes entry to have start time coinciding with past end time
				if i != 0:
					if this_driver[i][1] < this_driver[i-1][2]:
						this_driver[i][1] = this_driver[i-1][2]
				
				n_pass += int(this_driver[i][3])
				n_trip += 1
				t_occupied += (this_driver[i][2] - this_driver[i][1]).total_seconds()/3600
				n_mile += float(this_driver[i][5])
				earnings += float(this_driver[i][6]) + float(this_driver[i][7])
				
				if i != 0:
					time_since = this_driver[i][1] - this_driver[i-1][2] #time since the last trip ended

					if time_since > timedelta(minutes = 30): 
						t_offduty += time_since.total_seconds()/3600 # fraction of an hour idle between these rides, only counts if at least 30m elapsed

				#no need to print until we have moved onto a new hour
			else: #we have moved onto a new hour, or we are in a trip that spans multiple hours, or both

				#checks if this trip starts before last ends (an error in the data)); changes entry to have start time coinciding with past end time
				if i != 0:
					if this_driver[i][1] < this_driver[i-1][2]:
						this_driver[i][1] = this_driver[i-1][2]

				#if we are on a new hour
				if this_driver[i][1].hour != this_hour:
					#spit out our values for the hour we have; and reset
					time_since = this_driver[i][1] - this_driver[i-1][2]
					t_offduty_nexthour = 0 
					if time_since > timedelta(minutes = 30):
						#take subtraction from the old hour's ceiling as the time off duty for that hour
						t_offduty += ((this_driver[i-1][2].replace(second = 0, minute = 0) + timedelta(hours = 1)) - this_driver[i-1][2]).total_seconds()/3600
						t_offduty_nexthour += (this_driver[i][1] - this_driver[i][1].replace(second = 0, minute = 0)).total_seconds()/3600

					#report our values for the hour we have
					t_onduty = 1 - t_offduty
					print(this_date, this_hour, hack, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings) 
					#reset variables, if we're not going into the next loop
					this_hour = this_driver[i][1].hour
					this_date = this_driver[i][1].date().strftime("%Y-%m-%d")
					t_offduty = t_offduty_nexthour
					#if we're not going into the next loop, these variables are a bit different
					if not (this_driver[i][2].hour - this_driver[i][1].hour > 0):
						t_occupied = (this_driver[i][2] - this_driver[i][1]).total_seconds()/3600
						n_pass = int(this_driver[i][3])
						n_trip = 1
						n_mile = float(this_driver[i][5])
						earnings = float(this_driver[i][6]) + float(this_driver[i][7])
					else:
						t_occupied, n_pass, n_trip, n_mile, earnings = 0,0,0,0,0



				#if we are in a trip that spans multiple hours, do the following
				if this_driver[i][2].hour - this_driver[i][1].hour > 0: 

					#in these cases we want to attribute some miles, earnings, t_offduty and t_occupied to the middle hours (e.g. for a ride from 3-6, add values to 4 to 5)
					hour_counter = this_driver[i][1].replace(second = 0, minute = 0) #floor the starting hour
					curr_end_time = hour_counter + timedelta(hours = 1) #latest pt in the hour where ride is happening

					#while we are iterating through each of the hours of this ride
					while(hour_counter < this_driver[i][2]):
						#calculate proportion of total ride within current hour
						total_trip_time = this_driver[i][2] - this_driver[i][1]
						if hour_counter == this_driver[i][1].replace(second = 0, minute = 0): #if on first iteration through (where start time = real start time)
							curr_start_time = this_driver[i][1] #set current time to be the real start time
						else: 
							curr_start_time = hour_counter #otherwise, on a middle hour and count the current start time as that hour floored

						if curr_end_time > this_driver[i][2]: #if we are in the last hour
							curr_end_time = this_driver[i][2] #set end time to real end time

						prop_trip_in_hour = (curr_end_time - curr_start_time) / total_trip_time
						#print("prop", prop_trip_in_hour, this_driver[i], curr_start_time, curr_end_time)
						# attribute correct proportion to the hour
						n_mile += float(this_driver[i][5]) * prop_trip_in_hour
						
						earnings += (float(this_driver[i][6]) + float(this_driver[i][7])) * prop_trip_in_hour
						t_occupied += (curr_end_time - curr_start_time).total_seconds()/3600
						time_since = curr_start_time - curr_start_time.replace(second = 0, minute = 0)
						if time_since > timedelta(minutes = 30):
							t_offduty += time_since.total_seconds()/3600
						else:
							t_offduty += 0
						#if we are in the first hour, these are the values for these two
						if curr_start_time == this_driver[i][1]:
							n_pass += int(this_driver[i][3])
							n_trip += 1
						else:
							n_pass = 0
							n_trip = 0

						#if we are on the last hour, keep our variables and go through the original loop on line 48
						if curr_end_time == this_driver[i][2] and not (curr_end_time.second == 0 and curr_end_time.minute == 0): #exception of if we have rolled over into new hour just barely
							this_hour = this_driver[i][2].hour
							this_date = this_driver[i][2].date().strftime("%Y-%m-%d")
							break
						else: 
							t_onduty = 1 - t_offduty
							print(this_date, hour_counter.hour, hack, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings)

							#reset values
							t_offduty = 0
							t_occupied = 0
							n_pass = 0
							n_trip = 0
							n_mile = 0
							earnings = 0
						hour_counter += timedelta(hours = 1)
						curr_end_time += timedelta(hours = 1)
					#update our running hour after all these shenanigans
					this_hour = this_driver[i][2].hour


		#print last hour of last day's variables
		t_onduty = 1 - t_offduty
		print(this_date, this_hour, hack, t_onduty, t_occupied, n_pass, n_trip, n_mile, earnings)

main()		
