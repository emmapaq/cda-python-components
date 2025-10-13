import json
import logging

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DataUtil:
    """
    Utility class for serializing and deserializing IoT data objects to/from JSON.
    """

    def __init__(self, encodeToUtf8: bool = False):
        self.encodeToUtf8 = encodeToUtf8
        self.logger = logging.getLogger("DataUtil")

    # ---- ActuatorData conversions ----
    def actuatorDataToJson(self, actuatorData: ActuatorData) -> str:
        if actuatorData is None:
            return None
        try:
            jsonData = json.dumps(actuatorData.__dict__)
            return jsonData.encode("utf-8") if self.encodeToUtf8 else jsonData
        except Exception as e:
            self.logger.error("Failed to convert ActuatorData to JSON: %s", e)
            return None

    def jsonToActuatorData(self, jsonData: str) -> ActuatorData:
        if not jsonData:
            return None
        try:
            if self.encodeToUtf8 and isinstance(jsonData, bytes):
                jsonData = jsonData.decode("utf-8")

            dataDict = json.loads(jsonData)
            ad = ActuatorData()
            ad.__dict__.update(dataDict)
            return ad
        except Exception as e:
            self.logger.error("Failed to convert JSON to ActuatorData: %s", e)
            return None

    # ---- SensorData conversions ----
    def sensorDataToJson(self, sensorData: SensorData) -> str:
        if sensorData is None:
            return None
        try:
            jsonData = json.dumps(sensorData.__dict__)
            return jsonData.encode("utf-8") if self.encodeToUtf8 else jsonData
        except Exception as e:
            self.logger.error("Failed to convert SensorData to JSON: %s", e)
            return None

    def jsonToSensorData(self, jsonData: str) -> SensorData:
        if not jsonData:
            return None
        try:
            if self.encodeToUtf8 and isinstance(jsonData, bytes):
                jsonData = jsonData.decode("utf-8")

            dataDict = json.loads(jsonData)
            sd = SensorData()
            sd.__dict__.update(dataDict)
            return sd
        except Exception as e:
            self.logger.error("Failed to convert JSON to SensorData: %s", e)
            return None

    # ---- SystemPerformanceData conversions ----
    def systemPerformanceDataToJson(self, sysPerfData: SystemPerformanceData) -> str:
        if sysPerfData is None:
            return None
        try:
            jsonData = json.dumps(sysPerfData.__dict__)
            return jsonData.encode("utf-8") if self.encodeToUtf8 else jsonData
        except Exception as e:
            self.logger.error("Failed to convert SystemPerformanceData to JSON: %s", e)
            return None

    def jsonToSystemPerformanceData(self, jsonData: str) -> SystemPerformanceData:
        if not jsonData:
            return None
        try:
            if self.encodeToUtf8 and isinstance(jsonData, bytes):
                jsonData = jsonData.decode("utf-8")

            dataDict = json.loads(jsonData)
            spd = SystemPerformanceData()
            spd.__dict__.update(dataDict)
            return spd
        except Exception as e:
            self.logger.error("Failed to convert JSON to SystemPerformanceData: %s", e)
            return None
