'''
Created on Mar 16, 2012

@author: urjit

Perform GETs,PUTs and DELETEs at random
'''

import httplib
import sys

try:
    key = sys.argv[1]
    value = sys.argv[2]
    ip = sys.argv[3]
    port = sys.argv[4]
except:
    print "Usage: python get.py <key> <value> <ip> <port of node>"
    sys.exit()

node = ip + ':' + port
print node
try:
    conn = httplib.HTTPConnection(node)
    conn.request(method='PUT', url='/' + key + '/' + value, body='', headers={'Content-length':0})
    response = conn.getresponse().read()
    print response
    conn.close()
except Exception, e:
    if conn is not None:
        conn.close()
    print "%s is dead" % node 
