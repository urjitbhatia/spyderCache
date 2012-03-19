'''
Created on Mar 10, 2012

@author: urjit
'''

from keyManager import KeyManager
from sets import Set
from config import Config
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

    key_manager = KeyManager()

    #regex to match the node address pattern: ipAddress:port (IPv4 for now)
    remote_pattern = re.compile(r'^([0-9]{1,3}\.){3}[0-9]{1,3}\:[0-9]{4,5}$')
    local_reconstruct = False

    def __init__(self, config):
        '''
        Constructor: 
        This is going to setup the default configuration, if we need to parse the config file, 
        then need to call the configure method
        '''
        self.logger = LogHelper.getLogger()
        self.config = config
        self.logger.info("we are warming up... " + str(self.config.node_id))
        
        #=======================================================================
        # Setup the keyRing using the config...
        #    Also, Add yourself to the list...
        #=======================================================================
        self.key_manager.setupHashRing(self.config.peers, 3)
        self.key_manager.add_node(self.config.node_address)
        

    def connect(self, peer_node):
        '''
        Add a new node as its peers
        '''
        if (self.remote_pattern.match(peer_node)):    #make sure its in the format 'ipAddress:port' (IPv4)

            print "Connecting to new peer: ", peer_node
            self.key_manager.add_node(peer_node)

            print "Now configured as: ", self.key_manager.ring.values()


    def instructPeer(self, peer, command, path):

        self.logger.info(str(self.config.node_id) + " commanding: " + str(peer) + " to " + command + path)
        value = None
        try:
            #===================================================================
            # Append your own address to the request 
            # so that we can break cycles if they happen
            #===================================================================
            url = str(path) + "/" + str(self.config.node_address) + ":"
            
            conn = httplib.HTTPConnection(peer)
            conn.request(method=command, url=url, body='', headers={'Content-length':0})
            response = conn.getresponse().read()
            
            self.logger.info("Response: " + response)
            conn.close()
            
        except Exception, e:
            #TODO: inform other nodes?
            self.logger.error("Peer node seems down: ")
            self.logger.error(e)

        return value
