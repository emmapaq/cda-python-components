import logging
import asyncio
import traceback
import threading
from typing import Optional

import aiocoap
from aiocoap import Context, Message, Code
from aiocoap.numbers.types import Type as MessageType

# Import message types
CON = MessageType.CON
NON = MessageType.NON

from programmingtheiot.cda.connection.IRequestResponseClient import IRequestResponseClient
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.ConfigUtil import ConfigUtil
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.data.DataUtil import DataUtil

class AsyncCoapClientConnector(IRequestResponseClient):
    """
    Async CoAP client connector using aiocoap library with asyncio.
    Handles CoAP requests (GET, POST, PUT, DELETE, DISCOVERY) asynchronously.
    """
    
    def __init__(self, dataMsgListener: IDataMessageListener = None):
        """
        Initialize the async CoAP client connector.
        
        Args:
            dataMsgListener: Optional data message listener for callbacks
        """
        self.config = ConfigUtil()
        self.dataMsgListener = dataMsgListener
        self.dataUtil = DataUtil()
        
        # Load CoAP configuration
        self.host = self.config.getProperty(
            ConfigConst.COAP_GATEWAY_SERVICE, 
            ConfigConst.HOST_KEY, 
            ConfigConst.DEFAULT_HOST)
        
        self.port = self.config.getInteger(
            ConfigConst.COAP_GATEWAY_SERVICE, 
            ConfigConst.PORT_KEY, 
            ConfigConst.DEFAULT_COAP_PORT)
        
        # Build URI path
        self.uriPath = f"coap://{self.host}:{self.port}/"
        
        # Initialize event loop and context
        self._eventLoop: Optional[asyncio.AbstractEventLoop] = None
        self._executionThread: Optional[threading.Thread] = None
        self.clientContext: Optional[Context] = None
        
        # Dictionary to track active OBSERVE requests and tasks
        self.observeRequests = {}
        self.observeTasks = {}
        
        # Start the async event loop in a separate thread
        self._startEventLoop()
        
        logging.info(f"Async CoAP client configured for {self.uriPath}")
    
    def _startEventLoop(self):
        """
        Start the asyncio event loop in a separate daemon thread.
        """
        def runEventLoop(loop):
            """Run the event loop in the thread."""
            asyncio.set_event_loop(loop)
            loop.run_forever()
        
        # Create new event loop for this client
        self._eventLoop = asyncio.new_event_loop()
        
        # Create and start the thread
        self._executionThread = threading.Thread(
            target=runEventLoop, 
            args=(self._eventLoop,), 
            daemon=True,
            name="Async-CoAP-Client-Thread"
        )
        self._executionThread.start()
        
        # Create the aiocoap context in the event loop
        future = asyncio.run_coroutine_threadsafe(
            Context.create_client_context(), 
            self._eventLoop
        )
        
        try:
            self.clientContext = future.result(timeout=5)
            logging.info("Async CoAP client context created successfully")
        except Exception as e:
            logging.error(f"Failed to create async CoAP client context: {e}")
            traceback.print_exception(type(e), e, e.__traceback__)
    
    def sendDiscoveryRequest(self, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Send an async CoAP DISCOVERY request to retrieve available resources.
        
        Args:
            timeout: Request timeout in seconds
            
        Returns:
            bool: True if discovery request sent successfully
        """
        logging.info("Discovering remote resources...")
        
        resourcePath = ".well-known/core"
        
        logging.info(f"Issuing Async DISCOVERY to path: {resourcePath}")
        
        try:
            future = asyncio.run_coroutine_threadsafe(
                self._handleGetRequest(resourcePath, enableCON=False),
                self._eventLoop
            )
            
            return future.result(timeout=timeout)
        except Exception as e:
            logging.error(f"Discovery request failed: {e}")
            return False
    
    def sendGetRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Send an async CoAP GET request.
        
        Args:
            resource: The resource to request
            name: Optional name to extend the resource path
            enableCON: If True, use confirmable message
            timeout: Request timeout in seconds
            
        Returns:
            bool: True if GET request sent successfully
        """
        if resource or name:
            resourcePath = self._createResourcePath(resource, name)
            
            logging.info(f"Issuing Async GET to path: {resourcePath}")
            
            try:
                future = asyncio.run_coroutine_threadsafe(
                    self._handleGetRequest(resourcePath, enableCON),
                    self._eventLoop
                )
                
                return future.result(timeout=timeout)
            except Exception as e:
                logging.error(f"GET request failed: {e}")
                return False
        else:
            logging.warning("Can't issue Async GET - no path provided.")
            return False
    
    async def _handleGetRequest(self, resourcePath: str = None, enableCON: bool = False):
        """
        Handle async GET request.
        
        Args:
            resourcePath: The resource path to GET
            enableCON: If True, use confirmable message
            
        Returns:
            bool: True if successful
        """
        try:
            uriAndResourcePath = self.uriPath + resourcePath
            
            msgType = NON
            
            if enableCON:
                msgType = CON
            
            msg = Message(mtype=msgType, code=Code.GET, uri=uriAndResourcePath)
            
            responseData = await self.clientContext.request(request_message=msg).response
            
            self._onGetResponse(responseData, resourcePath)
            
            return True
            
        except Exception as e:
            logging.warning(f"Failed to process Async GET request for path: {uriAndResourcePath}")
            traceback.print_exception(type(e), e, e.__traceback__)
            return False
    
    def _onGetResponse(self, response, resourcePath: str = None):
        """
        Handle GET response.
        
        Args:
            response: The aiocoap response object
            resourcePath: The resource path used in the request
        """
        if not response:
            logging.warning("Async GET response invalid. Ignoring.")
            return
        
        logging.info("Async GET response received.")
        
        responseData = response.payload.decode("utf-8")
        
        locationPath = resourcePath.split('/')
        
        if len(locationPath) > 2:
            dataType = locationPath[2]
            
            if dataType == ConfigConst.ACTUATOR_CMD:
                logging.info(f"ActuatorData received: {responseData}")
                
                try:
                    ad = self.dataUtil.jsonToActuatorData(responseData)
                    
                    if self.dataMsgListener:
                        self.dataMsgListener.handleActuatorCommandMessage(ad)
                except:
                    logging.warning(f"Failed to decode actuator data. Ignoring: {responseData}")
                    return
            else:
                logging.info(f"Response data received. Payload: {responseData}")
        else:
            logging.info(f"Response data received. Payload: {responseData}")
    
    def sendPostRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Send an async CoAP POST request.
        
        Args:
            resource: The resource to POST to
            name: Optional name to extend the resource path
            enableCON: If True, use confirmable message
            payload: The data payload to send
            timeout: Request timeout in seconds
            
        Returns:
            bool: True if POST request sent successfully
        """
        if resource or name:
            resourcePath = self._createResourcePath(resource, name)
            
            logging.info(f"Issuing Async POST to path: {resourcePath}")
            
            try:
                future = asyncio.run_coroutine_threadsafe(
                    self._handlePostRequest(resourcePath, payload, enableCON),
                    self._eventLoop
                )
                
                return future.result(timeout=timeout)
            except Exception as e:
                logging.error(f"POST request failed: {e}")
                return False
        else:
            logging.warning("Can't issue Async POST - no path provided.")
            return False
    
    async def _handlePostRequest(self, resourcePath: str = None, payload: str = None, enableCON: bool = False):
        """
        Handle async POST request.
        
        Args:
            resourcePath: The resource path to POST to
            payload: The data payload to send
            enableCON: If True, use confirmable message
            
        Returns:
            bool: True if successful
        """
        try:
            uriAndResourcePath = self.uriPath + resourcePath
            
            msgType = NON
            
            if enableCON:
                msgType = CON
            
            msg = Message(mtype=msgType, payload=payload.encode("utf-8"), code=Code.POST, uri=uriAndResourcePath)
            
            responseData = await self.clientContext.request(request_message=msg).response
            
            self._onPostResponse(responseData)
            
            return True
            
        except Exception as e:
            # NOTE: for debugging, you may want to optionally include the stack trace, as shown
            logging.warning(f"Failed to process Async POST request for path: {uriAndResourcePath}")
            traceback.print_exception(type(e), e, e.__traceback__)
            return False
    
    def _onPostResponse(self, response):
        """
        Handle POST response.
        
        Args:
            response: The aiocoap response object
        """
        if not response:
            logging.warning("Async POST response invalid. Ignoring.")
            return
        
        logging.info("Async POST response received.")
        
        responseData = response.payload.decode("utf-8")
        
        logging.info(f"Response data received. Payload: {responseData}")
    
    def sendPutRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, payload: str = None, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Send an async CoAP PUT request.
        
        Args:
            resource: The resource to PUT to
            name: Optional name to extend the resource path
            enableCON: If True, use confirmable message
            payload: The data payload to send
            timeout: Request timeout in seconds
            
        Returns:
            bool: True if PUT request sent successfully
        """
        if resource or name:
            resourcePath = self._createResourcePath(resource, name)
            
            logging.info(f"Issuing Async PUT to path: {resourcePath}")
            
            future = asyncio.run_coroutine_threadsafe(
                self._handlePutRequest(resourcePath, payload, enableCON),
                self._eventLoopThread
            )
            
            return future.result()
        else:
            logging.warning("Can't issue Async PUT - no path provided.")
            return False
    
    async def _handlePutRequest(self, resourcePath: str = None, payload: str = None, enableCON: bool = False):
        """
        Handle async PUT request.
        
        Args:
            resourcePath: The resource path to PUT to
            payload: The data payload to send
            enableCON: If True, use confirmable message
            
        Returns:
            bool: True if successful
        """
        try:
            uriAndResourcePath = self.uriPath + resourcePath
            
            msgType = NON
            
            if enableCON:
                msgType = CON
            
            msg = Message(mtype=msgType, payload=payload.encode("utf-8"), code=Code.PUT, uri=uriAndResourcePath)
            
            responseData = await self.clientContext.request(request_message=msg).response
            
            self._onPutResponse(responseData)
            
            return True
            
        except Exception as e:
            logging.warning(f"Failed to process Async PUT request for path: {uriAndResourcePath}")
            traceback.print_exception(type(e), e, e.__traceback__)
            return False
    
    def _onPutResponse(self, response):
        """
        Handle PUT response.
        
        Args:
            response: The aiocoap response object
        """
        if not response:
            logging.warning("Async PUT response invalid. Ignoring.")
            return
        
        logging.info("Async PUT response received.")
        
        responseData = response.payload.decode("utf-8")
        
        logging.info(f"Response data received. Payload: {responseData}")
    
    def sendDeleteRequest(self, resource: ResourceNameEnum = None, name: str = None, enableCON: bool = False, timeout: int = IRequestResponseClient.DEFAULT_TIMEOUT) -> bool:
        """
        Send an async CoAP DELETE request.
        
        Args:
            resource: The resource to DELETE
            name: Optional name to extend the resource path
            enableCON: If True, use confirmable message
            timeout: Request timeout in seconds
            
        Returns:
            bool: True if DELETE request sent successfully
        """
        if resource or name:
            resourcePath = self._createResourcePath(resource, name)
            
            logging.info(f"Issuing Async DELETE to path: {resourcePath}")
            
            future = asyncio.run_coroutine_threadsafe(
                self._handleDeleteRequest(resourcePath, enableCON),
                self._eventLoopThread
            )
            
            return future.result()
        else:
            logging.warning("Can't issue Async DELETE - no path provided.")
            return False
    
    async def _handleDeleteRequest(self, resourcePath: str = None, enableCON: bool = False):
        """
        Handle async DELETE request.
        
        Args:
            resourcePath: The resource path to DELETE
            enableCON: If True, use confirmable message
            
        Returns:
            bool: True if successful
        """
        try:
            uriAndResourcePath = self.uriPath + resourcePath
            
            msgType = NON
            
            if enableCON:
                msgType = CON
            
            msg = Message(mtype=msgType, code=Code.DELETE, uri=uriAndResourcePath)
            
            responseData = await self.clientContext.request(request_message=msg).response
            
            self._onDeleteResponse(responseData)
            
            return True
            
        except Exception as e:
            logging.warning(f"Failed to process Async DELETE request for path: {uriAndResourcePath}")
            traceback.print_exception(type(e), e, e.__traceback__)
            return False
    
    def _onDeleteResponse(self, response):
        """
        Handle DELETE response.
        
        Args:
            response: The aiocoap response object
        """
        if not response:
            logging.warning("Async DELETE response invalid. Ignoring.")
            return
        
        logging.info("Async DELETE response received.")
        
        responseData = response.payload.decode("utf-8")
        
        logging.info(f"Response data received. Payload: {responseData}")
    
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
            logging.info("Data message listener set for AsyncCoapClientConnector")
            return True
        return False
    
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
            resourcePath = self._createResourcePath(resource, name)
            
            if resourcePath in self.observeTasks:
                logging.warning(f"Already observing resource {resourcePath}. Ignoring start observe request.")
                return False
            
            fullPath = self.uriPath + resourcePath
            
            task = asyncio.run_coroutine_threadsafe(
                self._handleStartObserveRequest(fullPath),
                self._eventLoop
            )
            
            self.observeTasks[resourcePath] = task  # Store in Tasks
            
            logging.info(f"Started observing: {resourcePath}")
            return True
        else:
            logging.warning("Can't issue Async OBSERVE - GET - no path provided.")
            return False
    
    def stopObserver(self, resource: ResourceNameEnum = None, name: str = None) -> bool:
        """
        Stop observing a resource.
        
        Args:
            resource: The resource to stop observing
            name: Optional name to extend the resource path
            
        Returns:
            bool: True if observation stopped successfully
        """
        if resource or name:
            resourcePath = self._createResourcePath(resource, name)
            
            if resourcePath not in self.observeTasks:  # Check Tasks
                logging.warning(f"Resource {resourcePath} not being observed. Ignoring stop observe request.")
                return False
            
            task = self.observeTasks[resourcePath]  # Get from Tasks
            task.cancel()
            
            cleanup_future = asyncio.run_coroutine_threadsafe(
                self._handleStopObserveRequest(resourcePath, ignoreErr=True),
                self._eventLoop
            )
            
            try:
                cleanup_future.result(timeout=5.0)
                logging.info(f"Stopped observing: {resourcePath}")
                del self.observeTasks[resourcePath]  # Delete from Tasks
                return True
            except Exception as e:
                logging.error(f"Error stopping observation: {e}")
                return False
        else:
            logging.warning("Can't cancel OBSERVE - GET - no path provided.")
            return False
    
    async def _handleStartObserveRequest(self, resourcePath: str = None):
        """
        Handle async OBSERVE start request.
        
        Args:
            resourcePath: The full resource path to observe (including URI)
        """
        logging.info(f"Handle start observe invoked. Waiting for each input: {resourcePath}")
        
        try:
            msg = Message(code=Code.GET, uri=resourcePath, observe=0)
            req = self.clientContext.request(msg)
            
            # store with relative path as key
            # needed for later cleanup
            relativePath = resourcePath.replace(self.uriPath, "")
            self.observeRequests[relativePath] = req
            
            # get initial response
            responseData = await req.response
            self._onGetResponse(responseData, relativePath)
            
            # continue observation
            async for responseData in req.observation:
                self._onGetResponse(responseData, relativePath)
                
        except asyncio.CancelledError:
            # expected
            logging.info(f"Observation cancelled for {resourcePath}")
        except Exception as e:
            logging.warning(f"Failed to execute OBSERVE - GET. Error: {e}")
            traceback.print_exception(type(e), e, e.__traceback__)
        finally:
            relativePath = resourcePath.replace(self.uriPath, "")
            
            if relativePath in self.observeRequests:
                del self.observeRequests[relativePath]
    
    async def _handleStopObserveRequest(self, resourcePath: str = None, ignoreErr: bool = False):
        """
        Handle async OBSERVE stop request.
        
        Args:
            resourcePath: The resource path to stop observing (relative path)
            ignoreErr: If True, suppress error logging
        """
        if resourcePath in self.observeRequests:
            logging.info(f"Handle stop observe invoked: {resourcePath}")
            
            try:
                observeRequest = self.observeRequests[resourcePath]
                observeRequest.observation.cancel()
            except Exception as e:
                if not ignoreErr:
                    logging.warning(f"Failed to cancel OBSERVE - GET: {resourcePath}")
            
            try:
                del self.observeRequests[resourcePath]
            except Exception as e:
                if not ignoreErr:
                    logging.warning(f"Failed to remove observable from list: {resourcePath}")
        else:
            if not ignoreErr:
                logging.warning(f"Resource not currently under observation. Ignoring: {resourcePath}")
    
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
        
        # Remove leading slash if present
        if resourcePath.startswith('/'):
            resourcePath = resourcePath[1:]
        
        return resourcePath
    
    def stop(self):
        """
        Stop the async CoAP client and clean up resources.
        """
        if self._eventLoop:
            try:
                logging.info("Stopping async CoAP client...")
                self._eventLoop.call_soon_threadsafe(self._eventLoop.stop)
                logging.info("Async CoAP client stopped successfully")
            except Exception as e:
                logging.error(f"Error stopping async CoAP client: {e}")