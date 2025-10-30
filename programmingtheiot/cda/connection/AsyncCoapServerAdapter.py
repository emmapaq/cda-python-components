##
# This class is part of the Programming the Internet of Things project.
#
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
##

import logging
import asyncio
import time
import traceback
import threading

import aiocoap
import aiocoap.resource as resource

from aiocoap.resource import Resource

from typing import Optional, Dict, Any
from contextlib import suppress

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.common.IDataMessageListener import IDataMessageListener

# TODO: Uncomment these when implementing PIOT-CDA-08-002-A
# from programmingtheiot.cda.connection.handlers.AsyncGetTelemetryResourceHandler import AsyncGetTelemetryResourceHandler
# from programmingtheiot.cda.connection.handlers.AsyncGetSystemPerformanceResourceHandler import AsyncGetSystemPerformanceResourceHandler
# from programmingtheiot.cda.connection.handlers.AsyncUpdateActuatorResourceHandler import AsyncUpdateActuatorResourceHandler


class AsyncCoapServerAdapter():
    """
    Async CoAP Server Adapter using aiocoap library with asyncio.
    
    This implementation provides an asynchronous CoAP server that can handle
    GET, PUT, POST, and DELETE requests using Python's asyncio framework.
    """
    
    def __init__(self, dataMsgListener: IDataMessageListener = None):
        """
        Initialize the Async CoAP server adapter.
        
        Args:
            dataMsgListener: An IDataMessageListener implementation for callbacks
        """
        self.config = ConfigUtil()
        self.dataMsgListener = dataMsgListener
        self.enableConfirmedMsgs = False
        
        # Get CoAP server configuration from config file
        self.host = self.config.getProperty(
            ConfigConst.COAP_GATEWAY_SERVICE,
            ConfigConst.HOST_KEY,
            ConfigConst.DEFAULT_HOST
        )
        
        self.port = self.config.getInteger(
            ConfigConst.COAP_GATEWAY_SERVICE,
            ConfigConst.PORT_KEY,
            ConfigConst.DEFAULT_COAP_PORT
        )
        
        self.serverUri = f"coap://{self.host}:{self.port}"
        
        # Initialize server components
        self.coapServer = None
        self.rootResource = None
        
        # Async components for event loop management
        self._serverTask: Optional[asyncio.Task] = None
        self._eventLoopThread: Optional[asyncio.AbstractEventLoop] = None
        self._executionThread: Optional[threading.Thread] = None
        self._shutdownEvent: Optional[asyncio.Event] = None
        self._shutdownFuture: Optional[asyncio.Future] = None
        
        # Initialize the server
        self._initServer()
        
        logging.info(f"Async CoAP Server configured at {self.serverUri}")
    
    
    def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
        """
        Set or update the data message listener.
        
        The data message listener will receive callbacks when data messages
        are received by the CoAP server.
        
        Args:
            listener: The IDataMessageListener implementation
            
        Returns:
            bool: True if listener was set successfully
        """
        if listener:
            self.dataMsgListener = listener
            return True
        
        return False
    
    
    def addResource(self, resourcePath: ResourceNameEnum = None, endName: str = None, resource: Resource = None):
        """
        Add a resource handler to the CoAP server.
        
        This method parses the resource path and registers the resource handler
        with the aiocoap server's resource tree.
        
        Args:
            resourcePath: The ResourceNameEnum representing the resource path
            endName: Optional endpoint name (final segment of the path)
            resource: The resource handler instance (aiocoap Resource)
        """
        if resourcePath and resource:
            uriPath = resourcePath.value
            
            if endName:
                uriPath = uriPath + '/' + endName
            
            resourceList = uriPath.split('/')
            
            if not self.rootResource:
                self.rootResource = resource.Site()
            
            logging.info(f"Adding resource to server: {resourceList}")
            
            try:
                self.rootResource.add_resource(resourceList, resource)
            except Exception as e:
                logging.error(f"Failed to add resource to server: {resourceList}")
                traceback.print_exc()
        else:
            logging.warning(f"No resource provided for path: {resourcePath}")
    
    
    def startServer(self) -> bool:
        """
        Start the Async CoAP server in a separate thread.
        
        Creates a new event loop, initializes the shutdown event, and starts
        the server thread. The server runs in daemon mode.
        
        Returns:
            bool: True if server started successfully, False otherwise
        """
        if self._serverTask and not self._serverTask.done():
            logging.warning("Server already running. Ignoring start request.")
            return False
        
        if not self.rootResource:
            logging.error("No resources configured. Nothing for server to do.")
            return False
        
        try:
            logging.info(f"Starting Async CoAP Server at {self.serverUri}")
            
            # Create new event loop for the server
            self._eventLoopThread = asyncio.new_event_loop()
            self._shutdownEvent = asyncio.Event()
            
            # Create and start the server thread
            self._executionThread = threading.Thread(
                target=self._runServerTask,
                daemon=True,
                name="Async-CoAP-Server-Thread"
            )
            
            self._executionThread.start()
            
            # Wait a fraction of a second so server can spin up
            time.sleep(0.5)
            
            logging.info(f"\n\n***** Async CoAP Server started. *****\n\n")
            logging.info(f"Async CoAP Server started at {self.serverUri}")
            
            return True
        
        except Exception as e:
            logging.error(f"Failed to start Async CoAP Server at {self.serverUri}")
            traceback.print_exception(type(e), e, e.__traceback__)
            return False
    
    
    def stopServer(self) -> bool:
        """
        Stop the Async CoAP server.
        
        Initiates graceful shutdown of the server, waiting up to 5 seconds
        for the server task to complete.
        
        Returns:
            bool: True if server stopped successfully, False otherwise
        """
        if not self._eventLoopThread or not self._serverTask:
            logging.warning("Async CoAP Server not yet running. Ignoring stop request.")
            return False
        
        try:
            logging.info(f"Shutting down Async CoAP Server at {self.serverUri}")
            
            if self._eventLoopThread.is_running():
                asyncio.run_coroutine_threadsafe(
                    self._shutdownServer(),
                    self._eventLoopThread
                )
            
            # Wait for server to shutdown (max 5 seconds)
            for _ in range(5):
                if self._serverTask.done():
                    break
                time.sleep(1.0)
            
            if self._eventLoopThread.is_running():
                self._eventLoopThread.call_soon_threadsafe(self._eventLoopThread.stop)
            
            logging.info(f"Async CoAP Server shutdown: {self.serverUri}")
            
            return True
        
        except Exception as e:
            logging.error(f"Failed to shutdown Async CoAP Server at {self.serverUri}")
            traceback.print_exception(type(e), e, e.__traceback__)
            return False
    
    
    def _initServer(self):
        """
        Initialize the CoAP server and prepare resources.
        
        This is a placeholder for resource registration which will be
        implemented in PIOT-CDA-08-002-A when resource handlers are created.
        
        Note:
            Full implementation including resource handler registration
            will be added in PIOT-CDA-08-002-A.
        """
        # TODO: Register resource handlers in PIOT-CDA-08-002-A
        pass
    
    
    def _runServerTask(self):
        """
        Run the server task in the event loop thread.
        
        This method runs in a separate thread and manages the asyncio event loop.
        It sets the event loop for the current thread and runs it forever.
        """
        try:
            # Set this thread's event loop
            asyncio.set_event_loop(self._eventLoopThread)
            
            # Create the server task
            self._serverTask = self._eventLoopThread.create_task(self._runServer())
            
            # Run the event loop forever
            self._eventLoopThread.run_forever()
            
        except Exception as e:
            logging.error("Error in server task execution")
            traceback.print_exception(type(e), e, e.__traceback__)
    
    
    async def _runServer(self):
        """
        Run the CoAP server (async coroutine).
        
        Creates the aiocoap Context bound to the configured host and port,
        then keeps the server running until shutdown is requested.
        """
        try:
            logging.info("Creating aiocoap server context...")
            
            # Create the CoAP server context
            self.coapServer = await aiocoap.Context.create_server_context(
                self.rootResource,
                bind=(self.host, self.port)
            )
            
            logging.info(f"Async CoAP server listening on {self.host}:{self.port}")
            
            # Keep server running
            await self._keepServerRunning()
            
        except Exception as e:
            logging.error("Failed to run Async CoAP server")
            traceback.print_exception(type(e), e, e.__traceback__)
    
    
    async def _keepServerRunning(self):
        """
        Keep the server running until shutdown is requested (async coroutine).
        
        Waits for the shutdown event to be set, keeping the server alive
        and processing requests.
        """
        try:
            # Wait indefinitely until shutdown is requested
            await self._shutdownEvent.wait()
            logging.info("Shutdown event received")
            
        except Exception as e:
            logging.error("Error in keep server running")
            traceback.print_exception(type(e), e, e.__traceback__)
    
    
    async def _shutdownServer(self):
        """
        Shutdown the CoAP server (async coroutine).
        
        Sets the shutdown event and performs cleanup of the aiocoap context.
        """
        try:
            logging.info("Initiating server shutdown...")
            
            # Signal shutdown
            if self._shutdownEvent:
                self._shutdownEvent.set()
            
            # Shutdown the aiocoap context
            if self.coapServer:
                await self.coapServer.shutdown()
            
            logging.info("Server shutdown complete")
            
        except Exception as e:
            logging.error("Error during server shutdown")
            traceback.print_exception(type(e), e, e.__traceback__)