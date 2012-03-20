'''
Created on Mar 16, 2012

@author: urjit

Connect to a given node on the fly
'''

import httplib
import sys

try:
    from_ip = sys.argv[1]
    from_port = sys.argv[2]
    to_ip = sys.argv[3]
    to_port = sys.argv[4]
except:
    print "Usage: python connect.py <from_ip> <from_port> <to_ip> <to_node>"
    sys.exit()

from_node = from_ip + ':' + from_port
to_node = to_ip + ':' + to_port
try:
    conn = httplib.HTTPConnection(from_node)
    conn.request(method='HEAD', url='/connect' + '/' + to_node, body='', headers={'Content-length':0})
    response = conn.getresponse().read()
    print response
    conn.close()
except Exception, e:
    if conn is not None:
        conn.close()
    print "%s is probably dead" % from_node 
