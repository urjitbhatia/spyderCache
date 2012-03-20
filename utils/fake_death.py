'''
Created on Mar 16, 2012

@author: urjit

tell a node that its peer is dead
'''

import httplib
import sys

try:
    from_ip = sys.argv[1]
    from_port = sys.argv[2]
    to_ip = sys.argv[3]
    to_port = sys.argv[4]
except:
    print "Usage: python fake_death.py <from_ip> <from_port> <to_ip> <to_node>"
    sys.exit()

from_node = from_ip + ':' + from_port
to_node = to_ip + ':' + to_port
print "telling node %s that its peer %s is dead" % (from_node, to_node)
try:
    conn = httplib.HTTPConnection(from_node)
    conn.request(method='HEAD', url='/dead' + '/' + to_node, body='', headers={'Content-length':0})
    response = conn.getresponse().read()
    print response
    conn.close()
except Exception, e:
    if conn is not None:
        conn.close()
    print "%s is probably dead" % from_node 
