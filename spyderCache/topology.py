'''
Created on Mar 10, 2012

@author: urjit
'''

from sets import Set
import ConfigParser
import cherrypy
import httplib
import os
import re

class Topology(object):
    '''
    classdocs
    '''
    
    connections = Set()
    node_id = 0
    node_port = 8080
    remote_pattern = re.compile(r'^([0-9]{1,3}\.){3}[0-9]{1,3}\:[0-9]{4,5}$')

    def __init__(self, node_port, node_id):
        '''
        Constructor: 
        This is going to setup the default configuration, if we need to parse the config file, 
        then need to call the configure method
        '''
        self.port_id = node_port
        self.node_id = node_id
        
    def connect(self, remote_host):
        if (self.remote_pattern.match(remote_host)):
            print "Connecting to new peer: ", remote_host
            self.connections.add(remote_host)
            
            print "Now connected to: ", self.connections
    
    def construct(self, config_file):
       
        config = ConfigParser.ConfigParser()
        try:
            config.read(config_file)
            print config.sections()
            self.node_id = config.get('local', 'node_id')
            self.node_port = int(config.get('local', 'node_port')) #Make sure the port is an integer value
            # TODO: check the port from cfg file isnumeric...
            
            if config.has_section('network') and config.has_option('network', 'peer'):
                peers = config.get('network', 'peer').replace('\n', '').split(',')
                self.connections.extend(peers)
                print peers
        except Exception as e:
            print "Incorrect cfg file"
            print e 
            
        return [self.node_id, self.node_port] 

        
    def instruct(self, command, vars):
        print "I am :", self.node_id
        
        print "Command: ", command
        print "vars: ", vars
        
        for address in self.connections:
            print "calling peer... ", address
            conn = httplib.HTTPConnection(address)
            conn.request(command, vars)
            conn.close()
