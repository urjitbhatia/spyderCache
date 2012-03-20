'''
Created on Mar 10, 2012

@author: urjit
'''

from keyManager import KeyManager
from config import Config
from utils import LogHelper
import httplib
import re


class Topology(object):
    '''
    This class maintains the topology of the network, absorbs the config and 
    becomes self-aware (almost :) and can talk to other nodes like itself.
    
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


    def instructPeer(self, peer, command, path, mirror=False):
        '''
        This method talks to other peers using same HTTP channels as a client, except adds its address for tracing
        Can be improved by having a dedicated control channel? Maybe use low level sockets and listen to multiple
        channels in the same application
        '''
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
            value = response

        except Exception, e:
            #TODO: inform other nodes?
            value = None

            if not mirror:
                self.key_manager.remove_node(peer)
                self.informAboutDownedPeer(peer)
                #===================================================================
                # I know this is a very dirty hack, putting it here for functionality
                # sake and so that I remember to fix this case
                #===================================================================
                self.instructPeer(self.config.node_address, command, path)
                #===================================================================
            else:
                self.logger.error("Mirror is down!! My mirror was: %s" % peer)

            self.logger.error("Peer node seems down: ")
            self.logger.error(e)

        return value

    def mirror(self, command, path):
        '''
        This method sends a mirror request for each activity this node performs.
        '''
        print self.config.mirrors
        
        for mirror in self.config.mirrors:
            print "mirroring to %s" % mirror
            self.instructPeer(mirror, command, path, mirror=True)

    def informAboutDownedPeer(self, dead_peer):
        #=======================================================================
        # For all the peers this node has, other than the node that is down,
        # inform them about it being down.
        #=======================================================================
        print "informing peers %s about dead node %s" % (self.config.peers, dead_peer)
        for peer in self.config.peers:
            if peer == self.config.node_address or peer == dead_peer:
                continue
            instruction = '/' + 'dead' + '/' + str(dead_peer)
            print self.instructPeer(peer, 'HEAD', instruction)
