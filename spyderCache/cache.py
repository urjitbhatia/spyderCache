'''
Created on Mar 10, 2012

@author: urjit
'''

from diskCache import DiskCache
from lruDict import LRUDict
from utils import LogHelper


class Cache(object):
    '''
    This is a wrapper class around the LRU cache. It provides simplified interface
    to store and retreive values from the underlying LRU cache.
    '''
    logger = LogHelper.getLogger()

    disk_persist = False
    diskCache = DiskCache()

    def __init__(self, reconstruct, disk_persist=False):
        '''
        Constructor
        '''
        print reconstruct
#        self.data_map = dict()
        self.data_map = LRUDict()
        
        #TODO: not implemented full disk persistence yet, only journaling
        self.disk_persist = disk_persist

        '''
        Need to check this...
        '''
        if reconstruct:
            self.data_map = self.diskCache.reconstruct()

    def store(self, key, value):

        #Log the event to the journal
        self.diskCache.journal('put', key, value)

#        data_value = self.data_map[key] if self.data_map.has_key(key) else "--saved--"
        data_value = self.data_map[key] if self.data_map.__contains__(key) else "--saved--"

        self.data_map[key] = value

        if self.disk_persist:
            self.diskCache.persist(self.data_map)

        return data_value

    def fetch(self, key):
        #No need to log the fetch event to the journal, won't help us reconstruct the cache
#        return self.data_map[key] if self.data_map.has_key(key) else "--null--"
        return self.data_map[key] if self.data_map.__contains__(key) else "--null--"

    def erase(self, key):

#        if self.data_map.has_key(key):
        if self.data_map.__contains__(key):
            #===================================================================
            # No need to journal deletes for keys that you dont have
            #===================================================================
            self.diskCache.journal('delete', key)
            self.data_map.__delitem__(key)
            return self.data_map.get(key)
        return "--null--"
