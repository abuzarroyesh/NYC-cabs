#!/usr/bin/env python3

import sys
from datetime import datetime
from math import floor

def parseUtc(dateStr):
	return datetime(year = int(dateStr[1:5]), month = int(dateStr[6:8]), day = int(dateStr[9:11]), hour = int(dateStr[12:14]), minute = int(dateStr[15:17]), second = int(dateStr[18:20]))

#'2013012129', '2013019831', 'CMT', '1', 'N', '2013-01-01 23:51:20', '2013-01-01 23:56:12', 
#'1', '291', '.80', '-73.9217', '40.743324', '-73.907387', '40.740669', 
# 'CSH', '5.5', '0.5', '0.5', '0', '0', '6.5'] 
#format of join.tsv

# 0: medallion, 1: hack, 2: vender id, 3: rate_code, 4: store_and_fwd_flag, 5: start time, 6: end time, 
# 7: passenger count, 8: trip time in seconds, 9: trip distance in miles, 10: pickup long, 11: pickup lat, 12: dropoff long, 13: dropoff lat
#14: payment type, 15: fare amount, 16: surcharge, 17: mta tax, 18: tip amount, 19: tolls amount, 20: total amount. 
for line in sys.stdin: 
	line = line.strip().split(",")
	hack = line[1]
	start = line[5].strip()
	full_date = parseUtc(start)
	#full_date = full_date.replace(second = 0, minute = 0)
	year = full_date.year
	key = hack + " " + str(year)
	value = line[1] + line[5] + line[6] + line[7] + line[8] + line[9] + line[15] + line[18] 
	print(key + "\t" + value)

