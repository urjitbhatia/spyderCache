'''
This script is a small utility to read the events journal, named as events_journal by default.
The journal stores all the put and delete events so that a node can be reconstructed from the logs
if it goes down.

We use msgpack for reading and writing data into the journal.
'''


import msgpack
import io
import sys

recovery_journal = 'events_journal'

try:
    recovery_journal = str(sys.argv[1])
except:
    print "Usage: python read.py <journal_file>"
    sys.exit()

unpacker = msgpack.Unpacker()
recovery_file = io.open(recovery_journal, mode='rb', buffering=1000)
        
unpacker.feed(recovery_file.read())
        
for command in unpacker:
	print command

