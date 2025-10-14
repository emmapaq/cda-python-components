"""
Sensor Data Module

Represents sensor data including temperature, humidity, pressure, etc.
"""

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.BaseIotData import BaseIotData


class SensorData(BaseIotData):
    """
    Encapsulates sensor data values and metadata.
    
    This class represents data from various sensor types including
    temperature, humidity, pressure, and other environmental sensors.
    """
    
    # Sensor type constants
    DEFAULT_SENSOR_TYPE = ConfigConst.DEFAULT_TYPE_ID
    TEMP_SENSOR_TYPE = ConfigConst.TEMP_SENSOR_TYPE
    HUMIDITY_SENSOR_TYPE = ConfigConst.HUMIDITY_SENSOR_TYPE
    PRESSURE_SENSOR_TYPE = ConfigConst.PRESSURE_SENSOR_TYPE
    
    def __init__(self, typeID: int = DEFAULT_SENSOR_TYPE, name: str = ConfigConst.NOT_SET):
        """
        Constructor for SensorData.
        
        Args:
            typeID: The sensor type ID (default: DEFAULT_SENSOR_TYPE)
            name: The sensor name (default: "Not Set")
        """
        super(SensorData, self).__init__(name=name, typeID=typeID)
        
        self.value = ConfigConst.DEFAULT_VAL
    
    def getValue(self) -> float:
        """
        Gets the sensor value.
        
        Returns:
            float: The sensor value
        """
        return self.value
    
    def setValue(self, val: float):
        """
        Sets the sensor value.
        
        Args:
            val: The value to set
        """
        self.value = val
        self.updateTimeStamp()
    
    def __str__(self) -> str:
        """
        Returns a string representation of the SensorData.
        
        Returns:
            str: String representation
        """
        return f"SensorData(name={self.name}, typeID={self.typeID}, value={self.value}, timestamp={self.timeStamp})"
    
    def _handleUpdateData(self, data):
        """
        Internal method to update data from another SensorData instance.
        
        Args:
            data: Another SensorData instance to copy from
        """
        if data and isinstance(data, SensorData):
            self.value = data.getValue()