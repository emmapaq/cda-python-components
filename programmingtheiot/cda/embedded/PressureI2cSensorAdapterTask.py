try:
    import smbus
    HAS_SMBUS = True
except ImportError:
    smbus = None
    HAS_SMBUS = False

import logging
import random

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SimulatedSensorData import SensorDataGenerator

class PressureI2cSensorAdapterTask(BaseSensorSimTask):
    """
    Adapter for LPS25H pressure sensor over I2C.
    Falls back to simulated values if I2C is unavailable.
    """

    def __init__(self):
        super(PressureI2cSensorAdapterTask, self).__init__(
            typeID=SensorData.PRESSURE_SENSOR_TYPE,
            minVal=SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE,
            maxVal=SensorDataGenerator.HI_NORMAL_ENV_PRESSURE
        )

        self.sensorType = SensorData.PRESSURE_SENSOR_TYPE
        self.pressAddr = 0x5C  # LPS25H sensor address
        self.dataMsgListener = None

        if HAS_SMBUS:
            try:
                self.i2cBus = smbus.SMBus(1)
                self.i2cBus.write_byte_data(self.pressAddr, 0, 0)
                logging.info("I2C bus initialized for pressure sensor.")
            except Exception as e:
                logging.warning(f"I2C init failed: {e}")
                self.i2cBus = None
        else:
            logging.info("smbus not available, using simulated pressure values")
            self.i2cBus = None

    def generateTelemetry(self) -> SensorData:
        pressVal = None

        if HAS_SMBUS and self.i2cBus:
            try:
                rawPress = self.i2cBus.read_word_data(self.pressAddr, 0x28)
                pressVal = (rawPress / 65536.0) * 1100.0  # Adjust per sensor spec
            except Exception as e:
                logging.warning(f"I2C read failed: {e}")
                pressVal = None

        if pressVal is None:
            pressVal = random.uniform(
                SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE,
                SensorDataGenerator.HI_NORMAL_ENV_PRESSURE
            )

        sensorData = SensorData(typeID=self.sensorType)
        sensorData.setValue(pressVal)

        logging.info(
            "SensorData: name=%s, typeID=%s, value=%.2f hPa",
            sensorData.getName(),
            sensorData.getSensorType(),
            sensorData.getValue()
        )

        if self.dataMsgListener:
            try:
                self.dataMsgListener.handleSensorData(sensorData)
            except Exception as e:
                logging.warning("Listener failed to handle pressure data: %s", e)

        return sensorData

    def setDataMessageListener(self, listener):
        """
        Registers a listener to receive sensor data updates.
        """
        self.dataMsgListener = listener
