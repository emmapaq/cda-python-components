from .BaseIotData import BaseIotData
from programmingtheiot.common import ConfigConst


class SensorData(BaseIotData):
    """
    SensorData represents a simple container for sensor readings (float values).
    Inherits from BaseIotData.
    """

    def __init__(self, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, name=ConfigConst.NOT_SET, d=None):
        super(SensorData, self).__init__(name=name, typeID=typeID, d=d)
        self.value = ConfigConst.DEFAULT_VAL

    def getValue(self) -> float:
        return self.value

    def setValue(self, newVal: float):
        self.value = newVal
        self.updateTimeStamp()

    def _handleUpdateData(self, data):
        if data and isinstance(data, SensorData):
            self.value = data.getValue()

    def __str__(self):
        return f"SensorData [name={self.getName()}, typeID={self.getTypeID()}, value={self.value}, timeStamp={self.timeStamp}]"
