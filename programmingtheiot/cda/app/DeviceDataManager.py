"""
Device Data Manager Module

This module manages device data collection, processing, and communication
with MQTT broker and CoAP server integration.

Location: programmingtheiot/cda/app/DeviceDataManager.py

@author: Emma
"""

import logging
import time

from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.cda.connection.CoapServerAdapter import CoapServerAdapter
from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from programmingtheiot.data.DataUtil import DataUtil

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


class DeviceDataManager(IDataMessageListener):
    """
    Main device data manager for CDA.
    
    Manages all sensor, actuator, and system performance data collection,
    as well as MQTT client connectivity, CoAP server, and CoAP client for 
    remote communication.
    """
    
    def __init__(self, disableAllComms: bool = False):
        """
        Constructor for DeviceDataManager.
        
        Initializes configuration, managers, MQTT client connectivity,
        CoAP server, and CoAP client.
        
        Args:
            disableAllComms (bool): If True, disables all MQTT and CoAP connectivity.
                                   Useful for testing without network connections.
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
        
        # Determine if communications should be enabled
        if disableAllComms:
            # Force disable all communications (for testing)
            self.enableMqttClient = False
            self.enableCoapServer = False
            self.enableCoapClient = False
            logging.info("All communications disabled via constructor parameter.")
        else:
            # Read from configuration
            self.enableMqttClient = \
                self.configUtil.getBoolean(
                    section=ConfigConst.CONSTRAINED_DEVICE,
                    key=ConfigConst.ENABLE_MQTT_CLIENT_KEY
                )
            
            self.enableCoapServer = \
                self.configUtil.getBoolean(
                    section=ConfigConst.CONSTRAINED_DEVICE,
                    key=ConfigConst.ENABLE_COAP_SERVER_KEY
                )
            
            self.enableCoapClient = \
                self.configUtil.getBoolean(
                    section=ConfigConst.CONSTRAINED_DEVICE,
                    key=ConfigConst.ENABLE_COAP_CLIENT_KEY
                )
        
        # Initialize MQTT client based on configuration
        self.mqttClient = None
        
        if self.enableMqttClient:
            logging.info("MQTT client enabled. Initializing MqttClientConnector...")
            self.mqttClient = MqttClientConnector()
            self.mqttClient.setDataMessageListener(self)
        else:
            logging.info("MQTT client disabled.")
        
        # Initialize CoAP server based on configuration
        self.coapServer = None
        
        if self.enableCoapServer:
            logging.info("CoAP server enabled. Initializing CoapServerAdapter...")
            self.coapServer = CoapServerAdapter(dataMsgListener=self)
        else:
            logging.info("CoAP server disabled.")
        
        # Initialize CoAP client based on configuration
        self.coapClient = None
        
        if self.enableCoapClient:
            logging.info("CoAP client enabled. Initializing CoapClientConnector...")
            self.coapClient = CoapClientConnector(dataMsgListener=self)
        else:
            logging.info("CoAP client disabled.")
        
        logging.info("DeviceDataManager initialization complete.")
    
            # Fermentation-specific attributes
        self.currentFermentationProfile = ConfigConst.FERMENTATION_PROFILE_ALE
        self.currentTempMin = ConfigConst.ALE_TEMP_MIN
        self.currentTempMax = ConfigConst.ALE_TEMP_MAX
        self.currentHumidityMin = ConfigConst.ALE_HUMIDITY_MIN
        self.currentHumidityMax = ConfigConst.ALE_HUMIDITY_MAX
        
        # Temperature spike detection
        self.recentTemperatures = []  # Store last N readings
        self.maxTempHistorySize = 15   # 30 minutes at 2-min intervals
        
        # LED state tracking
        self.currentLedState = ConfigConst.LED_OPTIMAL_CMD
    
    # =========================================================================
    # IDataMessageListener Interface Implementation - Message Handlers
    # =========================================================================
    
    def handleActuatorCommandMessage(self, data: ActuatorData) -> ActuatorData:
        """
        Handles incoming actuator command messages from the GDA.
        
        This method receives ActuatorData command messages (typically from MQTT or CoAP),
        validates them, and forwards them to the ActuatorAdapterManager for execution.
        
        Args:
            data (ActuatorData): The actuator command message to process
            
        Returns:
            ActuatorData: The response from the actuator with updated state, or None if processing failed
        """
        if data:
            logging.info("Processing actuator command message.")
            
            # TODO: add further validation before sending the command
            
            if self.actuatorAdapterManager:
                return self.actuatorAdapterManager.sendActuatorCommand(data)
            else:
                logging.warning("ActuatorAdapterManager not available")
                return None
        else:
            logging.warning("Received invalid ActuatorData command message. Ignoring.")
            return None
    
    def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
        """
        Handles actuator command responses.
        
        Publishes actuator responses back to the GDA via MQTT/CoAP.
        
        Args:
            data: ActuatorData instance containing response information
            
        Returns:
            bool: Success status
        """
        if data:
            logging.info("Incoming actuator response received (from actuator manager): " + str(data))
            
            # Convert ActuatorData to JSON
            jsonData = DataUtil().actuatorDataToJson(data)
            
            # Send response upstream to GDA
            self._handleUpstreamTransmission(
                resource=ResourceNameEnum.CDA_ACTUATOR_RESPONSE,
                msg=jsonData
            )
            
            return True
        else:
            logging.warning("Received empty actuator command response.")
            return False
    
    def handleSensorMessage(self, data: SensorData) -> bool:
        """
        Handles sensor data messages.
        
        Analyzes sensor data for threshold crossings and sends data to GDA.
        
        Args:
            data: SensorData instance
            
        Returns:
            bool: Success status
        """
        if data:
            logging.info("Incoming sensor data received (from sensor manager): " + str(data))
            
            # Analyze sensor data for threshold crossings and trigger actuations
            self._handleSensorDataAnalysis(data=data)
            
            # Convert the SensorData instance to JSON
            jsonData = DataUtil().sensorDataToJson(data=data)
            
            # Pass the resource and newly generated JSON data to upstream transmission
            self._handleUpstreamTransmission(
                resource=ResourceNameEnum.CDA_SENSOR_DATA,
                msg=jsonData
            )
            
            return True
        else:
            logging.warning("Incoming sensor data is invalid (null). Ignoring.")
            
            return False
    
    def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
        """
        Handles system performance data messages.
        
        Sends system performance data to GDA.
        
        Args:
            data: SystemPerformanceData instance
            
        Returns:
            bool: Success status
        """
        if data:
            logging.info("Incoming system performance data received: " + str(data))
            
            # Convert the SystemPerformanceData instance to JSON
            jsonData = DataUtil().systemPerformanceDataToJson(data=data)
            
            # Pass the resource and newly generated JSON data to upstream transmission
            self._handleUpstreamTransmission(
                resource=ResourceNameEnum.CDA_SYSTEM_PERF,
                msg=jsonData
            )
            
            return True
        else:
            logging.warning("Incoming system performance data is invalid (null). Ignoring.")
            
            return False
    
    def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
        """
        Callback for handling incoming messages from MQTT or CoAP.
        
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
            if resourceEnum == ResourceNameEnum.CDA_ACTUATOR_CMD:
                # Convert message to ActuatorData and process
                actuatorData = DataUtil().jsonToActuatorData(msg)
                
                if actuatorData:
                    self.handleActuatorCommandMessage(actuatorData)
                    return True
            
            return False
            
        except Exception as e:
            logging.error(f"Error handling incoming message: {e}")
            return False
    
    
    # =========================================================================
    # Private Methods - Data Analysis and Transmission
    # =========================================================================
    
    def _handleSensorDataAnalysis(self, data: SensorData):
        """
        Analyzes sensor data for threshold crossings and triggers actuator responses.
        
        Checks if temperature crosses configured floor or ceiling thresholds and
        triggers appropriate actuator commands to adjust temperature.
        
        Args:
            data (SensorData): The sensor data to analyze
        """
        if not data:
            return
        
        # Only analyze temperature sensor data for now
        if data.getTypeID() != ConfigConst.TEMP_SENSOR_TYPE:
            return
        
        logging.info("Analyzing temperature sensor data for threshold crossings...")
        
        # Get configured thresholds from config
        nominalTempFloor = self.configUtil.getFloat(
            ConfigConst.CONSTRAINED_DEVICE,
            "nominalTempFloor",
            18.0
        )
        
        nominalTempCeiling = self.configUtil.getFloat(
            ConfigConst.CONSTRAINED_DEVICE,
            "nominalTempCeiling",
            24.0
        )
        
        currentTemp = data.getValue()
        
        logging.debug(f"Temperature: {currentTemp}, Floor: {nominalTempFloor}, Ceiling: {nominalTempCeiling}")
        
        # Check for threshold crossings
        if currentTemp < nominalTempFloor:
            logging.info(f"Temperature {currentTemp} below floor {nominalTempFloor}. Triggering HVAC to raise temperature.")
            
            # Create actuator command to turn on heating
            actuatorData = ActuatorData()
            actuatorData.setName(ConfigConst.HVAC_ACTUATOR_NAME)
            actuatorData.setTypeID(ConfigConst.HVAC_ACTUATOR_TYPE)
            actuatorData.setCommand(ConfigConst.COMMAND_ON)
            actuatorData.setValue(nominalTempFloor)
            actuatorData.setStateData(f"Temperature too low: {currentTemp}°C. Raising to {nominalTempFloor}°C.")
            
            # Send command to actuator
            self.handleActuatorCommandMessage(actuatorData)
        
        elif currentTemp > nominalTempCeiling:
            logging.info(f"Temperature {currentTemp} above ceiling {nominalTempCeiling}. Triggering HVAC to lower temperature.")
            
            # Create actuator command to turn on cooling
            actuatorData = ActuatorData()
            actuatorData.setName(ConfigConst.HVAC_ACTUATOR_NAME)
            actuatorData.setTypeID(ConfigConst.HVAC_ACTUATOR_TYPE)
            actuatorData.setCommand(ConfigConst.COMMAND_ON)
            actuatorData.setValue(nominalTempCeiling)
            actuatorData.setStateData(f"Temperature too high: {currentTemp}°C. Lowering to {nominalTempCeiling}°C.")
            
            # Send command to actuator
            self.handleActuatorCommandMessage(actuatorData)
        
        else:
            logging.debug(f"Temperature {currentTemp} within normal range [{nominalTempFloor}, {nominalTempCeiling}].")
    
    def _handleUpstreamTransmission(self, resource: ResourceNameEnum = None, msg: str = None):
        """
        Handles upstream transmission of data to the GDA.
        
        Sends data to the GDA via MQTT and/or CoAP based on configuration.
        
        Args:
            resource (ResourceNameEnum): The resource/topic to send to
            msg (str): The message payload (JSON string)
        """
        if not resource or not msg:
            logging.warning("Resource or message is null. Cannot transmit upstream.")
            return
        
        logging.info("Upstream transmission invoked. Checking comm's integration.")
        
        # NOTE: If using MQTT, the following will attempt to publish the message to the broker
        if self.mqttClient:
            if self.mqttClient.publishMessage(resource=resource, msg=msg):
                logging.debug("Published incoming data to resource (MQTT): %s", str(resource))
            else:
                logging.warning("Failed to publish incoming data to resource (MQTT): %s", str(resource))
        
        # NOTE: If using CoAP, the following will attempt to POST the message to the server
        if self.coapClient:
            if self.coapClient.sendPostRequest(resource=resource, payload=msg):
                logging.debug("Posted incoming message data to resource (CoAP): %s", str(resource))
            else:
                logging.warning("Failed to post incoming message data to resource (CoAP): %s", str(resource))
    
    
    # =========================================================================
    # Public Methods - Lifecycle Management
    # =========================================================================
    
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
        
        Initializes MQTT connection, starts CoAP server, and starts scheduled tasks.
        Note: CoAP client is stateless and doesn't require start/stop.
        """
        logging.info("Starting DeviceDataManager...")
        
        # Start the scheduler
        if not self.scheduler.running:
            self.scheduler.start()
            logging.info("Scheduler started.")
        
        # Connect MQTT client if enabled
        # NOTE: Subscription now handled in onConnect() callback
        if self.mqttClient:
            logging.info("Connecting MQTT client to broker...")
            self.mqttClient.connectClient()
            logging.info("MQTT client connected.")
        
        # Start CoAP server if enabled
        if self.coapServer:
            logging.info("Starting CoAP server...")
            self.coapServer.startServer()
            logging.info("CoAP server started successfully.")
        
        # CoAP client is stateless - no start needed
        if self.coapClient:
            logging.info("CoAP client initialized and ready for use.")
        
        logging.info("DeviceDataManager started successfully.")
    
    def stopManager(self):
        """
        Stops the DeviceDataManager and all sub-managers.
        
        Disconnects MQTT client, stops CoAP server, and stops scheduled tasks.
        Note: CoAP client is stateless and doesn't require start/stop.
        """
        logging.info("Stopping DeviceDataManager...")
        
        # Stop the scheduler
        if self.scheduler.running:
            self.scheduler.shutdown()
            logging.info("Scheduler stopped.")
        
        # Disconnect MQTT client if enabled
        if self.mqttClient:
            logging.info("Disconnecting MQTT client from broker...")
            self.mqttClient.disconnectClient()
            logging.info("MQTT client disconnected.")
        
        # Stop CoAP server if enabled
        if self.coapServer:
            logging.info("Stopping CoAP server...")
            self.coapServer.stopServer()
            logging.info("CoAP server stopped successfully.")
        
        # CoAP client is stateless - no stop needed
        if self.coapClient:
            logging.info("CoAP client resources released.")
        
        logging.info("DeviceDataManager stopped successfully.")
    
    
    # =========================================================================
    # IDataMessageListener Interface Implementation - Cache Methods
    # =========================================================================
    
    def getLatestActuatorDataResponseFromCache(self, name: str = None) -> ActuatorData:
        """
        Retrieves the named actuator data (response) item from the internal data cache.
        
        @param name The name of the actuator (optional)
        @return ActuatorData The latest actuator response data, or None if not found
        """
        # TODO: Implement caching mechanism if needed
        return None
    
    def getLatestSensorDataFromCache(self, name: str = None) -> SensorData:
        """
        Retrieves the named sensor data item from the internal data cache.
        
        @param name The name of the sensor (optional)
        @return SensorData The latest sensor data, or None if not found
        """
        # TODO: Implement caching mechanism if needed
        return None
    
    def getLatestSystemPerformanceDataFromCache(self, name: str = None) -> SystemPerformanceData:
        """
        Retrieves the named system performance data from the internal data cache.
        
        @param name The name of the system performance metric (optional)
        @return SystemPerformanceData The latest system performance data, or None if not found
        """
        # TODO: Implement caching mechanism if needed
        return None
    
    def setSystemPerformanceDataListener(self, listener) -> bool:
        """
        Sets the system performance data listener.
        
        @param listener The listener reference
        @return bool True on success
        """
        # TODO: Implement if needed
        return True
    
    def setTelemetryDataListener(self, name: str = None, listener = None) -> bool:
        """
        Sets the named telemetry data listener.
        
        @param name The name of the listener
        @param listener The listener reference
        @return bool True on success
        """
        # TODO: Implement if needed
        return True
    
    def _handleFermentationProfileCommand(self, data: ActuatorData) -> bool:
        """
        Process fermentation profile change commands from GDA/Cloud.
        
        Expected ActuatorData format:
        - actuatorType: FERMENTATION_PROFILE_ACTUATOR_TYPE
        - command: Profile name (ALE, LAGER, CONDITIONING, COLD_CRASH)
        """
        if data.getCommand():
            profileName = data.getCommand().upper()
            
            logging.info(f"Received profile change command: {profileName}")
            
            if profileName == ConfigConst.FERMENTATION_PROFILE_ALE:
                self.currentTempMin = ConfigConst.ALE_TEMP_MIN
                self.currentTempMax = ConfigConst.ALE_TEMP_MAX
                self.currentHumidityMin = ConfigConst.ALE_HUMIDITY_MIN
                self.currentHumidityMax = ConfigConst.ALE_HUMIDITY_MAX
                self.currentFermentationProfile = profileName
                
            elif profileName == ConfigConst.FERMENTATION_PROFILE_LAGER:
                self.currentTempMin = ConfigConst.LAGER_TEMP_MIN
                self.currentTempMax = ConfigConst.LAGER_TEMP_MAX
                self.currentHumidityMin = ConfigConst.LAGER_HUMIDITY_MIN
                self.currentHumidityMax = ConfigConst.LAGER_HUMIDITY_MAX
                self.currentFermentationProfile = profileName
                
            elif profileName == ConfigConst.FERMENTATION_PROFILE_CONDITIONING:
                self.currentTempMin = ConfigConst.CONDITIONING_TEMP_MIN
                self.currentTempMax = ConfigConst.CONDITIONING_TEMP_MAX
                self.currentHumidityMin = ConfigConst.CONDITIONING_HUMIDITY_MIN
                self.currentHumidityMax = ConfigConst.CONDITIONING_HUMIDITY_MAX
                self.currentFermentationProfile = profileName
                
            elif profileName == ConfigConst.FERMENTATION_PROFILE_COLD_CRASH:
                self.currentTempMin = ConfigConst.COLD_CRASH_TEMP_MIN
                self.currentTempMax = ConfigConst.COLD_CRASH_TEMP_MAX
                self.currentHumidityMin = ConfigConst.COLD_CRASH_HUMIDITY_MIN
                self.currentHumidityMax = ConfigConst.COLD_CRASH_HUMIDITY_MAX
                self.currentFermentationProfile = profileName
                
            else:
                logging.warning(f"Unknown fermentation profile: {profileName}")
                return False
            
            logging.info(f"Profile changed to {profileName}: Temp [{self.currentTempMin}-{self.currentTempMax}], Humidity [{self.currentHumidityMin}-{self.currentHumidityMax}]")
            
            # Update LED to show profile change
            self._updateLedDisplay(f"Profile: {profileName}")
            
            return True
        
        return False
    
        
    def handleSensorData(self, data: SensorData) -> bool:
        """
        Enhanced sensor data handler with fermentation-specific logic.
        """
        if data:
            logging.info(f"Handling sensor data: {data.getName()}")
            
            # Store temperature readings for spike detection
            if data.getTypeID() == ConfigConst.TEMP_SENSOR_TYPE:
                self._trackTemperatureHistory(data.getValue())
                
                # Check for temperature spike (possible infection indicator)
                if self._detectTemperatureSpike():
                    logging.warning("Temperature spike detected! Possible fermentation issue.")
                    self._triggerAlert("TEMP_SPIKE")
            
            # Existing threshold checking
            if data.getTypeID() == ConfigConst.TEMP_SENSOR_TYPE:
                self._handleTemperatureThreshold(data)
            elif data.getTypeID() == ConfigConst.HUMIDITY_SENSOR_TYPE:
                self._handleHumidityThreshold(data)
            elif data.getTypeID() == ConfigConst.PRESSURE_SENSOR_TYPE:
                self._handlePressureData(data)
            
            return True
        
        return False
    
    def _trackTemperatureHistory(self, temp: float):
        """
        Track recent temperature readings for spike detection.
        """
        self.recentTemperatures.append({
            'value': temp,
            'timestamp': time.time()
        })
        
        # Keep only last N readings
        if len(self.recentTemperatures) > self.maxTempHistorySize:
            self.recentTemperatures.pop(0)
    
    def _detectTemperatureSpike(self) -> bool:
        """
        Detect rapid temperature increase (indicator of infection or equipment failure).
        Returns True if spike detected.
        """
        if len(self.recentTemperatures) < 2:
            return False
        
        # Check last 30 minutes (15 readings at 2-min intervals)
        oldest = self.recentTemperatures[0]
        newest = self.recentTemperatures[-1]
        
        timeDelta = newest['timestamp'] - oldest['timestamp']
        tempDelta = newest['value'] - oldest['value']
        
        # If temp increased by more than threshold in ~30 mins
        if timeDelta >= 1800 and tempDelta >= ConfigConst.TEMP_SPIKE_THRESHOLD:
            return True
        
        return False
    
    def _handleTemperatureThreshold(self, data: SensorData):
        """
        Handle temperature threshold crossings with fermentation profile awareness.
        """
        temp = data.getValue()
        
        # Critical thresholds (profile-independent)
        if temp >= ConfigConst.TEMP_CRITICAL_HIGH:
            logging.critical(f"CRITICAL: Temperature {temp}F exceeds safe maximum!")
            self._triggerCriticalCooling()
            self._updateLedDisplay(f"CRITICAL HIGH: {temp}F!", ConfigConst.LED_ALERT_CMD)
            return
        
        if temp <= ConfigConst.TEMP_CRITICAL_LOW:
            logging.critical(f"CRITICAL: Temperature {temp}F below freezing!")
            self._triggerEmergencyHeating()
            self._updateLedDisplay(f"CRITICAL LOW: {temp}F!", ConfigConst.LED_ALERT_CMD)
            return
        
        # Profile-specific thresholds
        if temp > self.currentTempMax:
            logging.warning(f"Temperature {temp}F above target max {self.currentTempMax}F")
            self._activateCooling()
            self._updateLedDisplay(f"Cooling: {temp}F", ConfigConst.LED_ACTIVE_CMD)
            
        elif temp < self.currentTempMin:
            logging.warning(f"Temperature {temp}F below target min {self.currentTempMin}F")
            self._activateHeating()
            self._updateLedDisplay(f"Heating: {temp}F", ConfigConst.LED_ACTIVE_CMD)
            
        else:
            # Temperature within range
            self._deactivateHvac()
            self._updateLedDisplay(f"Optimal: {temp}F", ConfigConst.LED_OPTIMAL_CMD)
    
    def _handleHumidityThreshold(self, data: SensorData):
        """
        Handle humidity threshold crossings with fermentation profile awareness.
        """
        humidity = data.getValue()
        
        # Critical thresholds
        if humidity <= ConfigConst.HUMIDITY_CRITICAL_LOW:
            logging.critical(f"CRITICAL: Humidity {humidity}% dangerously low!")
            self._triggerMaxHumidification()
            return
        
        if humidity >= ConfigConst.HUMIDITY_CRITICAL_HIGH:
            logging.warning(f"WARNING: Humidity {humidity}% very high!")
            self._deactivateHumidifier()
            return
        
        # Profile-specific thresholds
        if humidity < self.currentHumidityMin:
            logging.info(f"Humidity {humidity}% below target min {self.currentHumidityMin}%")
            self._activateHumidifier()
            
        elif humidity > self.currentHumidityMax:
            logging.info(f"Humidity {humidity}% above target max {self.currentHumidityMax}%")
            self._deactivateHumidifier()
            
        else:
            # Humidity within range - could deactivate if currently on
            pass
    
    def _handlePressureData(self, data: SensorData):
        """
        Handle pressure data - useful for fermentation activity detection.
        In a real system, rising pressure indicates CO2 production (active fermentation).
        """
        pressure = data.getValue()
        logging.info(f"Pressure reading: {pressure} kPa")
        
        # Could implement fermentation activity detection here
        # For now, just log the data
        
    def _activateCooling(self):
        """
        Activate HVAC in cooling mode.
        """
        actuatorData = ActuatorData()
        actuatorData.setTypeID(ConfigConst.HVAC_ACTUATOR_TYPE)
        actuatorData.setCommand(ConfigConst.HVAC_COOLING_CMD)
        actuatorData.setValue(1.0)  # Full power
        
        self.actuatorAdapterManager.sendActuatorCommand(actuatorData)
        logging.info("HVAC cooling activated")

    def _activateHeating(self):
        """
        Activate HVAC in heating mode.
        """
        actuatorData = ActuatorData()
        actuatorData.setTypeID(ConfigConst.HVAC_ACTUATOR_TYPE)
        actuatorData.setCommand(ConfigConst.HVAC_HEATING_CMD)
        actuatorData.setValue(1.0)
        
        self.actuatorAdapterManager.sendActuatorCommand(actuatorData)
        logging.info("HVAC heating activated")

    def _deactivateHvac(self):
        """
        Turn off HVAC system.
        """
        actuatorData = ActuatorData()
        actuatorData.setTypeID(ConfigConst.HVAC_ACTUATOR_TYPE)
        actuatorData.setCommand(ConfigConst.HVAC_OFF_CMD)
        actuatorData.setValue(0.0)
        
        self.actuatorAdapterManager.sendActuatorCommand(actuatorData)

    def _activateHumidifier(self):
        """
        Activate humidifier.
        """
        actuatorData = ActuatorData()
        actuatorData.setTypeID(ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
        actuatorData.setCommand(ConfigConst.HUMIDIFIER_ON_CMD)
        actuatorData.setValue(1.0)
        
        self.actuatorAdapterManager.sendActuatorCommand(actuatorData)
        logging.info("Humidifier activated")

    def _deactivateHumidifier(self):
        """
        Deactivate humidifier.
        """
        actuatorData = ActuatorData()
        actuatorData.setTypeID(ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
        actuatorData.setCommand(ConfigConst.HUMIDIFIER_OFF_CMD)
        actuatorData.setValue(0.0)
        
        self.actuatorAdapterManager.sendActuatorCommand(actuatorData)

    def _triggerCriticalCooling(self):
        """
        Emergency cooling - maximum power.
        """
        actuatorData = ActuatorData()
        actuatorData.setTypeID(ConfigConst.HVAC_ACTUATOR_TYPE)
        actuatorData.setCommand(ConfigConst.HVAC_COOLING_CMD)
        actuatorData.setValue(2.0)  # Max power indicator
        
        self.actuatorAdapterManager.sendActuatorCommand(actuatorData)
        logging.critical("EMERGENCY COOLING ACTIVATED")

    def _triggerEmergencyHeating(self):
        """
        Emergency heating - maximum power.
        """
        actuatorData = ActuatorData()
        actuatorData.setTypeID(ConfigConst.HVAC_ACTUATOR_TYPE)
        actuatorData.setCommand(ConfigConst.HVAC_HEATING_CMD)
        actuatorData.setValue(2.0)
        
        self.actuatorAdapterManager.sendActuatorCommand(actuatorData)
        logging.critical("EMERGENCY HEATING ACTIVATED")

    def _triggerMaxHumidification(self):
        """
        Maximum humidification.
        """
        actuatorData = ActuatorData()
        actuatorData.setTypeID(ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
        actuatorData.setCommand(ConfigConst.HUMIDIFIER_ON_CMD)
        actuatorData.setValue(2.0)
        
        self.actuatorAdapterManager.sendActuatorCommand(actuatorData)
        logging.critical("MAXIMUM HUMIDIFICATION ACTIVATED")

    def _updateLedDisplay(self, message: str, state: str = None):
        """
        Update LED display with message and optional state.
        """
        if state and state != self.currentLedState:
            self.currentLedState = state
        
        actuatorData = ActuatorData()
        actuatorData.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        actuatorData.setCommand(self.currentLedState)
        actuatorData.setStateData(message)
        
        self.actuatorAdapterManager.sendActuatorCommand(actuatorData)

    def _triggerAlert(self, alertType: str):
        """
        Trigger system alert.
        """
        self._updateLedDisplay(f"ALERT: {alertType}", ConfigConst.LED_ALERT_CMD)