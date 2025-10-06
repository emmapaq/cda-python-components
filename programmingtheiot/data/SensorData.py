import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.BaseIotData import BaseIotData

class SensorData(BaseIotData):
    """
    Concrete implementation of SensorData for storing sensor telemetry.
    """

    # Sensor type constants
    TEMPERATURE_SENSOR_TYPE = 1
    HUMIDITY_SENSOR_TYPE = 2
    PRESSURE_SENSOR_TYPE = 3

    def __init__(self, typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, name = ConfigConst.NOT_SET, d = None):
        super(SensorData, self).__init__(name = name, typeID = typeID, d = d)
        self.sensorType = typeID  # ✅ Fix: store the sensor type
        self.value = 0.0          # ✅ Initialize sensor value

    def getSensorType(self) -> int:
        """
        Returns the sensor type to the caller.
        """
        return self.sensorType

    def getValue(self) -> float:
        """
        Returns the current sensor value.
        """
        return self.value

    def setValue(self, newVal: float):
        """
        Sets the current sensor value.
        """
        self.value = newVal
        self._handleUpdateData(newVal)

    def _handleUpdateData(self, data):
        """
        Optional hook for processing or logging updates.
        """
        # You can extend this to update timestamps, log changes, etc.
        pass
