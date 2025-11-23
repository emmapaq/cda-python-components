import logging
from coapthon import defines
from coapthon.client.helperclient import HelperClient
from coapthon.utils import generate_random_token
import traceback

from programmingtheiot.cda.connection.IRequestResponseClient import IRequestResponseClient
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common import ConfigConst
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.data.DataUtil import DataUtil

class CoapClientConnector(IRequestResponseClient):
    """
    CoAP client connector for handling CoAP requests (GET, POST, PUT, DELETE, DISCOVERY).
    Uses CoAPthon3 library.
    """
    
    def __init__(self, dataMsgListener: IDataMessageListener = None):
        """
        Initialize the CoAP client connector.
        
        Args:
            dataMsgListener: Optional data message listener for callbacks
        """
        self.config = ConfigUtil()
        self.dataMsgListener = dataMsgListener
        
        # Load CoAP configuration
        self.host = self.config.getProperty(
            ConfigConst.COAP_GATEWAY_SERVICE, 
            ConfigConst.HOST_KEY, 
            ConfigConst.DEFAULT_HOST)
        
        self.port = self.config.getInteger(
            ConfigConst.COAP_GATEWAY_SERVICE, 
            ConfigConst.PORT_KEY, 
            ConfigConst.DEFAULT_COAP_PORT)
        
        # Initialize the CoAP client - will be created when needed
        self.coapClient = None
        
        # Dictionary to track active OBSERVE requests
        self.observeRequests = {}
        
        logging.info(f"CoAP client configured for host={self.host}, port={self.port}")
    
    def sendDiscoveryRequest(self, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Send a CoAP DISCOVERY request to retrieve available resources.
        Uses the .well-known/core resource path.
        
        Args:
            timeout: Request timeout in seconds
            
        Returns:
            bool: True if discovery request sent successfully
        """
        logging.info("Discovering remote resources...")
        
        # Create client for this request
        if not self.coapClient:
            self.coapClient = HelperClient(server=(self.host, self.port))
        
        resourcePath = self._createResourcePath(None, '.well-known/core')
        
        logging.info(f"Issuing DISCOVERY with path: {resourcePath}")
        
        request = self.coapClient.mk_request(defines.Codes.GET, path=resourcePath)
        request.token = generate_random_token(2)
        
        self.coapClient.send_request(request=request, timeout=timeout, callback=self._onDiscoveryResponse)
        
        return True
    
    def _onDiscoveryResponse(self, response):
        """
        Callback method for handling DISCOVERY responses.
        
        Args:
            response: CoAPthon3 response object
        """
        if not response:
            logging.warning("DISCOVERY response invalid. Ignoring.")
            return
        
        logging.info(f"DISCOVERY response received: {response.payload}")
    
    def sendGetRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Send a CoAP GET request for the specified resource.
        
        Args:
            resource: The resource to request (from ResourceNameEnum)
            name: Optional name to extend the resource path
            enableCON: If True, use confirmable message; otherwise use non-confirmable
            timeout: Request timeout in seconds
            
        Returns:
            bool: True if GET request sent successfully
        """
        if resource or name:
            # Create client for this request
            if not self.coapClient:
                self.coapClient = HelperClient(server=(self.host, self.port))
            
            resourcePath = self._createResourcePath(resource, name)
            
            logging.info(f"Issuing GET with path: {resourcePath}")
            
            request = self.coapClient.mk_request(defines.Codes.GET, path=resourcePath)
            request.token = generate_random_token(2)
            
            if not enableCON:
                request.type = defines.Types["NON"]
            
            response = self.coapClient.send_request(request=request, timeout=timeout)
            
            self._onGetResponse(response=response, resourcePath=resourcePath)
            
            return True
        else:
            logging.warning("Can't test GET - no path or path list provided.")
            return False
    
    def _onGetResponse(self, response, resourcePath: str = None):
        """
        Callback method for handling GET responses.
        Processes the response payload and routes to appropriate handler.
        
        Args:
            response: CoAPthon3 response object
            resourcePath: The resource path used in the request
        """
        if not response:
            logging.warning("GET response invalid. Ignoring.")
            return
        
        logging.info("GET response received.")
        
        jsonData = response.payload
        locationPath = resourcePath.split('/')
        
        if len(locationPath) > 2:
            dataType = locationPath[2]
            
            if dataType == ConfigConst.ACTUATOR_CMD:
                # Convert payload to ActuatorData
                logging.info(f"ActuatorData received: {jsonData}")
                
                try:
                    ad = DataUtil().jsonToActuatorData(jsonData)
                    
                    if self.dataMsgListener:
                        self.dataMsgListener.handleActuatorCommandMessage(ad)
                except:
                    logging.warning(f"Failed to decode actuator data. Ignoring: {jsonData}")
                    return
            else:
                logging.info(f"Response data received. Payload: {jsonData}")
        else:
            logging.info(f"Response data received. Payload: {jsonData}")
    
    def sendPostRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Send a CoAP POST request.
        """
        if resource or name:
            # Create client for this request
            if not self.coapClient:
                self.coapClient = HelperClient(server=(self.host, self.port))
            
            resourcePath = self._createResourcePath(resource, name)
            
            # PERFORMANCE TESTING: Comment out during performance tests
            # logging.info(f"Issuing POST with path: {resourcePath}")
            
            request = self.coapClient.mk_request(defines.Codes.POST, path=resourcePath)
            request.token = generate_random_token(2)
            request.payload = payload
            
            if not enableCON:
                request.type = defines.Types["NON"]
            
            # PERFORMANCE TESTING: Comment out during performance tests
            # logging.info(f"Sending POST with payload: {payload}")
            
            self.coapClient.send_request(request=request, callback=self._onPostResponse, timeout=timeout)
            
            return True
        else:
            logging.warning("Can't test POST - no path or path list provided.")
            return False

    def _onPostResponse(self, response):
        """
        Callback method for handling POST responses.
        """
        if not response:
            logging.warning("POST response invalid. Ignoring.")
            return
        
        # PERFORMANCE TESTING: Comment out during performance tests
        # logging.info(f"POST response received: {response.payload}")
        pass

    def sendPutRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Send a CoAP PUT request.
        """
        if resource or name:
            # Create client for this request
            if not self.coapClient:
                self.coapClient = HelperClient(server=(self.host, self.port))
            
            resourcePath = self._createResourcePath(resource, name)
            
            # PERFORMANCE TESTING: Comment out during performance tests
            # logging.info(f"Issuing PUT with path: {resourcePath}")
            
            request = self.coapClient.mk_request(defines.Codes.PUT, path=resourcePath)
            request.token = generate_random_token(2)
            request.payload = payload
            
            if not enableCON:
                request.type = defines.Types["NON"]
            
            self.coapClient.send_request(request=request, callback=self._onPutResponse, timeout=timeout)
            
            return True
        else:
            logging.warning("Can't test PUT - no path or path list provided.")
            return False

    def _onPutResponse(self, response):
        """
        Callback method for handling PUT responses.
        """
        if not response:
            logging.warning("PUT response invalid. Ignoring.")
            return
        
        # PERFORMANCE TESTING: Comment out during performance tests
        # logging.info(f"PUT response received: {response.payload}")
        pass
    
    def sendDeleteRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Send a CoAP DELETE request.
        
        Args:
            resource: The resource to DELETE
            name: Optional name to extend the resource path
            enableCON: If True, use confirmable message
            timeout: Request timeout in seconds
            
        Returns:
            bool: True if DELETE request sent successfully
        """
        if resource or name:
            # Create client for this request
            if not self.coapClient:
                self.coapClient = HelperClient(server=(self.host, self.port))
            
            resourcePath = self._createResourcePath(resource, name)
            
            logging.info(f"Issuing DELETE with path: {resourcePath}")
            
            request = self.coapClient.mk_request(defines.Codes.DELETE, path=resourcePath)
            request.token = generate_random_token(2)
            
            if not enableCON:
                request.type = defines.Types["NON"]
            
            response = self.coapClient.send_request(request=request, timeout=timeout)
            
            self._onDeleteResponse(response=response, resourcePath=resourcePath)
            
            return True
        else:
            logging.warning("Can't send DELETE - no path provided.")
            return False
    
    def _onDeleteResponse(self, response, resourcePath: str = None):
        """
        Callback method for handling DELETE responses.
        
        Args:
            response: CoAPthon3 response object
            resourcePath: The resource path used in the request
        """
        if not response:
            logging.warning("DELETE response invalid. Ignoring.")
            return
        
        logging.info(f"DELETE response received for path: {resourcePath}")
    
    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        """
        Set the data message listener for handling responses.
        
        Args:
            listener: The listener to set
            
        Returns:
            bool: True if successful
        """
        if listener:
            self.dataMsgListener = listener
            logging.info("Data message listener set for CoapClientConnector")
            return True
        return False
    
    def _createResourcePath(self, resource: ResourceNameEnum = None, name: str = None) -> str:
        """
        Create the resource path for CoAP requests.
        
        Args:
            resource: ResourceNameEnum to convert to path
            name: Optional name to append/use
            
        Returns:
            str: The formatted resource path
        """
        resourcePath = ""
        
        if resource:
            resourcePath = resource.value
        
        if name:
            if resourcePath:
                resourcePath = resourcePath + "/" + name
            else:
                resourcePath = name
        
        # Ensure path doesn't start with '/' for CoAPthon3
        if resourcePath.startswith('/'):
            resourcePath = resourcePath[1:]
        
        return resourcePath
    
    def startObserver(self, resource: ResourceNameEnum = None, name: str = None, ttl: int = IRequestResponseClient.DEFAULT_TTL) -> bool:
        """
        Start observing a resource (OBSERVE functionality).
        
        Args:
            resource: The resource to observe
            name: Optional name to extend the resource path
            ttl: Time to live for observation in seconds (not currently used)
            
        Returns:
            bool: True if observation started successfully
        """
        if resource or name:
            if resource in self.observeRequests:
                logging.warning(f"Already observing resource {resource}. Ignoring start observe request.")
                return False
            
            self.observeRequests[resource] = None
            
            # Create client for this request if needed
            if not self.coapClient:
                self.coapClient = HelperClient(server=(self.host, self.port))
            
            resourcePath = self._createResourcePath(resource, name)
            
            observeActuatorCmdHandler = HandleActuatorEvent(
                listener=self.dataMsgListener,
                resource=resource,
                requests=self.observeRequests
            )
            
            try:
                logging.info(f"Starting OBSERVE for resource: {resourcePath}")
                self.coapClient.observe(path=resourcePath, callback=observeActuatorCmdHandler.handleActuatorResponse)
                logging.info(f"OBSERVE started for resource: {resourcePath}")
                return True
            except Exception as e:
                logging.warning(f"Failed to observe path: {resourcePath}")
                traceback.print_exception(type(e), e, e.__traceback__)
                # Remove from tracking if observe failed
                if resource in self.observeRequests:
                    del self.observeRequests[resource]
                return False
        else:
            logging.warning("Can't start OBSERVE - no resource provided.")
            return False
    
    def stopObserver(self, resource: ResourceNameEnum = None, name: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Stop observing a resource.
        
        Args:
            resource: The resource to stop observing
            name: Optional name (not used but included for consistency)
            timeout: Request timeout in seconds
            
        Returns:
            bool: True if observation stopped successfully
        """
        if resource or name:
            if not resource in self.observeRequests:
                logging.warning(f"Resource {resource} not being observed. Ignoring stop observe request.")
                return False
            
            response = self.observeRequests[resource]
            
            if response:
                logging.info(f"Cancelling observe for resource {resource}.")
                
                try:
                    self.coapClient.cancel_observing(response=response, send_rst=True)
                    
                    del self.observeRequests[resource]
                    
                    logging.info(f"Cancelled observe for resource {resource}.")
                    return True
                except Exception as e:
                    logging.warning(f"Failed to cancel observe for resource {resource}")
                    traceback.print_exception(type(e), e, e.__traceback__)
                    return False
            else:
                logging.warning(f"No response yet for observed resource {resource}. Ignoring stop request.")
                
                # Just remove from tracking since we can't cancel without a response
                del self.observeRequests[resource]
                
                logging.info(f"Removed resource {resource} from observe tracking (no response to cancel).")
                return True
        else:
            logging.warning("Can't stop OBSERVE - no resource provided.")
            return False
    
    def stop(self):
        """
        Stop the CoAP client and clean up resources.
        This should be called when done using the client to properly
        shut down threads and release resources.
        """
        if self.coapClient:
            try:
                logging.info("Stopping CoAP client...")
                self.coapClient.stop()
                self.coapClient = None
                logging.info("CoAP client stopped successfully")
            except Exception as e:
                logging.error(f"Error stopping CoAP client: {e}")


class HandleActuatorEvent():
    """
    Internal handler class for processing OBSERVE responses containing ActuatorData.
    Used as a callback handler for CoAP OBSERVE functionality.
    """
    
    def __init__(self, 
                 listener: IDataMessageListener = None,
                 resource: ResourceNameEnum = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE,
                 requests = None):
        """
        Initialize the actuator event handler.
        
        Args:
            listener: The data message listener to forward actuator commands to
            resource: The resource being observed
            requests: Dictionary tracking active observe requests
        """
        self.listener = listener
        self.resource = resource
        self.observeRequests = requests
        
        if not self.resource:
            self.resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE
    
    def handleActuatorResponse(self, response):
        """
        Handle incoming actuator response from OBSERVE.
        
        Args:
            response: CoAPthon3 response object containing ActuatorData
        """
        if response:
            jsonData = response.payload
            
            if self.observeRequests is not None:
                self.observeRequests[self.resource] = response
            
            logging.info(f"Received actuator command response to resource {self.resource} -> {jsonData}")
            
            if self.listener:
                try:
                    data = DataUtil().jsonToActuatorData(jsonData=jsonData)
                    self.listener.handleActuatorCommandMessage(data=data)
                except:
                    logging.warning(f"Failed to decode actuator data. Ignoring: {jsonData}")