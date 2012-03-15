'''
Created on Mar 10, 2012

@author: urjit
'''

from cache import Cache
from mhlib import isnumeric
from random import random, Random
from topology import Topology
from utils import LogHelper
import cherrypy
import httplib
import logging
import os
import sys

class Communicator(object):
    '''
    classdocs
    '''

    base_file_path = os.path.abspath('.')
    
    #------------------------------------------------------------------------------ 
    # Logging setup
    #------------------------------------------------------------------------------ 
    logger = LogHelper.getLogger()
    cache = Cache()

    def __init__(self, topology):
        '''
        Constructor
        '''
        #=======================================================================
        # By this time, topology has configured itself based on the config file 
        # or the defaults
        #=======================================================================
        
        self.CURRENT_NODE_ID = topology.node_id
        self.logger.info('setup up comm: ' + str(self.CURRENT_NODE_ID) + '\n')
        
        self.map = dict()
        self.topology = topology
        self.cache.topology = self.topology

        
        
    def get(self, key, origin='client'):
        if origin == 'client':
            print "From Client"
        else:
            if str(origin) == self.topology.node_address:
                print "Houston, we have a problem. Cycle detected. Have to fail"
                return None
            
        self.logger.info("Key requested: " + key)
        
        node = self.topology.key_manager.get_node(key)
        print node
        
        if node == self.topology.node_address:  #we are responsible for fetching this key from the cache
            return self.cache.fetch(key)
        else:                                   #tell our peer to handle this key
            return self.topology.instructPeer(node, 'GET', cherrypy.serving.request.path_info) #TODO change faux get/post to auto route
    
    def put(self, key, value, origin='client'):
        #self.topology.instruct(cherrypy.serving.request.method, cherrypy.serving.request.path_info)
        if origin == 'client':
            print "From Client"
        else:
            if str(origin) == self.topology.node_address:
                print "Houston, we have a problem. Cycle detected. Have to fail"
                return None
        
        node = self.topology.key_manager.get_node(key)
        print node
        print self.topology.key_manager.gen_key(key)
        
        if node == self.topology.node_address:  #we are responsible for storing this key in the cache
            return self.cache.store(key, value)
        else:                                   #tell our peer to handle this key
            return self.topology.instructPeer(node, 'GET', cherrypy.serving.request.path_info) #TODO change faux get/post to auto route 
        
    def delete(self, key, origin='client'):
        
        if origin == 'client':
            print "From Client"
        else:
            if str(origin) == self.topology.node_address:
                print "Houston, we have a problem. Cycle detected. Have to fail"
                return None
        
        node = self.topology.key_manager.get_node(key)
        print node
        
        if node == self.topology.node_address:  #we are responsible for deleting this key from the cache
            return self.cache.erase(key)
        else:                                   #tell our peer to handle this key
            return self.topology.instructPeer(node, 'GET', cherrypy.serving.request.path_info) #TODO change faux get/post to auto route
    
    def connect(self, remote_address):
        self.topology.connect(remote_address)
        
    def reconstruct(self):
        self.cache.diskCache.reconstruct()
    
    #===============================================================================
    # Need to tell the CherryPy engine which methods we need to expose
    #===============================================================================
    get.exposed = True
    put.exposed = True
    delete.exposed = True
    connect.exposed = True
    reconstruct.exposed = True
    
def main():
    my_port = 8080 #default
    my_id = 0 #default
    my_address = '127.0.0.1'
    
    topology = Topology(my_address, my_port, my_id) 

    if len(sys.argv) > 1:
        #=======================================================================
        # Ask Topology to read the config file and 
        # configure itself appropriately
        #=======================================================================
        my_id, my_port = topology.configure(my_address, sys.argv[1])
        print "Running in configured mode: id=%s, port=%s" % (my_id, my_port)
    else:
        print "Running in standalone mode: id=%s, port=%s" % (my_id, my_port)
    
    conf = {
        'global': {
           #just saying you are to run at the localhost port..
            'server.socket_host': my_address,
            'server.socket_port': my_port,
        }
    }
    
    cherrypy.quickstart(Communicator(topology), '/', conf)
    
if __name__ == "__main__":
    main()
