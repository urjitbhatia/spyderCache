'''
Created on Mar 10, 2012

@author: urjit
'''
import logging

class LogHelper(object):
    
    @staticmethod
    def setupLogging(logger):
        
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        
        consoleLogger = logging.StreamHandler()
        consoleLogger.setLevel(logging.INFO)
        consoleLogger.setFormatter(formatter)
        logger.addHandler(consoleLogger)
        
        fileLogger = logging.FileHandler(filename='errors.log')
        fileLogger.setLevel(logging.ERROR)
        fileLogger.setFormatter(formatter)
        logger.addHandler(fileLogger)
    


