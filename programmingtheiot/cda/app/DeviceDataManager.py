import logging

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector

from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData


class DeviceDataManager(IDataMessageListener):
    def __init__(self):
        self.configUtil = ConfigUtil()

        # Retrieve configuration flags
        self.enableSystemPerf = self.configUtil.getBoolean(
            ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_SYSTEM_PERF_KEY
        )
        self.enableSensing = self.configUtil.getBoolean(
            ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_SENSING_KEY
        )
        self.enableActuation = True

        # Internal state
        self.sysPerfMgr = None
        self.sensorAdapterMgr = None
        self.actuatorAdapterMgr = None
        self.mqttClient = None
        self.coapClient = None
        self.coapServer = None

        # Actuator logic thresholds
        self.handleTempChangeOnDevice = self.configUtil.getBoolean(
            ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HANDLE_TEMP_CHANGE_ON_DEVICE_KEY
        )
        self.triggerHvacTempFloor = self.configUtil.getFloat(
            ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY
        )
        self.triggerHvacTempCeiling = self.configUtil.getFloat(
            ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY
        )

        # Initialize managers
        if self.enableSystemPerf:
            self.sysPerfMgr = SystemPerformanceManager()
            self.sysPerfMgr.setDataMessageListener(self)
            logging.info("Local system performance tracking enabled")

        if self.enableSensing:
            self.sensorAdapterMgr = SensorAdapterManager()
            self.sensorAdapterMgr.setDataMessageListener(self)
            logging.info("Local sensor tracking enabled")

        if self.enableActuation:
            self.actuatorAdapterMgr = ActuatorAdapterManager(dataMsgListener=self)
            logging.info("Local actuation capabilities enabled")

        # Cache for actuator responses
        self.actuatorResponseCache = {}

    # --- Manager lifecycle ---
    def startManager(self):
        logging.info("Starting DeviceDataManager...")
        if self.sysPerfMgr:
            self.sysPerfMgr.startManager()
        if self.sensorAdapterMgr:
            self.sensorAdapterMgr.startManager()
        logging.info("Started DeviceDataManager.")

    def stopManager(self):
        logging.info("Stopping DeviceDataManager...")
        if self.sysPerfMgr:
            self.sysPerfMgr.stopManager()
        if self.sensorAdapterMgr:
            self.sensorAdapterMgr.stopManager()
        logging.info("Stopped DeviceDataManager.")

    # --- IDataMessageListener methods ---
    def handleActuatorCommandMessage(self, data: ActuatorData = None) -> ActuatorData:
        logging.info("Actuator command message received: %s", str(data))
        if data:
            logging.info("Processing actuator command message.")
            return self.actuatorAdapterMgr.sendActuatorCommand(data)
        logging.warning("Incoming actuator command is invalid (null). Ignoring.")
        return None

    def handleActuatorCommandResponse(self, data: ActuatorData = None) -> bool:
        if data:
            logging.debug("Incoming actuator response received: %s", str(data))
            self.actuatorResponseCache[data.getTypeID()] = data
            actuatorMsg = DataUtil().actuatorDataToJson(data)
            resourceName = ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE
            self._handleUpstreamTransmission(resource=resourceName, msg=actuatorMsg)
            return True
        logging.warning("Incoming actuator response is invalid (null). Ignoring.")
        return False

    def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
        logging.info("Incoming message for resource %s: %s", str(resourceEnum), str(msg))
        # Optional: call self._handleIncomingDataAnalysis(msg)
        return True

    def handleSensorMessage(self, data: SensorData = None) -> bool:
        if data:
            logging.debug("Incoming sensor data received: %s", str(data))
            self._handleSensorDataAnalysis(data=data)
            return True
        logging.warning("Incoming sensor data is invalid (null). Ignoring.")
        return False

    def handleSystemPerformanceMessage(self, data: SystemPerformanceData = None) -> bool:
        if data:
            logging.debug("Incoming system performance message received: %s", str(data))
            # Optional: forward upstream
            return True
        logging.warning("Incoming system performance data is invalid (null). Ignoring.")
        return False

    # --- Private helper methods ---
    def _handleSensorDataAnalysis(self, resource=None, data: SensorData = None):
        if self.handleTempChangeOnDevice and data.getTypeID() == ConfigConst.TEMP_SENSOR_TYPE:
            logging.info(
                "Handling temperature change: value=%s, typeID=%s",
                data.getValue(), data.getTypeID()
            )

            ad = ActuatorData(typeID=ConfigConst.HVAC_ACTUATOR_TYPE)
            if data.getValue() > self.triggerHvacTempCeiling:
                ad.setCommand(ConfigConst.COMMAND_ON)
                ad.setValue(self.triggerHvacTempCeiling)
            elif data.getValue() < self.triggerHvacTempFloor:
                ad.setCommand(ConfigConst.COMMAND_ON)
                ad.setValue(self.triggerHvacTempFloor)
            else:
                ad.setCommand(ConfigConst.COMMAND_OFF)

            self.handleActuatorCommandMessage(ad)

    def _handleUpstreamTransmission(self, resource=None, msg: str = None):
        logging.debug("Upstream transmission: resource=%s, msg=%s", str(resource), str(msg))

    def _handleIncomingDataAnalysis(self, msg: str):
        logging.debug("Incoming data analysis: %s", msg)
