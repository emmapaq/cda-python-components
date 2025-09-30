import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

class PressureSensorSimTask(BaseSensorSimTask):
    """
    Simulates a pressure sensor by generating telemetry data
    within normal environmental pressure ranges.
    """
    def __init__(self, dataSet = None):
        super(PressureSensorSimTask, self).__init__(
            name   = ConfigConst.PRESSURE_SENSOR_NAME,
            typeID = ConfigConst.PRESSURE_SENSOR_TYPE,
            dataSet = dataSet,
            minVal = SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE,
            maxVal = SensorDataGenerator.HI_NORMAL_ENV_PRESSURE
        )
