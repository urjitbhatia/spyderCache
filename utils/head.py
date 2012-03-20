'''
Created on Mar 16, 2012

@author: urjit

Perform GETs,PUTs and DELETEs at random
'''

import httplib
import sys
import time

try:
    monitor_file_path = str(sys.argv[1])
    monitor_interval = float(5) #seconds
    if len(sys.argv) == 3:
        monitor_interval = float(sys.argv[2])
except:
    print "Usage: python heartBeatMonitor.py <file with nodelist to monitor> <interval-seconds>"
    sys.exit()

print "Monitoring at a %f second interval" % monitor_interval

monitor_file = open(monitor_file_path, 'r')

monitor_list = []

for line in monitor_file:
    monitor_list.append(line.strip())

try:
    while True:
        for monitor in monitor_list:
            try:
                conn = httplib.HTTPConnection(monitor)
                conn.request(method='HEAD', url='', body='', headers={'Content-length':0})
                response = conn.getresponse().read()
                conn.close()
                print "%s is alive" % monitor
            except Exception, e:
                if conn is not None:
                    conn.close()
                print "%s is dead" % monitor
        time.sleep(monitor_interval)
except KeyboardInterrupt, k:
    print "\nMonitor Closed..."
