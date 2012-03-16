'''
Created on Mar 16, 2012

@author: urjit

Perform GETs,PUTs and DELETEs at random
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

CONN_STRING = '127.0.0.1:%s'%port

def randomString(length):
    result = ''
    for i in xrange(0, length):
        result += random.choice("random")
        
    return result

key_list = []

for x in xrange(0, MAX_ITER):
    key_list.append(randomString(10))
    
value_list = []

for x in xrange(0, MAX_ITER):
    value_list.append(randomString(10))
    

print len(key_list)
print len(value_list)

def putTest():
    put_times = []
    for idx, key in enumerate(key_list):
        conn = httplib.HTTPConnection(CONN_STRING)
        path = '/' + str(key) + '/' + str(value_list[idx])
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
        response = conn.getresponse()
        get_times.append((time.time() - t))
        conn.close()
        
    print "avg for 1000 gets ", sum(get_times) / len(get_times)

def delTest():
    del_times = []
    for idx, key in enumerate(key_list):
        conn = httplib.HTTPConnection(CONN_STRING)
        path = '/' + str(key)
        t = time.time()
        conn.request(method='DELETE', url=path, body='', headers={'Content-length':0})
        response = conn.getresponse()
        del_times.append((time.time() - t))
        conn.close()
        
    print "avg for 1000 deletes ", sum(del_times) / len(del_times)

putTest()
getTest()    
delTest()
putTest()
delTest()
