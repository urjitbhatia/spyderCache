'''
Created on Mar 10, 2012

@author: urjit
'''
import logging

class LogHelper(object):
    
    setup_complete = False
    logger = logging.getLogger('spyderLog')
    
    @staticmethod
    def getLogger():
        if not LogHelper.setup_complete:
            formatter = logging.Formatter('[%(levelname)s] %(message)s')
            
            fileLogHandler = logging.FileHandler(filename='./errors.log', delay=0, mode='a')
            fileLogHandler.setLevel(logging.ERROR)
            fileLogHandler.setFormatter(formatter)
            LogHelper.logger.addHandler(fileLogHandler)
            print "Logging errors to: ", fileLogHandler.baseFilename
            
            infoLogHandler = logging.FileHandler(filename='./info.log',delay=0, mode='a')
            infoLogHandler.setLevel(logging.INFO)
            infoLogHandler.setFormatter(formatter)
            LogHelper.logger.addHandler(infoLogHandler)
            print "Logging info to: ", infoLogHandler.baseFilename
            
            LogHelper.logger.setLevel(logging.INFO)
            LogHelper.setup_complete = True
            
        return LogHelper.logger
