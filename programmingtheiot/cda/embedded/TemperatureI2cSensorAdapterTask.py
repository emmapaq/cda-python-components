import logging
import random

try:
    import smbus
    HAS_SMBUS = True
except ImportError:
    smbus = None
    HAS_SMBUS = False

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SimulatedSensorData import SensorDataGenerator

class TemperatureI2cSensorAdapterTask(BaseSensorSimTask):
    """
    Adapter for HTS221 temperature sensor over I2C.
    Falls back to simulated values if I2C is unavailable.
    """

    def __init__(self):
        super(TemperatureI2cSensorAdapterTask, self).__init__(
            typeID=SensorData.TEMPERATURE_SENSOR_TYPE,
            minVal=SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP,
            maxVal=SensorDataGenerator.HI_NORMAL_INDOOR_TEMP
        )

        self.sensorType = SensorData.TEMPERATURE_SENSOR_TYPE
        self.tempAddr = 0x5F  # Shared with HTS221
        self.dataMsgListener = None

        if HAS_SMBUS:
            try:
                self.i2cBus = smbus.SMBus(1)
                self.i2cBus.write_byte_data(self.tempAddr, 0, 0)
                logging.info("I2C bus initialized for temperature sensor.")
            except Exception as e:
                logging.warning(f"I2C init failed: {e}")
                self.i2cBus = None
        else:
            logging.info("smbus not available, using simulated temperature values")
            self.i2cBus = None

    def generateTelemetry(self) -> SensorData:
        tempVal = None

        if HAS_SMBUS and self.i2cBus:
            try:
                rawTemp = self.i2cBus.read_word_data(self.tempAddr, 0x2A)
                tempVal = (rawTemp / 65536.0) * 120.0 - 40.0  # Adjust per sensor spec
            except Exception as e:
                logging.warning(f"I2C read failed: {e}")
                tempVal = None

        if tempVal is None:
            tempVal = random.uniform(
                SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP,
                SensorDataGenerator.HI_NORMAL_INDOOR_TEMP
            )

        sensorData = SensorData(typeID=self.sensorType)
        sensorData.setValue(tempVal)

        logging.info(
            "SensorData: name=%s, typeID=%s, value=%.2f °C",
            sensorData.getName(),
            sensorData.getSensorType(),
            sensorData.getValue()
        )

        if self.dataMsgListener:
            try:
                self.dataMsgListener.handleSensorData(sensorData)
            except Exception as e:
                logging.warning("Listener failed to handle temperature data: %s", e)

        return sensorData

    def setDataMessageListener(self, listener):
        """
        Registers a listener to receive sensor data updates.
        """
        self.dataMsgListener = listener
