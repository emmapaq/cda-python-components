import json
import logging
from decimal import Decimal
from json import JSONEncoder

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DataUtil:
    def __init__(self, encodeToUtf8: bool = False):
        self.encodeToUtf8 = encodeToUtf8
        logging.info("Created DataUtil instance.")

    # ----------------------
    # ActuatorData Conversions
    # ----------------------
    def actuatorDataToJson(self, data: ActuatorData = None, useDecForFloat: bool = False) -> str:
        if not data:
            logging.debug("ActuatorData is null. Returning empty string.")
            return ""
        return self._generateJsonData(obj=data, useDecForFloat=useDecForFloat)

    def jsonToActuatorData(self, jsonData: str = None, useDecForFloat: bool = False) -> ActuatorData | None:
        if not jsonData:
            logging.warning("JSON data is empty or null. Returning None.")
            return None
        jsonStruct = self._formatDataAndLoadDictionary(jsonData, useDecForFloat)
        ad = ActuatorData()
        self._updateIotData(jsonStruct, ad)
        return ad

    # ----------------------
    # SensorData Conversions
    # ----------------------
    def sensorDataToJson(self, data: SensorData = None, useDecForFloat: bool = False) -> str:
        if not data:
            logging.debug("SensorData is null. Returning empty string.")
            return ""
        return self._generateJsonData(obj=data, useDecForFloat=useDecForFloat)

    def jsonToSensorData(self, jsonData: str = None, useDecForFloat: bool = False) -> SensorData | None:
        if not jsonData:
            logging.warning("JSON data is empty or null. Returning None.")
            return None
        jsonStruct = self._formatDataAndLoadDictionary(jsonData, useDecForFloat)
        sd = SensorData()
        self._updateIotData(jsonStruct, sd)
        return sd

    # ----------------------
    # SystemPerformanceData Conversions
    # ----------------------
    def systemPerformanceDataToJson(self, data: SystemPerformanceData = None, useDecForFloat: bool = False) -> str:
        if not data:
            logging.debug("SystemPerformanceData is null. Returning empty string.")
            return ""
        return self._generateJsonData(obj=data, useDecForFloat=useDecForFloat)

    def jsonToSystemPerformanceData(self, jsonData: str = None, useDecForFloat: bool = False) -> SystemPerformanceData | None:
        if not jsonData:
            logging.warning("JSON data is empty or null. Returning None.")
            return None
        jsonStruct = self._formatDataAndLoadDictionary(jsonData, useDecForFloat)
        spd = SystemPerformanceData()
        self._updateIotData(jsonStruct, spd)
        return spd

    # ----------------------
    # Private helper methods
    # ----------------------
    def _formatDataAndLoadDictionary(self, jsonData: str, useDecForFloat: bool = False) -> dict:
        """
        Prepare JSON string and load into a dictionary.
        """
        jsonData = jsonData.replace("'", '"').replace('False', 'false').replace('True', 'true')
        if useDecForFloat:
            return json.loads(jsonData, parse_float=Decimal)
        return json.loads(jsonData)

    def _generateJsonData(self, obj, useDecForFloat: bool = False) -> str:
        """
        Convert an object to a JSON string using JsonDataEncoder.
        """
        if self.encodeToUtf8:
            jsonData = json.dumps(obj, cls=JsonDataEncoder).encode('utf8')
        else:
            jsonData = json.dumps(obj, cls=JsonDataEncoder, indent=4)

        if jsonData:
            jsonData = jsonData.replace("'", '"').replace('False', 'false').replace('True', 'true')
        return jsonData

    def _updateIotData(self, jsonStruct: dict, obj):
        """
        Map dictionary values into the object's attributes.
        """
        varStruct = vars(obj)
        for key in jsonStruct:
            if key in varStruct:
                setattr(obj, key, jsonStruct[key])
            else:
                logging.warning("JSON data contains key not mappable to object: %s", key)


class JsonDataEncoder(JSONEncoder):
    """
    Convenience class to facilitate JSON encoding of an object that
    can be converted to a dict.
    """
    def default(self, o):
        return o.__dict__
