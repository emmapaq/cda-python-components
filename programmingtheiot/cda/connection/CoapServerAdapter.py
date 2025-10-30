##
# This class is part of the Programming the Internet of Things project.
#
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
##

import logging
import traceback

from threading import Thread

from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.IDataMessageListener import IDataMessageListener


class CoapServerAdapter():
    """
    CoAP Server Adapter for hosting CoAP resources in the Constrained Device Application (CDA).
    
    This implementation uses the CoAPthon3 library with threading support to provide
    a CoAP server that can handle GET, PUT, POST, and DELETE requests for various
    IoT resources including telemetry data, actuator commands, and system performance.
    """
    
    def __init__(self, dataMsgListener: IDataMessageListener = None):
        """
        Initialize the CoAP server adapter.
        
        This constructor:
        - Loads configuration from the config file
        - Sets up the server host and port
        - Initializes the CoAP server instance
        - Registers the data message listener for callbacks
        
        Args:
            dataMsgListener: An IDataMessageListener implementation that will
                           receive callbacks when data messages are received.
                           Typically this will be DeviceDataManager.
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
        
        # Initialize server and thread references
        self.coapServer = None
        self.coapServerTask = None
        
        # Set listen timeout for server loop
        self.listenTimeout = 30
        
        # Initialize the CoAP server
        self._initServer()
        
        logging.info(f"CoAP server configured for host and port: {self.serverUri}")
    
    
    def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
        """
        Set or update the data message listener for this adapter.
        
        The data message listener will receive callbacks when data messages
        are received by the CoAP server (e.g., actuator commands, sensor data).
        
        Args:
            listener: The IDataMessageListener implementation to register.
            
        Returns:
            bool: True if the listener was set successfully, False otherwise.
        """
        if listener:
            self.dataMsgListener = listener
            return True
        
        return False
    
    
    def addResource(self, resourcePath: ResourceNameEnum = None, endName: str = None, resource = None):
        """
        Add a resource handler to the CoAP server.
        
        This method parses the resource path and registers the resource handler
        with the CoAP server's resource tree. It handles hierarchical paths
        like /PIOT/ConstrainedDevice/SensorMsg as a tree structure.
        
        Args:
            resourcePath: The ResourceNameEnum representing the resource path.
            endName: Optional endpoint name (final segment of the path).
            resource: The resource handler instance (must extend coapthon Resource).
        """
        if resourcePath and resource:
            uriPath = resourcePath.value
            
            if endName:
                uriPath = uriPath + '/' + endName
                resource.name = endName
            
            # Parse the path into components
            trimmedUriPath = uriPath.strip("/")
            resourceList = trimmedUriPath.split("/")
            resourceTree = None
            registrationPath = ""
            generationCount = 0
            
            # Navigate through the resource tree
            for resourceName in resourceList:
                generationCount = generationCount + 1
                registrationPath = registrationPath + "/" + resourceName
                
                try:
                    resourceTree = self.coapServer.root[registrationPath]
                except KeyError:
                    resourceTree = None
            
            # Register the resource if not already in tree
            if not resourceTree:
                if len(resourceList) != generationCount:
                    logging.warning(f"Resource path mismatch: {resourcePath.value}")
                    return None
                
                resource.path = registrationPath
                self.coapServer.root[registrationPath] = resource
                logging.info(f"Added resource at path: {registrationPath}")
        else:
            logging.warning(f"No resource provided for path: {resourcePath}")
    
    
    def startServer(self):
        """
        Start the CoAP server in a separate daemon thread.
        
        This method:
        - Checks if the server is initialized
        - Stops any existing server task
        - Creates a new daemon thread to run the server
        - Starts the server thread
        
        The daemon thread ensures the server won't prevent application shutdown.
        """
        if self.coapServer:
            logging.info("Starting CoAP server...")
            
            # Stop existing server task if it's still running
            if self.coapServerTask and self.coapServerTask.isAlive():
                logging.info("CoAP server task already running. Stopping...")
                self.stopServer()
                self.coapServerTask = None
            
            # Create and start new server thread
            self.coapServerTask = Thread(target=self._runServer)
            self.coapServerTask.setDaemon(True)
            self.coapServerTask.start()
            
            logging.info("\n\n***** CoAP server started. *****\n\n")
        else:
            logging.warning("CoAP server not yet initialized (shouldn't happen).")
    
    
    def stopServer(self):
        """
        Stop the CoAP server and cleanup resources.
        
        This method:
        - Closes the CoAP server connection
        - Waits for the server thread to terminate (with 5 second timeout)
        - Cleans up server resources
        """
        if self.coapServer:
            logging.info("Stopping CoAP server...")
            
            # Close the server
            self.coapServer.close()
            
            # Wait for server thread to finish (max 5 seconds)
            if self.coapServerTask:
                self.coapServerTask.join(5)
            
            logging.info("CoAP server stopped.")
        else:
            logging.warning("CoAP server not yet initialized (shouldn't happen).")
    
    
    def _initServer(self):
        """
        Initialize the CoAP server instance and register resource handlers.
        
        This private method:
        - Creates the CoAP server instance bound to configured host/port
        - Creates and registers all resource handlers
        - Sets up callbacks for data listeners
        """
        try:
            # Create CoAP server instance bound to configured host and port
            self.coapServer = CoAP(server_address=(self.host, self.port))
            
            logging.info(f"CoAP server instance created and bound to {self.host}:{self.port}")
            
            # Import handlers
            from programmingtheiot.cda.connection.handlers.GetSystemPerformanceResourceHandler import GetSystemPerformanceResourceHandler
            from programmingtheiot.cda.connection.handlers.GetTelemetryResourceHandler import GetTelemetryResourceHandler
            from programmingtheiot.cda.connection.handlers.UpdateActuatorResourceHandler import UpdateActuatorResourceHandler
            
            # Create and register actuator resource handlers
            # Humidifier actuator
            self.addResource(
                resourcePath=ResourceNameEnum.CDA_ACTUATOR_CMD,
                endName=ConfigConst.HUMIDIFIER_ACTUATOR_NAME,
                resource=UpdateActuatorResourceHandler(dataMsgListener=self.dataMsgListener)
            )
            
            # HVAC actuator
            self.addResource(
                resourcePath=ResourceNameEnum.CDA_ACTUATOR_CMD,
                endName=ConfigConst.HVAC_ACTUATOR_NAME,
                resource=UpdateActuatorResourceHandler(dataMsgListener=self.dataMsgListener)
            )
            
            # Create and register system performance resource handler
            sysPerfDataListener = GetSystemPerformanceResourceHandler(
                coap_server=self.coapServer,
                dataMsgListener=self.dataMsgListener
            )
            
            self.addResource(
                resourcePath=ResourceNameEnum.CDA_SYSTEM_PERF,
                resource=sysPerfDataListener
            )
            
            # Create and register telemetry/sensor resource handler
            telemetryDataListener = GetTelemetryResourceHandler(
                coap_server=self.coapServer,
                dataMsgListener=self.dataMsgListener
            )
            
            self.addResource(
                resourcePath=ResourceNameEnum.CDA_SENSOR_DATA,
                resource=telemetryDataListener
            )
            
            # Register callbacks with data message listener
            if self.dataMsgListener:
                # These will be used in Lab Module 10
                # self.dataMsgListener.setSystemPerformanceDataListener(sysPerfDataListener)
                # self.dataMsgListener.setTelemetryDataListener(telemetryDataListener)
                pass
            
            logging.info("Created CoAP server with default resources.")
            
        except Exception as e:
            logging.error(f"Failed to initialize CoAP server: {e}")
            traceback.print_exc()
            self.coapServer = None
    
    
    def _runServer(self):
        """
        Run the CoAP server listener loop.
        
        This private method is called by the server thread and runs the
        CoAP server's listen loop, which processes incoming requests.
        The loop runs continuously to keep the server accepting requests.
        
        Handles exceptions gracefully and logs any errors that occur.
        """
        try:
            if self.coapServer:
                logging.info("CoAP server listening...")
                
                # Keep listening indefinitely
                while True:
                    self.coapServer.listen(self.listenTimeout)
                    
            else:
                logging.warning("CoAP server instance not initialized.")
        except KeyboardInterrupt:
            logging.info("CoAP server interrupted")
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            logging.warning("Failed to run CoAP server.")