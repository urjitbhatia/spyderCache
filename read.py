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

