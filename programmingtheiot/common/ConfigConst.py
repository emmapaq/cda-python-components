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
DEFAULT_TIMEOUT = 5
DEFAULT_POLLING_CYCLES = 5
DEFAULT_POLL_CYCLES = 60
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
CDA_SENSOR_DATA_MSG_RESOURCE = "PIOT/ConstrainedDevice/SensorMsg"
CDA_ACTUATOR_CMD_MSG_RESOURCE = "PIOT/ConstrainedDevice/ActuatorCmd"
CDA_ACTUATOR_RESPONSE_MSG_RESOURCE = "PIOT/ConstrainedDevice/ActuatorResponse"
CDA_MGMT_STATUS_MSG_RESOURCE = "PIOT/ConstrainedDevice/MgmtStatusMsg"
CDA_MGMT_CMD_MSG_RESOURCE = "PIOT/ConstrainedDevice/MgmtCmd"
CDA_SYSTEM_PERF_MSG_RESOURCE = "PIOT/ConstrainedDevice/SystemPerfMsg"
CDA_UPDATE_NOTIFICATIONS_MSG_RESOURCE = "PIOT/ConstrainedDevice/UpdateMsg"
CDA_SENSOR_MSG_RESOURCE = "PIOT/ConstrainedDevice/SensorMsg"  # Alias for tests

#####
# Resource Handler Names
#####
SYSTEM_PERF_MSG = "SystemPerfMsg"
SYSTEM_PERF_NAME = "SystemPerfMsg"  # Alias for tests
SENSOR_MSG = "SensorMsg"
ACTUATOR_CMD = "ActuatorCmd"
ACTUATOR_RESPONSE = "ActuatorResponse"

# Additional aliases for tests
SYSTEM_PERF_NAME = "SystemPerfMsg"
CDA_MGMT_STATUS_MSG_RESOURCE = "PIOT/ConstrainedDevice/MgmtStatusMsg"

#####
# Actuator Names
#####
HUMIDIFIER_ACTUATOR_NAME = "HumidifierActuator"
HVAC_ACTUATOR_NAME = "HvacActuator"
LED_ACTUATOR_NAME = "LedActuator"

#####
# Sensor Names
#####
TEMP_SENSOR_NAME = "TempSensor"
HUMIDITY_SENSOR_NAME = "HumiditySensor"
PRESSURE_SENSOR_NAME = "PressureSensor"

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
CRED_SECTION = "Credentials"

#####
# Configuration Keys - CDA
#####
ENABLE_MQTT_CLIENT_KEY = "enableMqttClient"
ENABLE_COAP_CLIENT_KEY = "enableCoapClient"
ENABLE_COAP_SERVER_KEY = "enableCoapServer"
ENABLE_CLOUD_CLIENT_KEY = "enableCloudClient"
ENABLE_SYSTEM_PERF_KEY = "enableSystemPerformanceManager"
ENABLE_SENSOR_MANAGER_KEY = "enableSensorManager"
ENABLE_ACTUATOR_MANAGER_KEY = "enableActuatorManager"
POLLING_CYCLES_KEY = "pollCycleSecs"
POLL_CYCLES_KEY = "pollCycleSecs"  # Alias
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
ENABLE_CRYPT_KEY = "enableEncryption"
TLS_VERSION_KEY = "tlsVersion"
CERT_FILE_KEY = "pemFileName"
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
# Sensor and Actuator Type Defaults
#####
DEFAULT_SENSOR_TYPE = 0
DEFAULT_ACTUATOR_TYPE = 0
SYSTEM_PERF_TYPE = 9000

#####
# Sensor Types
#####
TEMP_SENSOR_TYPE = 1
HUMIDITY_SENSOR_TYPE = 3
PRESSURE_SENSOR_TYPE = 2

#####
# Actuator Types
#####
HVAC_ACTUATOR_TYPE = 1
HUMIDIFIER_ACTUATOR_TYPE = 2
LED_DISPLAY_ACTUATOR_TYPE = 100
LED_ACTUATOR_TYPE = 3

#####
# Actuator Commands
#####
DEFAULT_COMMAND = 0
COMMAND_OFF = 0
COMMAND_ON = 1
COMMAND_UPDATE = 2
COMMAND_SET_VALUE = 3
COMMAND_GET_VALUE = 4

#####
# Actuator State
#####
STATE_OFF = 0
STATE_ON = 1

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
# Sensor Names
#####
TEMP_SENSOR_NAME = "TempSensor"
HUMIDITY_SENSOR_NAME = "HumiditySensor"
PRESSURE_SENSOR_NAME = "PressureSensor"

SYSTEM_PERF_TYPE = "SystemPerformance"

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

####
# LAB MODULE 12 - PROJECT CONFIG
####
# Fermentation Profile Types
FERMENTATION_PROFILE_ALE = "ALE"
FERMENTATION_PROFILE_LAGER = "LAGER"
FERMENTATION_PROFILE_CONDITIONING = "CONDITIONING"
FERMENTATION_PROFILE_COLD_CRASH = "COLD_CRASH"

# Ale Profile Thresholds
ALE_TEMP_MIN = 68.0
ALE_TEMP_MAX = 72.0
ALE_TEMP_NOMINAL = 70.0
ALE_HUMIDITY_MIN = 60.0
ALE_HUMIDITY_MAX = 70.0
ALE_HUMIDITY_NOMINAL = 65.0

# Lager Profile Thresholds
LAGER_TEMP_MIN = 50.0
LAGER_TEMP_MAX = 55.0
LAGER_TEMP_NOMINAL = 52.0
LAGER_HUMIDITY_MIN = 55.0
LAGER_HUMIDITY_MAX = 65.0
LAGER_HUMIDITY_NOMINAL = 60.0

# Conditioning Profile Thresholds
CONDITIONING_TEMP_MIN = 55.0
CONDITIONING_TEMP_MAX = 65.0
CONDITIONING_TEMP_NOMINAL = 60.0
CONDITIONING_HUMIDITY_MIN = 50.0
CONDITIONING_HUMIDITY_MAX = 60.0
CONDITIONING_HUMIDITY_NOMINAL = 55.0

# Cold Crash Profile Thresholds
COLD_CRASH_TEMP_MIN = 35.0
COLD_CRASH_TEMP_MAX = 40.0
COLD_CRASH_TEMP_NOMINAL = 38.0
COLD_CRASH_HUMIDITY_MIN = 50.0
COLD_CRASH_HUMIDITY_MAX = 60.0
COLD_CRASH_HUMIDITY_NOMINAL = 55.0

# Alert Thresholds
TEMP_SPIKE_THRESHOLD = 5.0  # degrees F in 30 minutes
TEMP_CRITICAL_HIGH = 80.0   # dangerous for any fermentation
TEMP_CRITICAL_LOW = 32.0    # freezing point
HUMIDITY_CRITICAL_LOW = 30.0
HUMIDITY_CRITICAL_HIGH = 85.0

# Actuation Response Times
ACTUATION_RESPONSE_TIME_SECS = 30  # max time to respond to threshold crossing

# Command values for fermentation control
HVAC_COOLING_CMD = "COOLING"
HVAC_HEATING_CMD = "HEATING"
HVAC_OFF_CMD = "OFF"

HUMIDIFIER_ON_CMD = "ON"
HUMIDIFIER_OFF_CMD = "OFF"

LED_OPTIMAL_CMD = "OPTIMAL"      # Green - conditions good
LED_ACTIVE_CMD = "ACTIVE"        # Yellow - fermentation active
LED_ALERT_CMD = "ALERT"          # Red - problem detected
LED_OFF_CMD = "OFF"

# Display messages for LED
LED_MSG_OPTIMAL = "Temp: {temp}F Humid: {humid}% - OPTIMAL"
LED_MSG_FERMENTATION = "Temp: {temp}F - FERMENTING"
LED_MSG_TEMP_HIGH = "ALERT: TEMP HIGH {temp}F!"
LED_MSG_TEMP_LOW = "ALERT: TEMP LOW {temp}F!"
LED_MSG_HUMID_LOW = "ALERT: HUMIDITY LOW {humid}%!"