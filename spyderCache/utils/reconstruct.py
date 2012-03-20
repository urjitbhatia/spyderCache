'''
Created on Mar 16, 2012

@author: urjit

Command a node to reconstruct to its previous state using the events journal
'''

import httplib
import sys

try:
    from_ip = sys.argv[1]
    from_port = sys.argv[2]
except:
    print "Usage: python connect.py <from_ip> <from_port> <to_ip> <to_node>"
    sys.exit()

from_node = from_ip + ':' + from_port

print "asking node %s to reconstruct itself using the events log" % from_node
try:
    conn = httplib.HTTPConnection(from_node)
    conn.request(method='HEAD', url='/reconstruct', body='', headers={'Content-length':0})
    response = conn.getresponse().read()
    print response
    conn.close()
except Exception, e:
    if conn is not None:
        conn.close()
    print "%s is probably dead" % from_node 
