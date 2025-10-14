"""
Configuration Constants Module

Contains all configuration keys, default values, and constants
used throughout the Constrained Device Application (CDA).
"""

#####
# General Paths and Defaults
#####

# Base configuration directory (adjust to your environment)
PARENT_PATH = "/home/emmapaq/piot/cda-python-components/config/"

# Default configuration file
DEFAULT_CONFIG_FILE_NAME = "PiotConfig.props"

# Default host
DEFAULT_HOST = "localhost"

# Default ports
DEFAULT_COAP_PORT = 5683
DEFAULT_COAP_SECURE_PORT = 5684
DEFAULT_MQTT_PORT = 1883
DEFAULT_MQTT_SECURE_PORT = 8883

# Default settings
DEFAULT_KEEP_ALIVE = 60
DEFAULT_QOS = 1
DEFAULT_COMMAND_TIMEOUT = 5
DEFAULT_POLLING_CYCLES = 5
DEFAULT_TTL = 300

#####
# Product and Device Names
#####
PRODUCT_NAME = "PIOT"
CLOUD = "Cloud"
GATEWAY = "Gateway"
CONSTRAINED_DEVICE = "Constrained Device"
DEVICE_NAME = "CDA"

#####
# CDA Resource and Message Names
#####
CDA_SENSOR_DATA_MSG_RESOURCE = "CdaSensorDataMsg"
CDA_ACTUATOR_CMD_MSG_RESOURCE = "CdaActuatorCmdMsg"
CDA_ACTUATOR_RESPONSE_MSG_RESOURCE = "CdaActuatorResponseMsg"
CDA_MGMT_STATUS_MSG_RESOURCE = "CdaMgmtStatusMsg"
CDA_MGMT_CMD_MSG_RESOURCE = "CdaMgmtCmdMsg"
CDA_SYSTEM_PERF_MSG_RESOURCE = "CdaSystemPerfMsg"
CDA_UPDATE_NOTIFICATIONS_MSG_RESOURCE = "CdaUpdateNotificationsMsg"
CDA_SENSOR_MSG_RESOURCE = "CdaSensorMsg"  # required by tests

#####
# Configuration Sections
#####
CONSTRAINED_DEVICE_SECTION = "ConstrainedDevice"
COAP_GATEWAY_SERVICE = "Coap.GatewayService"
MQTT_GATEWAY_SERVICE = "Mqtt.GatewayService"
CLOUD_GATEWAY_SERVICE = "Cloud.GatewayService"
SENSOR_SIMULATOR = "SensorSimulator"
ACTUATOR_SIMULATOR = "ActuatorSimulator"
LOGGING = "Logging"
CRED_SECTION = "Credentials"  # required by ConfigUtil.py

#####
# Configuration Keys - CDA
#####
ENABLE_MQTT_CLIENT_KEY = "enableMqttClient"
ENABLE_COAP_CLIENT_KEY = "enableCoapClient"
ENABLE_CLOUD_CLIENT_KEY = "enableCloudClient"
ENABLE_SYSTEM_PERF_KEY = "enableSystemPerformanceManager"
ENABLE_SENSOR_MANAGER_KEY = "enableSensorManager"
ENABLE_ACTUATOR_MANAGER_KEY = "enableActuatorManager"
POLLING_CYCLES_KEY = "pollCycleSecs"
DEVICE_LOCATION_ID_KEY = "deviceLocationID"
LATITUDE_KEY = "latitude"
LONGITUDE_KEY = "longitude"
ELEVATION_KEY = "elevation"

#####
# Configuration Keys - Gateway Services
#####
HOST_KEY = "host"
PORT_KEY = "port"
SECURE_PORT_KEY = "securePort"
CLIENT_ID_KEY = "clientID"
KEEP_ALIVE_KEY = "keepAlive"
DEFAULT_QOS_KEY = "defaultQos"
ENABLE_AUTH_KEY = "enableAuth"
USER_NAME_KEY = "userName"
USER_PASSWORD_KEY = "userPassword"
CRED_FILE_KEY = "credFile"
ENABLE_TLS_KEY = "enableTls"
TLS_VERSION_KEY = "tlsVersion"
CERT_FILE_KEY = "certFile"
KEY_FILE_KEY = "keyFile"
CA_CERT_FILE_KEY = "caFile"

#####
# Configuration Keys - MQTT Topics
#####
ACTUATOR_CMD_TOPIC_KEY = "actuatorCommandTopic"
SENSOR_DATA_TOPIC_KEY = "sensorDataTopic"
SYSTEM_PERF_TOPIC_KEY = "systemPerfTopic"
MGMT_TOPIC_KEY = "managementTopic"

#####
# Configuration Keys - Sensor Simulator
#####
ENABLE_TEMP_SENSOR_KEY = "enableTempSensor"
TEMP_SENSOR_MIN_KEY = "tempSensorMinValue"
TEMP_SENSOR_MAX_KEY = "tempSensorMaxValue"
ENABLE_HUMIDITY_SENSOR_KEY = "enableHumiditySensor"
HUMIDITY_SENSOR_MIN_KEY = "humiditySensorMinValue"
HUMIDITY_SENSOR_MAX_KEY = "humiditySensorMaxValue"
ENABLE_PRESSURE_SENSOR_KEY = "enablePressureSensor"
PRESSURE_SENSOR_MIN_KEY = "pressureSensorMinValue"
PRESSURE_SENSOR_MAX_KEY = "pressureSensorMaxValue"

#####
# Configuration Keys - Actuator Simulator
#####
ENABLE_HVAC_ACTUATOR_KEY = "enableHvacActuator"
ENABLE_HUMIDIFIER_ACTUATOR_KEY = "enableHumidifierActuator"
ENABLE_LED_ACTUATOR_KEY = "enableLedActuator"

#####
# Logging
#####
LOG_LEVEL_KEY = "logLevel"
ENABLE_FILE_LOGGING_KEY = "enableFileLogging"
LOG_FILE_PATH_KEY = "logFilePath"
MAX_LOG_FILE_SIZE_KEY = "maxLogFileSize"
MAX_LOG_FILE_BACKUPS_KEY = "maxLogFileBackups"

#####
# Sensor and Actuator Types
#####
TEMP_SENSOR_TYPE = 1
PRESSURE_SENSOR_TYPE = 2
HUMIDITY_SENSOR_TYPE = 3
HVAC_ACTUATOR_TYPE = 1
HUMIDIFIER_ACTUATOR_TYPE = 2
LED_DISPLAY_ACTUATOR_TYPE = 100

#####
# Actuator Commands
#####
COMMAND_OFF = 0
COMMAND_ON = 1
COMMAND_UPDATE = 2
COMMAND_SET_VALUE = 3
COMMAND_GET_VALUE = 4

#####
# Actuator Status Codes
#####
STATUS_OK = 0
STATUS_ERROR = 1
STATUS_WARNING = 2
STATUS_PROCESSING = 3

#####
# Data Ranges
#####
DEFAULT_TEMP_MIN = 0.0
DEFAULT_TEMP_MAX = 50.0
DEFAULT_HUMIDITY_MIN = 0.0
DEFAULT_HUMIDITY_MAX = 100.0
DEFAULT_PRESSURE_MIN = 80.0
DEFAULT_PRESSURE_MAX = 120.0

#####
# System Performance Thresholds
#####
CPU_UTIL_THRESHOLD = 80.0
MEM_UTIL_THRESHOLD = 85.0
DISK_UTIL_THRESHOLD = 90.0

#####
# Data Formats
#####
JSON_FORMAT = "application/json"
TEXT_FORMAT = "text/plain"
BINARY_FORMAT = "application/octet-stream"

#####
# Protocol Versions
#####
MQTT_VERSION_3_1_1 = 4
MQTT_VERSION_5_0 = 5
COAP_VERSION_1 = 1

#####
# Boolean String Values
#####
TRUE_VALUES = ["true", "True", "TRUE", "1", "yes", "Yes", "YES", "on", "On", "ON"]
FALSE_VALUES = ["false", "False", "FALSE", "0", "no", "No", "NO", "off", "Off", "OFF"]

#####
# Miscellaneous Defaults
#####
NOT_SET = "Not Set"
DEFAULT_VAL = 0.0
DEFAULT_STATE = ""
DEFAULT_TYPE_ID = 0
DEFAULT_LOCATION_ID = "constraineddevice001"
DEFAULT_ENCODING = "utf-8"
DEFAULT_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f%z"
