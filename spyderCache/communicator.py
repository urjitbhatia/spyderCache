'''
Created on Mar 10, 2012

@author: urjit
'''

from cache import Cache
from topology import Topology, Config
from utils import LogHelper
import cherrypy
import os
import sys

class Communicator(object):
    '''
    Communicator talks to the client and recieves commands from the client
    in terms of HTTP GET, PUT and DETELE verbs.
    '''

    base_file_path = os.path.abspath('.')

    #------------------------------------------------------------------------------ 
    # Logging setup
    #------------------------------------------------------------------------------ 
    logger = LogHelper.getLogger()

    def __init__(self, config):
        '''
        Constructor
        '''
        #=======================================================================
        # By this time, topology has configured itself based on the config file 
        # or the defaults
        #=======================================================================
        self.config = config
        self.topology = Topology(config)
        
        print self.config.local_reconstruct
        print type(self.config.local_reconstruct)
        
        self.cache = Cache(reconstruct=self.config.local_reconstruct)

        self.logger.info('setup up communicator for node: ' + str(self.config.node_id) + '\n')


    def GET(self, key, origin='client'):

        if origin == 'client':
            self.logger.info("Request from client")
        else:
            if str(origin) == self.config.node_address:
                self.logger.error("Houston, we have a problem. Cycle detected. Have to fail...")
                return None
        node = self.topology.key_manager.get_node(key)

        self.logger.info("Key requested: " + key)
        self.logger.info("Node responsible: " + node)

        if node == self.config.node_address:  #we are responsible for fetching this key from the cache
            return self.cache.fetch(key)
        else:                                   #tell our peer to handle this key
            return self.topology.instructPeer(node, 'GET', cherrypy.serving.request.path_info) #TODO change faux get/post to auto route


    def PUT(self, key, value, origin='client'):

        if origin == 'client':
            self.logger.info("Request from client")
        else:
            if str(origin) == self.config.node_address:
                self.logger.error("Houston, we have a problem. Cycle detected. Have to fail...")
                return None

        node = self.topology.key_manager.get_node(key)

        if node == self.config.node_address:  #we are responsible for storing this key in the cache
            return self.cache.store(key, value)
        else:                                   #tell our peer to handle this key
            return self.topology.instructPeer(node, 'PUT', cherrypy.serving.request.path_info) #TODO change faux get/post to auto route 


    def DELETE(self, key, origin='client'):

        if origin == 'client':
            self.logger.info("Request from Client")
        else:
            if str(origin) == self.config.node_address:
                self.logger.error("Houston, we have a problem. Cycle detected. Have to fail...")
                return None

        node = self.topology.key_manager.get_node(key)

        if node == self.config.node_address:  #we are responsible for deleting this key from the cache
            return self.cache.erase(key)
        else:                                   #tell our peer to handle this key
            return self.topology.instructPeer(node, 'DELETE', cherrypy.serving.request.path_info) #TODO change faux get/post to auto route

    
    def HEAD(self, key=None, value=None):
        print "head called"
        if key is None:
            #===================================================================
            # This is a simple heartbeat check, do nothing
            #===================================================================
            return "alive"
        if key == 'connect':
            self.topology.connect(value)
        elif key == 'reconstruct':
            self.cache.diskCache.reconstruct()

    #===============================================================================
    # Need to tell the CherryPy engine to expose this class as a web-servlet definition
    #===============================================================================
    exposed = True

def main():
    #===========================================================================
    # Default Settings
    #===========================================================================
    my_port = 8080
    my_id = 0
    my_address = '127.0.0.1'

    #===========================================================================
    # This object contains the basic config block for the whole engine to share
    #===========================================================================
    config = Config(my_address, my_port, my_id)

    if len(sys.argv) > 1:
        #=======================================================================
        # Ask Topology to read the config file and 
        # configure itself appropriately
        #=======================================================================
        my_id, my_port = config.configure(my_address, sys.argv[1])
        print "Running in configured mode: id=%s, port=%s" % (my_id, my_port)
    else:
        print "Running in standalone mode: id=%s, port=%s" % (my_id, my_port)

    conf = {
        'global': {
           #just saying you are to run at the my_port port and my_address ip-address..
            'server.socket_host': my_address,
            'server.socket_port': my_port,
        },
        '/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
    }

    cherrypy.quickstart(Communicator(config), '/', conf)

if __name__ == "__main__":
    main()
