##
# This class is part of the Programming the Internet of Things project.
##

import logging

import aiocoap
from aiocoap.resource import Resource

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.ActuatorData import ActuatorData


class AsyncUpdateActuatorResourceHandler(Resource):
    """
    Async resource handler for actuator command updates using aiocoap.
    
    Handles PUT requests to update actuator states from the GDA.
    """
    
    def __init__(self, dataMsgListener: IDataMessageListener = None):
        """
        Initialize the async actuator resource handler.
        
        Args:
            dataMsgListener: Listener for actuator command callbacks
        """
        super().__init__()
        self.dataMsgListener = dataMsgListener
        self.dataUtil = DataUtil()
        logging.info("Async Update Actuator resource handler initialized")
    
    
    async def render_put(self, request):
        """
        Handle PUT requests for actuator commands (async).
        
        Args:
            request: The aiocoap request
            
        Returns:
            aiocoap.Message with response
        """
        try:
            responseCode = aiocoap.Code.NOT_ACCEPTABLE
            
            # Validate request has payload
            if not request.payload:
                logging.warning("Empty payload in PUT request")
                return aiocoap.Message(code=aiocoap.Code.BAD_REQUEST)
            
            # Convert JSON payload to ActuatorData
            actuatorCmdData = self.dataUtil.jsonToActuatorData(request.payload.decode('utf-8'))
            
            if not actuatorCmdData:
                logging.warning("Failed to parse actuator command data")
                return aiocoap.Message(code=aiocoap.Code.BAD_REQUEST)
            
            logging.info(f'Handling PUT request for actuator: {actuatorCmdData.getName()}')
            
            # Create and return response
            return self._createResponse(actuatorCmdData)
            
        except Exception as e:
            logging.error(f"Failed to handle actuator command: {e}")
            return aiocoap.Message(code=aiocoap.Code.INTERNAL_SERVER_ERROR)
    
    
    async def render_get(self, request):
        """
        Handle GET requests (basic implementation).
        """
        logging.info("GET request received for Async Actuator resource")
        payload = "Async Actuator Command Resource".encode('utf-8')
        return aiocoap.Message(code=aiocoap.Code.CONTENT, payload=payload)
    
    
    def _createResponse(self, data: ActuatorData = None):
        """
        Create response for actuator command.
        
        Args:
            data: The ActuatorData command
            
        Returns:
            aiocoap.Message with response
        """
        responseCode = aiocoap.Code.CHANGED
        
        try:
            # Forward command to listener
            actuatorResponseData = None
            
            if self.dataMsgListener:
                actuatorResponseData = self.dataMsgListener.handleActuatorCommandRequest(data)
            
            # If no response, create error response
            if not actuatorResponseData:
                logging.warning("No response from actuator command processing")
                actuatorResponseData = ActuatorData()
                actuatorResponseData.updateData(data)
                actuatorResponseData.setAsResponse()
                actuatorResponseData.setStatusCode(-1)
                responseCode = aiocoap.Code.PRECONDITION_FAILED
            
            # Convert to JSON
            jsonData = self.dataUtil.actuatorDataToJson(actuatorResponseData)
            
            return aiocoap.Message(code=responseCode, payload=jsonData.encode('utf-8'))
            
        except Exception as e:
            logging.error(f"Error creating actuator response: {e}")
            return aiocoap.Message(code=aiocoap.Code.INTERNAL_SERVER_ERROR)
