##
# This class is part of the Programming the Internet of Things project.
#
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
##

import logging

from coapthon import defines
from coapthon.resources.resource import Resource

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ITelemetryDataListener import ITelemetryDataListener

from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.SensorData import SensorData


class GetTelemetryResourceHandler(Resource, ITelemetryDataListener):
    """
    Observable CoAP resource handler for Sensor/Telemetry Data.
    
    Supports GET requests and OBSERVE functionality to notify clients
    of sensor data updates.
    """
    
    def __init__(self, name: str = ConfigConst.SENSOR_MSG, coap_server = None, dataMsgListener: IDataMessageListener = None):
        """
        Initialize the Telemetry resource handler.
        
        Args:
            name: Resource name
            coap_server: Reference to the CoAP server
            dataMsgListener: Data message listener for callbacks
        """
        super(GetTelemetryResourceHandler, self).__init__(
            name, coap_server, visible=True, observable=True, allow_children=True)
        
        # Get polling cycles from configuration
        self.pollCycles = ConfigUtil().getInteger(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.POLL_CYCLES_KEY,
            defaultVal=ConfigConst.DEFAULT_POLLING_CYCLES
        )
        
        self.dataUtil = DataUtil()
        self.sensorData = SensorData()
        
        self.dataMsgListener = dataMsgListener
        
        # Reserved for lab module 10
        if self.dataMsgListener:
            self.dataMsgListener.setTelemetryDataListener(self)
        
        # For testing
        self.payload = "GetSensorData"
        
        logging.info("Telemetry resource handler initialized")
    
    
    def render_GET_advanced(self, request, response):
        """
        Handle GET requests for sensor/telemetry data.
        """
        if request:
            response.code = defines.Codes.CONTENT.number
            
            if not self.sensorData:
                response.code = defines.Codes.EMPTY.number
                self.sensorData = SensorData()
            
            # Convert sensor data to JSON
            jsonData = self.dataUtil.sensorDataToJson(self.sensorData)
            
            logging.info("Latest SensorData JSON: " + jsonData)
            
            # Set response payload with JSON content type
            response.payload = (defines.Content_types["application/json"], jsonData)
            response.max_age = self.pollCycles
            
            # 'changed' will be discussed in a later exercise
            self.changed = False
        
        return self, response
    
    
    def render_PUT_advanced(self, request, response):
        """
        Handle PUT requests (update resource).
        """
        logging.info("PUT request received for Telemetry resource")
        
        if request:
            response.code = defines.Codes.CHANGED.number
            logging.debug(f"PUT payload: {request.payload}")
        
        return self, response
    
    
    def render_POST_advanced(self, request, response):
        """
        Handle POST requests (create/update resource).
        """
        logging.info("POST request received for Telemetry resource")
        
        if request:
            response.code = defines.Codes.CREATED.number
            logging.debug(f"POST payload: {request.payload}")
        
        return self, response
    
    
    def render_DELETE_advanced(self, request, response):
        """
        Handle DELETE requests (remove resource).
        """
        logging.info("DELETE request received for Telemetry resource")
        
        if request:
            response.code = defines.Codes.DELETED.number
        
        return True, response
    
    
    def onSensorDataUpdate(self, data: SensorData) -> bool:
        """
        Callback for sensor data updates.
        """
        if data:
            self.sensorData = data
            self.changed = True
            logging.debug("Sensor data updated")
            return True
        
        return False