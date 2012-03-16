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
        self.cache = Cache(reconstruct=self.topology.local_reconstruct)
        self.cache.topology = self.topology
        
        
    def GET(self, key, origin='client'):
        
        if origin == 'client':
            self.logger.info("Request from client")
        else:
            if str(origin) == self.topology.node_address:
                self.logger.error("Houston, we have a problem. Cycle detected. Have to fail...")
                return None
        node = self.topology.key_manager.get_node(key)
        
        self.logger.info("Key requested: " + key)
        self.logger.info("Node responsible: " + node)
        
        if node == self.topology.node_address:  #we are responsible for fetching this key from the cache
            return self.cache.fetch(key)
        else:                                   #tell our peer to handle this key
            return self.topology.instructPeer(node, 'GET', cherrypy.serving.request.path_info) #TODO change faux get/post to auto route
    
    
    def PUT(self, key, value, origin='client'):
        
        if origin == 'client':
            self.logger.info("Request from client")
        else:
            if str(origin) == self.topology.node_address:
                self.logger.error("Houston, we have a problem. Cycle detected. Have to fail...")
                return None
        
        node = self.topology.key_manager.get_node(key)
        
        if node == self.topology.node_address:  #we are responsible for storing this key in the cache
            return self.cache.store(key, value)
        else:                                   #tell our peer to handle this key
            return self.topology.instructPeer(node, 'PUT', cherrypy.serving.request.path_info) #TODO change faux get/post to auto route 
    
        
    def DELETE(self, key, origin='client'):
        
        if origin == 'client':
            self.logger.info("Request from Client")
        else:
            if str(origin) == self.topology.node_address:
                self.logger.error("Houston, we have a problem. Cycle detected. Have to fail...")
                return None
        
        node = self.topology.key_manager.get_node(key)
        
        if node == self.topology.node_address:  #we are responsible for deleting this key from the cache
            return self.cache.erase(key)
        else:                                   #tell our peer to handle this key
            return self.topology.instructPeer(node, 'DELETE', cherrypy.serving.request.path_info) #TODO change faux get/post to auto route
    
    
    def connect(self, remote_address):
        self.topology.connect(remote_address)
    
        
    def reconstruct(self):
        self.cache.diskCache.reconstruct()
    
    #===============================================================================
    # Need to tell the CherryPy engine which methods we need to expose
    #===============================================================================
    #    get.exposed = True
    #    put.exposed = True
    #    delete.exposed = True
    #    connect.exposed = True
    #    reconstruct.exposed = True
    exposed = True
    
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
        },
        '/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
    }
    
    cherrypy.quickstart(Communicator(topology), '/', conf)
    cherrypy.log.screen=False
    
if __name__ == "__main__":
    main()
