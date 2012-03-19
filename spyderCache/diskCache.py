'''
Created on Mar 15, 2012

@author: urjit
'''

from lruDict import LRUDict
import io
import msgpack


class DiskCache(object):
    '''
    This class provides a journaling mechanism for logging events that
    are pushed onto this node.
    We can use the events log file to reconstruct the cache when a node
    goes down and then is restored/moved to another machine.
    '''
    #===========================================================================
    # Possible modes: 
    # 1. Buffered - flush events after buffer is full
    # 2. Realtime - journal events as they occur
    #===========================================================================
    mode = ''
    journal_path = './events_journal'
    old_journals = []
    max_journal_size = 1024
    
    
    def __init__(self, mode='buffered'):
        self.mode = mode

        #=======================================================================
        # self.journal_file = open(self.journal_path, 'a', 0) - 
        # last arg is 0 since we want to flush immediately
        # Immediate flush mode is 'slow' 
        #=======================================================================
        self.journal_file = open(self.journal_path, 'a')
        self.packer = msgpack.Packer()
        
        
    '''
    This method adds an entry into the events_journal
    '''
    def journal(self, command, key, value=None):
        #store the cache to the disk
        self.journal_file.write(self.packer.pack([command, key, value]))
    
    '''
    This method takes an event journal and reconstructs the cache
    '''
    def reconstruct(self, recovery_journal='./events_journal'):
        print "Reconstructing from journal: %s" % recovery_journal
        cache = LRUDict()
        
        unpacker = msgpack.Unpacker()
        recovery_file = io.open(recovery_journal, 'rb', buffering=1024)
        
        unpacker.feed(recovery_file.read())
        
        for command, key, value in unpacker:
            if command == 'put':
                cache[key] = value
            else:
                cache.pop(key)
                
        #return the cache we built from the journal
        return cache
            
