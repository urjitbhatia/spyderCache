'''
Created on Mar 18, 2012

@author: urjit
'''
import ConfigParser

class Config():
    '''
    This class is a simple config elements that is used all over spyderCache engine.
    It has basic building blocks telling what is the node port, address, its peers etc.
    '''

    node_id = 0
    node_port = 8080
    node_address = ''
    cache_size = 1024
    replicas = 3
    peers = []
    local_reconstruct = False
    mirrors = []

    def __init__(self, node_id, node_address, node_port):
        self.node_id = node_id
        self.node_port = node_port
        self.node_address = node_address

    def configure(self, node_address, config_file, replicas=3):

        print 'reading configuration from file: ', config_file

        try:
            config = ConfigParser.ConfigParser()
            config.read(config_file)

            #===================================================================
            # Local node configuration settings
            #===================================================================
            self.node_id = config.get('local', 'node_id')
            self.node_port = int(config.get('local', 'node_port'))
            self.cache_size = int(config.get('local', 'cache_size'))

            #update self node address
            self.node_address = str(node_address) + ':' + str(self.node_port)
            # TODO: check the port from cfg file isnumeric...

            #===================================================================
            # Whether to reconstruct the cache using the event_log
            #===================================================================
            if config.has_option('local', 'reconstruct') and str(config.get('local', 'reconstruct')).lower() == "true":
                self.local_reconstruct = True

            #===================================================================
            # Setup the network topology from the config file
            #===================================================================

            if config.has_section('network') and config.has_option('network', 'peers'):
                self.peers = config.get('network', 'peers').replace('\n', '').split(',')
            
            if config.has_section('network') and config.has_option('network', 'mirrors'):
                self.mirrors = config.get('network', 'mirrors').replace('\n', '').split(',')

        except Exception as e:
            print "Problem processing the configuration file"
            print e

        return [self.node_id, self.node_port]
