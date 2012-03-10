'''
Created on Mar 10, 2012

@author: urjit
'''

import logging
from utils import LogHelper
import pickle


class Cache(object):
    '''
    classdocs
    '''
    logger = logging.getLogger('Cache')
    
    disk_persist = False
    diskCache = None
    
    def __init__(self, disk_persist=False):
        '''
        Constructor
        '''
        self.data_map = dict()
        self.disk_persist = disk_persist
        
        if self.disk_persist:
            self.diskCache = DiskCache() 
            
        LogHelper.setupLogging(self.logger)
        
    def store(self, key, value):
        
        data_value = self.data_map[key] if self.data_map.has_key(key) else "--saved--"        
        
        self.data_map[key] = value
        
        if self.disk_persist:
            self.diskCache.persist(self.data_map)
            
        return data_value
        
        
    def fetch(self, key):
        
        return self.data_map[key] if self.data_map.has_key(key) else "--null--"
    
    def erase(self, key):
        
        return self.data_map.pop(key, "--null--")  

class DiskCache(object):
    '''
    classdocs
    '''
    
    def persist(self, data_to_persist):
        #store the cache to the disk
        print pickle.dumps(data_to_persist)