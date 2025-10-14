"""
Device Data Manager Module

This module manages device data collection, processing, and communication
with MQTT broker integration.

Location: programmingtheiot/cda/app/DeviceDataManager.py
"""

import logging

from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector

# Import managers - create stubs if they don't exist
try:
    from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager
except ImportError:
    SystemPerformanceManager = None

try:
    from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
except ImportError:
    SensorAdapterManager = None

try:
    from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
except ImportError:
    ActuatorAdapterManager = None

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DeviceDataManager(IDataMessageListener):
    """
    Main device data manager for CDA.
    
    Manages all sensor, actuator, and system performance data collection,
    as well as MQTT client connectivity for remote communication.
    """
    
    def __init__(self):
        """
        Constructor for DeviceDataManager.
        
        Initializes configuration, managers, and MQTT client connectivity.
        """
        self.configUtil = ConfigUtil()
        
        # Initialize managers (with null checks for optional managers)
        self.sysPerfManager = SystemPerformanceManager() if SystemPerformanceManager else None
        self.sensorAdapterManager = SensorAdapterManager() if SensorAdapterManager else None
        self.actuatorAdapterManager = ActuatorAdapterManager() if ActuatorAdapterManager else None
        
        # Set data message listeners
        if self.sysPerfManager:
            self.sysPerfManager.setDataMessageListener(self)
        if self.sensorAdapterManager:
            self.sensorAdapterManager.setDataMessageListener(self)
        
        # Initialize scheduler
        pollCycles = self.configUtil.getInteger(
            ConfigConst.CONSTRAINED_DEVICE,
            ConfigConst.POLLING_CYCLES_KEY,
            ConfigConst.DEFAULT_POLLING_CYCLES
        )
        
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(
            self.handleTelemetry,
            'interval',
            seconds=pollCycles
        )
        
        # Initialize MQTT client based on configuration
        self.enableMqttClient = \
            self.configUtil.getBoolean(
                section=ConfigConst.CONSTRAINED_DEVICE,
                key=ConfigConst.ENABLE_MQTT_CLIENT_KEY
            )
        
        self.mqttClient = None
        
        if self.enableMqttClient:
            logging.info("MQTT client enabled. Initializing MqttClientConnector...")
            self.mqttClient = MqttClientConnector()
            self.mqttClient.setDataMessageListener(self)
        else:
            logging.info("MQTT client disabled in configuration.")
    
    def handleActuatorCommandRequest(self, data: ActuatorData) -> ActuatorData:
        """
        Handles actuator command requests.
        
        Args:
            data: ActuatorData instance containing command information
            
        Returns:
            ActuatorData: Response from actuator
        """
        logging.info("Processing actuator command request...")
        
        if data:
            logging.debug(f"Actuator data: {data}")
            if self.actuatorAdapterManager:
                response = self.actuatorAdapterManager.sendActuatorCommand(data)
                return response
            else:
                logging.warning("ActuatorAdapterManager not available")
        else:
            logging.warning("Received empty actuator command request.")
        
        return None
    
    def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
        """
        Handles actuator command responses.
        
        Args:
            data: ActuatorData instance containing response information
            
        Returns:
            bool: Success status
        """
        logging.info("Processing actuator command response...")
        
        if data:
            logging.debug(f"Actuator response: {data}")
            # Process the response (could be sent to cloud, logged, etc.)
            return True
        else:
            logging.warning("Received empty actuator command response.")
            return False
    
    def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
        """
        Callback for handling incoming messages from MQTT.
        
        Args:
            resourceEnum: The resource type/topic
            msg: Message payload as string
            
        Returns:
            bool: Success status
        """
        logging.info(f"Handling incoming message from resource: {resourceEnum}")
        logging.debug(f"Message payload: {msg}")
        
        try:
            # Parse the message and handle based on resource type
            if resourceEnum == ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE:
                # Convert message to ActuatorData and process
                from programmingtheiot.data.DataUtil import DataUtil
                dataUtil = DataUtil()
                actuatorData = dataUtil.jsonToActuatorData(msg)
                
                if actuatorData:
                    self.handleActuatorCommandRequest(actuatorData)
                    return True
            
            return False
            
        except Exception as e:
            logging.error(f"Error handling incoming message: {e}")
            return False
    
    def handleSensorMessage(self, data: SensorData) -> bool:
        """
        Handles sensor data messages.
        
        Args:
            data: SensorData instance
            
        Returns:
            bool: Success status
        """
        logging.info("Processing sensor message...")
        
        if data:
            logging.debug(f"Sensor data: {data}")
            # Process sensor data (could be sent to cloud, stored, etc.)
            return True
        else:
            logging.warning("Received empty sensor message.")
            return False
    
    def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
        """
        Handles system performance data messages.
        
        Args:
            data: SystemPerformanceData instance
            
        Returns:
            bool: Success status
        """
        logging.info("Processing system performance message...")
        
        if data:
            logging.debug(f"System performance data: {data}")
            # Process system performance data
            return True
        else:
            logging.warning("Received empty system performance message.")
            return False
    
    def handleTelemetry(self):
        """
        Periodic telemetry handling method.
        
        Called by scheduler to collect and process sensor and system data.
        """
        logging.debug("Handling telemetry data...")
        
        # Trigger system performance manager
        if self.sysPerfManager:
            self.sysPerfManager.handleTelemetry()
        
        # Trigger sensor adapter manager
        if self.sensorAdapterManager:
            self.sensorAdapterManager.handleTelemetry()
    
    def startManager(self):
        """
        Starts the DeviceDataManager and all sub-managers.
        
        Initializes MQTT connection and starts scheduled tasks.
        """
        logging.info("Starting DeviceDataManager...")
        
        # Start the scheduler
        if not self.scheduler.running:
            self.scheduler.start()
            logging.info("Scheduler started.")
        
        # Connect MQTT client if enabled
        if self.mqttClient:
            logging.info("Connecting MQTT client to broker...")
            self.mqttClient.connectClient()
            
            # Subscribe to actuator command topic
            self.mqttClient.subscribeToTopic(
                resource=ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE,
                callback=None,
                qos=ConfigConst.DEFAULT_QOS
            )
            
            logging.info("MQTT client connected and subscribed to topics.")
        
        logging.info("DeviceDataManager started successfully.")
    
    def stopManager(self):
        """
        Stops the DeviceDataManager and all sub-managers.
        
        Disconnects MQTT client and stops scheduled tasks.
        """
        logging.info("Stopping DeviceDataManager...")
        
        # Stop the scheduler
        if self.scheduler.running:
            self.scheduler.shutdown()
            logging.info("Scheduler stopped.")
        
        # Disconnect MQTT client if enabled
        if self.mqttClient:
            logging.info("Disconnecting MQTT client from broker...")
            
            # Unsubscribe from topics
            self.mqttClient.unsubscribeFromTopic(
                resource=ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE
            )
            
            # Disconnect client
            self.mqttClient.disconnectClient()
            
            logging.info("MQTT client disconnected.")
        
        logging.info("DeviceDataManager stopped successfully.")