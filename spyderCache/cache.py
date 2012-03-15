'''
Created on Mar 10, 2012

@author: urjit
'''

from diskCache import DiskCache
from utils import LogHelper


class Cache(object):
    '''
    classdocs
    '''
    logger = LogHelper.getLogger()
    
    disk_persist = False
    diskCache = DiskCache()
    
    def __init__(self, disk_persist=False):
        '''
        Constructor
        '''
        self.data_map = dict()
        self.disk_persist = disk_persist
        self.data_map = self.diskCache.reconstruct()
        
    def store(self, key, value):
        
        self.diskCache.journal('put', key, value)
        
        data_value = self.data_map[key] if self.data_map.has_key(key) else "--saved--"        
        
        self.data_map[key] = value
        
        if self.disk_persist:
            self.diskCache.persist(self.data_map)
            
        return data_value

    def fetch(self, key):
        
        return self.data_map[key] if self.data_map.has_key(key) else "--null--"
    
    def erase(self, key):
        
        self.diskCache.journal('delete', key)
        
        return self.data_map.pop(key, "--null--")  