"""
Interface for data message listeners.

Defines callback methods that implementing classes must provide
for handling incoming data messages from various sources (MQTT, CoAP, sensors, etc.).

@author: Emma
"""

from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from programmingtheiot.common.ITelemetryDataListener import ITelemetryDataListener
from programmingtheiot.common.ISystemPerformanceDataListener import ISystemPerformanceDataListener


class IDataMessageListener():
    """
    Interface definition for data message listener clients.
    
    This interface defines the contract for classes that need to receive and process
    various types of data messages including sensor data, actuator commands, and
    system performance data.
    """
    
    def getLatestActuatorDataResponseFromCache(self, name: str = None) -> ActuatorData:
        """
        Retrieves the named actuator data (response) item from the internal data cache.
        
        @param name The name of the actuator (optional)
        @return ActuatorData The latest actuator response data, or None if not found
        """
        pass
    
    def getLatestSensorDataFromCache(self, name: str = None) -> SensorData:
        """
        Retrieves the named sensor data item from the internal data cache.
        
        @param name The name of the sensor (optional)
        @return SensorData The latest sensor data, or None if not found
        """
        pass
    
    def getLatestSystemPerformanceDataFromCache(self, name: str = None) -> SystemPerformanceData:
        """
        Retrieves the named system performance data from the internal data cache.
        
        @param name The name of the system performance metric (optional)
        @return SystemPerformanceData The latest system performance data, or None if not found
        """
        pass
    
    def handleActuatorCommandMessage(self, data: ActuatorData) -> ActuatorData:
        """
        Callback function to handle an actuator command message packaged as a ActuatorData object.
        
        This method is called when an actuator command is received (typically from the GDA
        via MQTT or CoAP). The implementing class should process the command and return
        a response ActuatorData object with the response flag set to True.
        
        @param data The ActuatorData message received.
        @return ActuatorData An ActuatorData message that contains the same content as 'data',
        but with the response flag set to True and updated state information.
        """
        pass
    
    def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
        """
        Callback function to handle an actuator command response packaged as a ActuatorData object.
        
        This method is called when an actuator response is received (typically after
        sending a command to an actuator). This is for processing the result of
        actuator operations.
        
        @param data The ActuatorData message received.
        @return bool True on success; False otherwise.
        """
        pass
    
    def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
        """
        Callback function to handle incoming messages on a given topic with
        a string-based payload.
        
        This is a generic message handler that receives raw messages (typically JSON strings)
        and routes them to appropriate specialized handlers based on the resource type.
        
        @param resourceEnum The topic enum associated with this message.
        @param msg The message received. It is expected to be in JSON format.
        @return bool True on success; False otherwise.
        """
        pass
    
    def handleSensorMessage(self, data: SensorData) -> bool:
        """
        Callback function to handle a sensor message packaged as a SensorData object.
        
        This method is called when sensor data is received or generated. The implementing
        class should process the sensor data appropriately (e.g., send to GDA, check
        thresholds, log, etc.).
        
        @param data The SensorData message received.
        @return bool True on success; False otherwise.
        """
        pass
    
    def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
        """
        Callback function to handle a system performance message packaged as
        SystemPerformanceData object.
        
        This method is called when system performance data (CPU, memory, disk usage)
        is collected. The implementing class should process this data appropriately.
        
        @param data The SystemPerformanceData message received.
        @return bool True on success; False otherwise.
        """
        pass
    
    def setSystemPerformanceDataListener(self, listener: ISystemPerformanceDataListener = None):
        """
        Sets the system performance listener. The listener's callback function will be invoked
        when system performance data is available.
        
        @param listener The listener reference.
        """
        pass
    
    def setTelemetryDataListener(self, name: str = None, listener: ITelemetryDataListener = None):
        """
        Sets the named telemetry data listener. The listener's callback function will be invoked
        when telemetry data is available for the given name.
        
        @param name The name of the listener (e.g., sensor name, actuator name).
        @param listener The listener reference.
        """
        pass