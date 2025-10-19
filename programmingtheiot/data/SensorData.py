import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.BaseIotData import BaseIotData

class SensorData(BaseIotData):
    def __init__(self, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, name=ConfigConst.NOT_SET, d=None):
        super(SensorData, self).__init__(name=name, typeID=typeID, d=d)
        self._value = None  # Initialize sensor value

    def getSensorType(self) -> int:
        return self.sensorType

    def getValue(self) -> float:
        return self._value

    def setValue(self, newVal: float):
        if newVal is None or not isinstance(newVal, (float, int)):
            raise ValueError("Sensor value must be a float or int.")
        self._value = float(newVal)

    def _handleUpdateData(self, data):
        # Optional: implement if you want to merge or update from another SensorData
        pass

    def __str__(self):
        return f"SensorData(name={self.getName()}, typeID={self.getTypeID()}, value={self.getValue()})"
