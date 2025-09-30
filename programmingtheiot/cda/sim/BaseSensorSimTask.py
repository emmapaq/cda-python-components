import random

from programmingtheiot.common import ConfigConst
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataSet


class BaseSensorSimTask():
    """
    Base class for simulated sensor tasks.
    Supports either random value generation or pre-defined data sets.
    """

    DEFAULT_MIN_VAL = ConfigConst.DEFAULT_VAL
    DEFAULT_MAX_VAL = 100.0

    def __init__(self, 
                 name: str = ConfigConst.NOT_SET, 
                 typeID: int = ConfigConst.DEFAULT_SENSOR_TYPE, 
                 dataSet: SensorDataSet = None, 
                 minVal: float = DEFAULT_MIN_VAL, 
                 maxVal: float = DEFAULT_MAX_VAL):
        
        self.dataSet = dataSet
        self.name = name
        self.typeID = typeID
        self.dataSetIndex = 0
        self.latestSensorData = None
        self.useRandomizer = False

        if not self.dataSet:
            self.useRandomizer = True
            self.minVal = minVal
            self.maxVal = maxVal

    def getName(self) -> str:
        return self.name

    def getTypeID(self) -> int:
        return self.typeID

    def generateTelemetry(self) -> SensorData:
        """
        Generate a SensorData object, either using random values or a fixed dataset.
        """
        sensorData = SensorData(typeID=self.getTypeID(), name=self.getName())
        sensorVal = ConfigConst.DEFAULT_VAL

        if self.useRandomizer:
            sensorVal = random.uniform(self.minVal, self.maxVal)
        else:
            sensorVal = self.dataSet.getDataEntry(index=self.dataSetIndex)
            self.dataSetIndex += 1

            if self.dataSetIndex >= self.dataSet.getDataEntryCount() - 1:
                self.dataSetIndex = 0

        sensorData.setValue(sensorVal)
        self.latestSensorData = sensorData

        return self.latestSensorData

    def getTelemetryValue(self) -> float:
        """
        Return the latest sensor value (generates a new one if none exists yet).
        """
        if not self.latestSensorData:
            self.generateTelemetry()

        return self.latestSensorData.getValue()
