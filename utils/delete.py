'''
Created on Mar 16, 2012

@author: urjit

Perform GETs,PUTs and DELETEs at random
'''

import httplib
import sys
import time

try:
    key = str(sys.argv[1])
    ip = str(sys.argv[2])
    port = str(sys.argv[3]) 
except:
    print "Usage: python delete.py <key> <ip> <port>"
    sys.exit()

node = ip + ':' + port
print "deleting key %s from node a %s second interval" % (key, node)

try:
    conn = httplib.HTTPConnection(node)
    conn.request(method='DELETE', url='/'+key, body='', headers={'Content-length':0})
    response = conn.getresponse().read()
    conn.close()
    print "%s deleted, value was %s" % (key, response)
except Exception, e:
    if conn is not None:
        conn.close()
    print "error: "
    print e
