"""
System Performance Manager Module

This module manages system performance monitoring tasks including CPU and
memory utilization tracking, and reports data via callback listeners.

License: PIOT-DOC-LIC
@author: Your Name
"""

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask

from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData


class SystemPerformanceManager():
    """
    Manager class for system performance monitoring.
    
    Coordinates CPU and memory utilization tasks and reports
    performance data through a registered data message listener.
    """
    
    def __init__(self):
        """
        Constructor for SystemPerformanceManager.
        
        Initializes the CPU and memory utilization monitoring tasks
        and retrieves the location ID from configuration.
        """
        # Get configuration
        configUtil = ConfigUtil()
        
        # Get location ID from config file
        self.locationID = \
            configUtil.getProperty(
                ConfigConst.CONSTRAINED_DEVICE, 
                ConfigConst.DEVICE_LOCATION_ID_KEY,
                ConfigConst.NOT_SET)
        
        # Initialize CPU and memory utilization tasks
        self.cpuUtilTask = SystemCpuUtilTask()
        self.memUtilTask = SystemMemUtilTask()
        
        # Initialize data message listener reference
        self.dataMsgListener = None
        
        # Initialize utilization tracking variables
        self.cpuUtilPct = 0.0
        self.memUtilPct = 0.0
        
        logging.info("SystemPerformanceManager initialized with location ID: %s", self.locationID)
    
    def handleTelemetry(self):
        """
        Handles telemetry collection from CPU and memory monitoring tasks.
        
        Retrieves current CPU and memory utilization values, creates a
        SystemPerformanceData instance, and notifies the registered listener.
        """
        # Get current CPU and memory utilization
        cpuUtilPct = self.cpuUtilTask.getTelemetryValue()
        memUtilPct = self.memUtilTask.getTelemetryValue()
        
        logging.debug('CPU utilization is %s percent, and memory utilization is %s percent.', 
                     str(cpuUtilPct), str(memUtilPct))
        
        # Create SystemPerformanceData instance
        sysPerfData = SystemPerformanceData()
        sysPerfData.setLocationID(self.locationID)
        sysPerfData.setCpuUtilization(cpuUtilPct)
        sysPerfData.setMemoryUtilization(memUtilPct)
        
        # Notify listener if registered
        if self.dataMsgListener:
            self.dataMsgListener.handleSystemPerformanceMessage(data=sysPerfData)
    
    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        """
        Sets the data message listener for callback notifications.
        
        @param listener The IDataMessageListener instance to register
        @return True if listener was set successfully, False otherwise
        """
        if listener:
            self.dataMsgListener = listener
            logging.info("Data message listener registered: %s", type(listener).__name__)
            return True
        else:
            logging.warning("No data message listener provided. Ignoring.")
            return False
    
    def startManager(self):
        """
        Starts the system performance manager.
        
        This would typically start background tasks or threads for
        continuous monitoring. Currently a placeholder for future implementation.
        """
        logging.info("SystemPerformanceManager started.")
    
    def stopManager(self):
        """
        Stops the system performance manager.
        
        This would typically stop background tasks or threads.
        Currently a placeholder for future implementation.
        """
        logging.info("SystemPerformanceManager stopped.")