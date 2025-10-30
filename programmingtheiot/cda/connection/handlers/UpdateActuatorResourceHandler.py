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

from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.ActuatorData import ActuatorData


class UpdateActuatorResourceHandler(Resource):
    """
    CoAP resource handler for actuator command updates.
    
    Handles PUT requests from the GDA to update actuator states on the CDA.
    Converts JSON payloads to ActuatorData and forwards to the data message listener.
    """
    
    def __init__(self, name: str = ConfigConst.ACTUATOR_CMD, coap_server = None, dataMsgListener: IDataMessageListener = None):
        """
        Initialize the Update Actuator resource handler.
        
        Args:
            name: Resource name
            coap_server: Reference to the CoAP server
            dataMsgListener: Data message listener for callbacks
        """
        super(UpdateActuatorResourceHandler, self).__init__(
            name, coap_server, visible=True, observable=False, allow_children=True)
        
        self.dataMsgListener = dataMsgListener
        self.dataUtil = DataUtil()
        
        # Get polling cycles from configuration
        self.pollCycles = ConfigUtil().getInteger(
            section=ConfigConst.CONSTRAINED_DEVICE,
            key=ConfigConst.POLL_CYCLES_KEY,
            defaultVal=ConfigConst.DEFAULT_POLLING_CYCLES
        )
        
        logging.info("Update Actuator resource handler initialized")
    
    
    def render_PUT_advanced(self, request, response):
        """
        Handle PUT requests for actuator command updates.
        
        Processes incoming JSON actuator commands, converts them to ActuatorData,
        and forwards to the data message listener for processing.
        
        Args:
            request: The CoAP PUT request containing actuator command
            response: The CoAP response to populate
            
        Returns:
            Tuple of (self, response)
        """
        if request:
            logging.info("PUT request received for Actuator resource")
            
            # Get the payload from the request
            requestPayload = request.payload
            
            if requestPayload:
                try:
                    logging.debug(f"Actuator command payload: {requestPayload}")
                    
                    # Convert JSON payload to ActuatorData
                    actuatorCmdData = self.dataUtil.jsonToActuatorData(requestPayload)
                    
                    if actuatorCmdData:
                        # Create response with processed data
                        response.payload = self._createResponse(response=response, data=actuatorCmdData)
                        response.max_age = self.pollCycles
                    else:
                        logging.warning("Failed to parse actuator command data")
                        response.code = defines.Codes.BAD_REQUEST.number
                        response.payload = "Invalid actuator data format"
                        
                except Exception as e:
                    logging.error(f"Error processing actuator command: {e}")
                    response.code = defines.Codes.INTERNAL_SERVER_ERROR.number
                    response.payload = "Error processing request"
            else:
                logging.warning("Empty payload in PUT request")
                response.code = defines.Codes.BAD_REQUEST.number
                response.payload = "Empty payload"
        else:
            logging.warning("Invalid PUT request received")
            response.code = defines.Codes.BAD_REQUEST.number
        
        return self, response
    
    
    def render_GET_advanced(self, request, response):
        """
        Handle GET requests (basic implementation).
        """
        logging.info("GET request received for Actuator resource")
        response.code = defines.Codes.CONTENT.number
        response.payload = "Actuator Command Resource"
        return self, response
    
    
    def render_POST_advanced(self, request, response):
        """
        Handle POST requests (create/update resource).
        """
        logging.info("POST request received for Actuator resource")
        
        if request:
            response.code = defines.Codes.CREATED.number
            logging.debug(f"POST payload: {request.payload}")
        
        return self, response
    
    
    def render_DELETE_advanced(self, request, response):
        """
        Handle DELETE requests (remove resource).
        """
        logging.info("DELETE request received for Actuator resource")
        
        if request:
            response.code = defines.Codes.DELETED.number
        
        return True, response
    
    
    def _createResponse(self, response = None, data: ActuatorData = None) -> tuple:
        """
        Create a response for the actuator command.
        
        Forwards the actuator command to the data message listener and
        creates an appropriate response based on the result.
        
        Args:
            response: The CoAP response object to update
            data: The ActuatorData from the command
            
        Returns:
            Tuple of (content_type, json_data)
        """
        try:
            # Forward actuator command to the data message listener
            actuatorResponseData = None
            
            if self.dataMsgListener:
                actuatorResponseData = self.dataMsgListener.handleActuatorCommandRequest(data)
            
            # If no response or processing failed, create error response
            if not actuatorResponseData:
                logging.warning("No response from actuator command processing")
                
                actuatorResponseData = ActuatorData()
                actuatorResponseData.updateData(data)
                actuatorResponseData.setAsResponse()
                actuatorResponseData.setStatusCode(-1)
                
                response.code = defines.Codes.PRECONDITION_FAILED.number
            else:
                logging.info("Actuator command processed successfully")
                response.code = defines.Codes.CHANGED.number
            
            # Convert response to JSON
            jsonData = self.dataUtil.actuatorDataToJson(actuatorResponseData)
            
            logging.debug(f"Actuator response JSON: {jsonData}")
            
            return (defines.Content_types["application/json"], jsonData)
            
        except Exception as e:
            logging.error(f"Error creating actuator response: {e}")
            response.code = defines.Codes.INTERNAL_SERVER_ERROR.number
            
            # Return error response
            errorData = ActuatorData()
            errorData.setStatusCode(-1)
            jsonData = self.dataUtil.actuatorDataToJson(errorData)
            
            return (defines.Content_types["application/json"], jsonData)