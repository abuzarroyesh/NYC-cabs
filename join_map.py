#!/usr/bin/env python3

import sys

for line in sys.stdin:
  #avoid header
  if "medallion" not in line:
    line = line.strip()
    words = line.split(",")
    hack_license = words[1]
    if len(words) > 11:
      #comes from trips
      pickup = words[5]
    else:
      pickup = words[3]
    print(hack_license + " " + pickup + "\t" + line) 
