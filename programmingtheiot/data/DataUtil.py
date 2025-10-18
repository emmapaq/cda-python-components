"""
Data Utility Module

This module provides JSON serialization and deserialization utilities
for IoT data objects including ActuatorData, SensorData, and SystemPerformanceData.

License: PIOT-DOC-LIC
@author: Your Name
"""

import json
import logging

from decimal import Decimal
from json import JSONEncoder

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData


class DataUtil():
    """
    Utility class for converting IoT data objects to/from JSON format.
    """
    
    def __init__(self, encodeToUtf8=False):
        """
        Constructor for DataUtil.
        
        @param encodeToUtf8 If True, encode JSON strings to UTF-8 bytes
        """
        self.encodeToUtf8 = encodeToUtf8
        
        logging.info("Created DataUtil instance.")
    
    def actuatorDataToJson(self, data: ActuatorData = None, useDecForFloat: bool = False):
        """
        Converts ActuatorData to JSON string.
        
        @param data The ActuatorData instance to convert
        @param useDecForFloat If True, use Decimal for float values
        @return JSON string representation, or empty string if data is None
        """
        if not data:
            logging.debug("ActuatorData is null. Returning empty string.")
            return ""
        
        logging.debug("Encoding ActuatorData to JSON [pre]  --> %s", str(data))
        
        jsonData = self._generateJsonData(obj=data, useDecForFloat=useDecForFloat)
        
        logging.info("Encoding ActuatorData to JSON [post] --> %s", jsonData)
        
        return jsonData
    
    def sensorDataToJson(self, data: SensorData = None, useDecForFloat: bool = False):
        """
        Converts SensorData to JSON string.
        
        @param data The SensorData instance to convert
        @param useDecForFloat If True, use Decimal for float values
        @return JSON string representation, or empty string if data is None
        """
        if not data:
            logging.debug("SensorData is null. Returning empty string.")
            return ""
        
        logging.debug("Encoding SensorData to JSON [pre]  --> %s", str(data))
        
        jsonData = self._generateJsonData(obj=data, useDecForFloat=useDecForFloat)
        
        logging.info("Encoding SensorData to JSON [post] --> %s", jsonData)
        
        return jsonData
    
    def systemPerformanceDataToJson(self, data: SystemPerformanceData = None, useDecForFloat: bool = False):
        """
        Converts SystemPerformanceData to JSON string.
        
        @param data The SystemPerformanceData instance to convert
        @param useDecForFloat If True, use Decimal for float values
        @return JSON string representation, or empty string if data is None
        """
        if not data:
            logging.debug("SystemPerformanceData is null. Returning empty string.")
            return ""
        
        logging.debug("Encoding SystemPerformanceData to JSON [pre]  --> %s", str(data))
        
        jsonData = self._generateJsonData(obj=data, useDecForFloat=useDecForFloat)
        
        logging.info("Encoding SystemPerformanceData to JSON [post] --> %s", jsonData)
        
        return jsonData
    
    def jsonToActuatorData(self, jsonData: str = None, useDecForFloat: bool = False):
        """
        Converts JSON string to ActuatorData instance.
        
        @param jsonData The JSON string to convert
        @param useDecForFloat If True, parse floats as Decimal
        @return ActuatorData instance, or None if jsonData is None/empty
        """
        if not jsonData:
            logging.warning("JSON data is empty or null. Returning null.")
            return None
        
        logging.debug("Converting JSON to ActuatorData [pre]  --> %s", jsonData)
        
        jsonStruct = self._formatDataAndLoadDictionary(jsonData, useDecForFloat=useDecForFloat)
        
        ad = ActuatorData()
        self._updateIotData(jsonStruct, ad)
        
        logging.debug("Converted JSON to ActuatorData [post] --> %s", str(ad))
        
        return ad
    
    def jsonToSensorData(self, jsonData: str = None, useDecForFloat: bool = False):
        """
        Converts JSON string to SensorData instance.
        
        @param jsonData The JSON string to convert
        @param useDecForFloat If True, parse floats as Decimal
        @return SensorData instance, or None if jsonData is None/empty
        """
        if not jsonData:
            logging.warning("JSON data is empty or null. Returning null.")
            return None
        
        logging.debug("Converting JSON to SensorData [pre]  --> %s", jsonData)
        
        jsonStruct = self._formatDataAndLoadDictionary(jsonData, useDecForFloat=useDecForFloat)
        
        sd = SensorData()
        self._updateIotData(jsonStruct, sd)
        
        logging.debug("Converted JSON to SensorData [post] --> %s", str(sd))
        
        return sd
    
    def jsonToSystemPerformanceData(self, jsonData: str = None, useDecForFloat: bool = False):
        """
        Converts JSON string to SystemPerformanceData instance.
        
        @param jsonData The JSON string to convert
        @param useDecForFloat If True, parse floats as Decimal
        @return SystemPerformanceData instance, or None if jsonData is None/empty
        """
        if not jsonData:
            logging.warning("JSON data is empty or null. Returning null.")
            return None
        
        logging.debug("Converting JSON to SystemPerformanceData [pre]  --> %s", jsonData)
        
        jsonStruct = self._formatDataAndLoadDictionary(jsonData, useDecForFloat=useDecForFloat)
        
        spd = SystemPerformanceData()
        self._updateIotData(jsonStruct, spd)
        
        logging.debug("Converted JSON to SystemPerformanceData [post] --> %s", str(spd))
        
        return spd
    
    def _formatDataAndLoadDictionary(self, jsonData: str, useDecForFloat: bool = False) -> dict:
        """
        Formats JSON string and loads it into a dictionary.
        
        @param jsonData The JSON string to format and parse
        @param useDecForFloat If True, parse floats as Decimal
        @return Dictionary containing the parsed JSON data
        """
        # Replace single quotes with double quotes and Python booleans with JSON booleans
        jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
        
        jsonStruct = None
        
        if useDecForFloat:
            jsonStruct = json.loads(jsonData, parse_float=Decimal)
        else:
            jsonStruct = json.loads(jsonData)
        
        return jsonStruct
    
    def _generateJsonData(self, obj, useDecForFloat: bool = False) -> str:
        """
        Generates JSON string from an object.
        
        @param obj The object to convert to JSON
        @param useDecForFloat If True, use Decimal for float values (currently not implemented)
        @return JSON string representation
        """
        jsonData = None
        
        if self.encodeToUtf8:
            jsonData = json.dumps(obj, cls=JsonDataEncoder).encode('utf8')
        else:
            jsonData = json.dumps(obj, cls=JsonDataEncoder, indent=4)
        
        if jsonData:
            jsonData = jsonData.replace("\'", "\"").replace('False', 'false').replace('True', 'true')
        
        return jsonData
    
    def _updateIotData(self, jsonStruct, obj):
        """
        Updates an IoT data object from a JSON dictionary structure.
        
        @param jsonStruct The dictionary containing JSON data
        @param obj The IoT data object to update
        """
        varStruct = vars(obj)
        
        for key in jsonStruct:
            if key in varStruct:
                setattr(obj, key, jsonStruct[key])
                logging.debug("JSON data contains key mappable to object: %s", key)
            else:
                logging.warning("JSON data contains key not mappable to object: %s", key)


class JsonDataEncoder(JSONEncoder):
    """
    Convenience class to facilitate JSON encoding of an object that
    can be converted to a dict.
    """
    
    def default(self, o):
        """
        Converts an object to a dictionary for JSON serialization.
        
        @param o The object to convert
        @return Dictionary representation of the object
        """
        return o.__dict__