'''
Created on Mar 10, 2012

@author: urjit
'''

from cache import Cache
from mhlib import isnumeric
from random import random, Random
from shovel import task
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
    logger = logging.getLogger('Communicator')
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
        self.map = dict()
        self.topology = topology
        
        LogHelper.setupLogging(self.logger)
        
    def get(self, key):
        self.logger.info("Key requested: " + key)
        return self.cache.fetch(key)
    
    def put(self, key, value):
        self.topology.instruct(cherrypy.serving.request.method, cherrypy.serving.request.path_info)
        return self.cache.store(key, value)
    
        
    def delete(self, key):
        return self.cache.erase(key)
    
    def connect(self, remote_address):
        self.topology.connect(remote_address)
    
    
    #===============================================================================
    # Need to tell the CherryPy engine which methods we need to expose
    #===============================================================================
    get.exposed = True
    put.exposed = True
    delete.exposed = True
    connect.exposed = True
    
@task
def main():
    my_port = 8080 #default
    my_id = 0 #default
    topology = Topology(my_port, my_id) 

    if len(sys.argv) > 1:
        #=======================================================================
        # Ask Topology to read the config file and 
        # configure itself appropriately
        #=======================================================================
        my_id, my_port = topology.construct(sys.argv[1])
        print "Running in configured mode: id=%s, port=%s" % (my_id, my_port)
    else:
        print "Running in standalone mode: id=%s, port=%s" % (my_id, my_port)
    
    conf = {
        'global': {
           #just saying you are to run at the localhost port..
            'server.socket_host': '0.0.0.0',
            'server.socket_port': my_port,
        }
    }
    
    cherrypy.quickstart(Communicator(topology), '/', conf)
    
if __name__ == "__main__":
    main()
