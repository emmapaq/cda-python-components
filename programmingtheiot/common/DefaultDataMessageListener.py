"""
Default Data Message Listener

A simple placeholder implementation of IDataMessageListener for testing.

@author: Emma
"""

import logging

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData


class DefaultDataMessageListener(IDataMessageListener):
    """
    Simple default implementation of IDataMessageListener.
    
    Logs received messages but doesn't perform any actual processing.
    Useful for testing message flow without full application logic.
    """
    
    def __init__(self):
        """
        Constructor
        """
        logging.info("DefaultDataMessageListener created.")
    
    def handleActuatorCommandMessage(self, data: ActuatorData) -> ActuatorData:
        """
        Handles actuator command messages by logging them.
        """
        if data:
            logging.info("DefaultDataMessageListener: Actuator command received.")
            logging.info(f"  - Name: {data.getName()}")
            logging.info(f"  - TypeID: {data.getTypeID()}")
            logging.info(f"  - Command: {data.getCommand()}")
            return data
        return None
    
    def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
        """
        Handles actuator responses by logging them.
        """
        if data:
            logging.info("DefaultDataMessageListener: Actuator response received.")
            return True
        return False
    
    def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
        """
        Handles generic incoming messages by logging them.
        """
        logging.info(f"DefaultDataMessageListener: Message received on {resourceEnum}")
        logging.debug(f"Payload: {msg}")
        return True
    
    def handleSensorMessage(self, data: SensorData) -> bool:
        """
        Handles sensor messages by logging them.
        """
        if data:
            logging.info("DefaultDataMessageListener: Sensor data received.")
            return True
        return False
    
    def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
        """
        Handles system performance messages by logging them.
        """
        if data:
            logging.info("DefaultDataMessageListener: System performance data received.")
            return True
        return False
    
    def getLatestActuatorDataResponseFromCache(self, name: str = None) -> ActuatorData:
        """
        Placeholder - returns None
        """
        return None
    
    def getLatestSensorDataFromCache(self, name: str = None) -> SensorData:
        """
        Placeholder - returns None
        """
        return None
    
    def getLatestSystemPerformanceDataFromCache(self, name: str = None) -> SystemPerformanceData:
        """
        Placeholder - returns None
        """
        return None
    
    def setSystemPerformanceDataListener(self, listener) -> bool:
        """
        Placeholder
        """
        return True
    
    def setTelemetryDataListener(self, name: str = None, listener = None) -> bool:
        """
        Placeholder
        """
        return True