'''
Created on Mar 16, 2012

@author: urjit

Perform GETs on the given node
'''

import httplib
import sys

try:
    key = sys.argv[1]
    ip = sys.argv[2]
    port = sys.argv[3]
except:
    print "Usage: python get.py <key to get> <ip of node> <port of node>"
    sys.exit()

node = ip + ':' + port

try:
    conn = httplib.HTTPConnection(node)
    conn.request(method='GET', url='/' + key, body='', headers={'Content-length':0})
    response = conn.getresponse().read()
    print response
    conn.close()
except Exception, e:
    if conn is not None:
        conn.close()
    print "%s is dead" % node 
