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
from programmingtheiot.common.ISystemPerformanceDataListener import ISystemPerformanceDataListener

from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData


class GetSystemPerformanceResourceHandler(Resource, ISystemPerformanceDataListener):
    """
    Observable CoAP resource handler for System Performance Data.
    
    Supports GET requests and OBSERVE functionality to notify clients
    of system performance updates.
    """
    
    def __init__(self, name: str = ConfigConst.SYSTEM_PERF_MSG, coap_server = None, dataMsgListener: IDataMessageListener = None):
        """
        Initialize the System Performance resource handler.
        
        Args:
            name: Resource name
            coap_server: Reference to the CoAP server
            dataMsgListener: Data message listener for callbacks
        """
        super(GetSystemPerformanceResourceHandler, self).__init__(
            name, coap_server, visible=True, observable=True, allow_children=True)
        
        # Get polling cycles from configuration
        self.pollCycles = ConfigUtil().getInteger(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.POLL_CYCLES_KEY,
            defaultVal=ConfigConst.DEFAULT_POLLING_CYCLES
        )
        
        self.dataUtil = DataUtil()
        self.sysPerfData = SystemPerformanceData()
        
        self.dataMsgListener = dataMsgListener
        
        # Reserved for lab module 10
        if self.dataMsgListener:
            self.dataMsgListener.setSystemPerformanceDataListener(self)
        
        # For testing
        self.payload = "GetSysPerfData"
        
        logging.info("System Performance resource handler initialized")
    
    
    def render_GET_advanced(self, request, response):
        """
        Handle GET requests for system performance data.
        
        Args:
            request: The CoAP request
            response: The CoAP response to populate
            
        Returns:
            Tuple of (self, response)
        """
        if request:
            response.code = defines.Codes.CONTENT.number
            
            if not self.sysPerfData:
                response.code = defines.Codes.EMPTY.number
                self.sysPerfData = SystemPerformanceData()
            
            # Convert system performance data to JSON
            jsonData = self.dataUtil.systemPerformanceDataToJson(self.sysPerfData)
            
            logging.info("Latest SystemPerformanceData JSON: " + jsonData)
            
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
        logging.info("PUT request received for System Performance resource")
        
        if request:
            response.code = defines.Codes.CHANGED.number
            logging.debug(f"PUT payload: {request.payload}")
        
        return self, response
    
    
    def render_POST_advanced(self, request, response):
        """
        Handle POST requests (create/update resource).
        """
        logging.info("POST request received for System Performance resource")
        
        if request:
            response.code = defines.Codes.CREATED.number
            logging.debug(f"POST payload: {request.payload}")
        
        return self, response
    
    
    def render_DELETE_advanced(self, request, response):
        """
        Handle DELETE requests (remove resource).
        """
        logging.info("DELETE request received for System Performance resource")
        
        if request:
            response.code = defines.Codes.DELETED.number
        
        return True, response
    
    
    def onSystemPerformanceDataUpdate(self, data: SystemPerformanceData) -> bool:
        """
        Callback for system performance data updates.
        
        Args:
            data: Updated SystemPerformanceData instance
            
        Returns:
            bool: True if update was successful
        """
        if data:
            self.sysPerfData = data
            self.changed = True
            logging.debug("System performance data updated")
            return True
        
        return False