import httplib
import sys

try:
    load_max = sys.argv[1]
    node = sys.argv[2]
except:
    print "Please pass number of trials argument: Usage- python loadData.py 100 127.0.0.1:8001"
    sys.exit()

try:
    conn = httplib.HTTPConnection(node)
    for i in xrange(0, int(load_max)):
        reqString = '/put' + "/" + str(i) + "/" + str(i+1)
        print reqString
        conn.request('GET', reqString)
        print conn.getresponse().read()
    conn.close()
except Exception as e:
    #TODO: inform other nodes?
    print "Peer node seems down", e
