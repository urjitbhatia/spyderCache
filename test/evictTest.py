'''
Created on Mar 16, 2012

@author: urjit

Perform a series of gets and puts on the node
'''

import httplib
import random
import time
import sys


MAX_ITER = 100
port = '8001'

try:
    port = str(sys.argv[1])
    MAX_ITER = int(sys.argv[2])
except:
    print "Using port: ", port
    print "Using MAX_ITER: ", MAX_ITER

CONN_STRING = '127.0.0.1:%s' % port

key_list = []
for x in xrange(0, MAX_ITER):
    key_list.append(x)

def putTest():
    put_times = []
    for idx, key in enumerate(key_list):
        conn = httplib.HTTPConnection(CONN_STRING)
        path = '/' + str(key) + '/' + str(key)
        t = time.time()
        conn.request(method='PUT', url=path, body='', headers={'Content-length':0})
        response = conn.getresponse()
        put_times.append((time.time() - t))
        conn.close()

    print "avg for 1000 puts ", sum(put_times) / len(put_times)

def getTest():
    get_times = []
    
    for idx, key in enumerate(key_list):
        conn = httplib.HTTPConnection(CONN_STRING)
        path = '/' + str(key)
        t = time.time()
        conn.request(method='GET', url=path, body='', headers={'Content-length':0})
        response = conn.getresponse().read()
    print key, response
    
    if isinstance(response, basestring) and response == '--null--':
        if response == '--null--':
            print "key %s must have been evicted" % key
        elif response.isnumeric() and int(response) != int(key):
            print "key %s does not match expected value" % key
    
    get_times.append((time.time() - t))
    conn.close()

    print "avg for 1000 gets ", sum(get_times) / len(get_times)


putTest()
getTest()
