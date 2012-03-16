'''
Created on Mar 10, 2012

@author: urjit
'''

from keyManager import KeyManager
from sets import Set
from utils import LogHelper
import ConfigParser
import cherrypy
import httplib
import logging
import md5
import os
import re


class Topology(object):
    '''
    classdocs
    '''
    
    connections = Set()
    connection_addresses = dict()
    key_manager = KeyManager()
    
    node_id = 0
    node_port = 8080
    node_address = ''
    
    #regex to match the node address pattern: ipAddress:port (IPv4 for now)
    remote_pattern = re.compile(r'^([0-9]{1,3}\.){3}[0-9]{1,3}\:[0-9]{4,5}$')
    local_reconstruct = False

    def __init__(self, node_address, node_port, node_id):
        '''
        Constructor: 
        This is going to setup the default configuration, if we need to parse the config file, 
        then need to call the configure method
        '''
        self.logger = LogHelper.getLogger()
        self.logger.info("we are warming up... " + str(node_id))
        
        self.node_id = node_id
        self.port_id = node_port
        self.node_address = str(node_address) + ':' + str(node_port)
        
        
    def connect(self, peer_node):
        '''
        Add a new node as its peers
        '''
        if (self.remote_pattern.match(peer_node)):    #make sure its in the format 'ipAddress:port' (IPv4)
            
            print "Connecting to new peer: ", peer_node
            self.key_manager.add_node(peer_node)
            
            print "Now configured as: ", self.key_manager.ring.values()
    
    def configure(self, node_address, config_file, replicas=1):
        
        
        print 'reading configuration from : ', config_file
        
        try:
            config = ConfigParser.ConfigParser()
            config.read(config_file)
            
            self.node_id = config.get('local', 'node_id')
            self.node_port = int(config.get('local', 'node_port'))
            
            #update self node address
            self.node_address = str(node_address) + ':' + str(self.node_port)
            # TODO: check the port from cfg file isnumeric...
            
            if config.has_option('local', 'reconstruct') and str(config.get('local', 'reconstruct')).lower() == "true":
                self.local_reconstruct = True
            
            #===================================================================
            # Setup the network topology from the config file
            #===================================================================
            peers = None                                  #list of peers found in the configuration file
            
            if config.has_section('network') and config.has_option('network', 'peer'):
                
                peers = config.get('network', 'peer').replace('\n', '').split(',')
                self.key_manager.setupHashRing(peers, 3)
#                self.logger.info("my peers: ", self.key_manager.ring)

            #Add yourself to the list...
            self.key_manager.add_node(self.node_address)
            
        except Exception as e:
            print "Problem processing the configuration file"
            print e 
            
        return [self.node_id, self.node_port] 
        
    def instructPeer(self, peer, command, path):
        
        self.logger.info(str(self.node_id) + " commanding: " + str(peer) + " to " + command + path)
        value = None
        try:
            url = str(path) + "/" + str(self.node_address) + ":"
            conn = httplib.HTTPConnection(peer)
            conn.request(method=command, url=url, body='', headers={'Content-length':0})
            response = conn.getresponse()
            value = response.read()
            self.logger.info("Response: " + response)
            conn.close()
        except Exception, e:
            #TODO: inform other nodes?
            self.logger.error("Peer node seems down: ")
            self.logger.error(e)
            
        return value
