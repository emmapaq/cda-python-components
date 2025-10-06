try:
    import smbus
    HAS_SMBUS = True
except ImportError:
    HAS_SMBUS = False
    smbus = None

import logging
import random

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SimulatedSensorData import SensorDataGenerator

class HumidityI2cSensorAdapterTask(BaseSensorSimTask):
    """
    Adapter for HTS221 humidity sensor over I2C.
    Falls back to simulated values if I2C is unavailable.
    """

    def __init__(self):
        super(HumidityI2cSensorAdapterTask, self).__init__(
            typeID=SensorData.HUMIDITY_SENSOR_TYPE,
            minVal=SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY,
            maxVal=SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY
        )

        self.sensorType = SensorData.HUMIDITY_SENSOR_TYPE
        self.humidAddr = 0x5F  # HTS221 sensor address
        self.dataMsgListener = None

        if HAS_SMBUS:
            try:
                self.i2cBus = smbus.SMBus(1)
                self.i2cBus.write_byte_data(self.humidAddr, 0, 0)
                logging.info("I2C bus initialized for humidity sensor.")
            except Exception as e:
                logging.warning(f"I2C init failed: {e}")
                self.i2cBus = None
        else:
            logging.info("smbus not available, using simulated humidity values")
            self.i2cBus = None

    def generateTelemetry(self) -> SensorData:
        humidVal = None

        if HAS_SMBUS and self.i2cBus:
            try:
                rawHumid = self.i2cBus.read_word_data(self.humidAddr, 0x28)
                humidVal = (rawHumid / 65536.0) * 100.0
            except Exception as e:
                logging.warning(f"I2C read failed: {e}")
                humidVal = None

        if humidVal is None:
            humidVal = random.uniform(
                SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY,
                SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY
            )

        sensorData = SensorData(typeID=self.sensorType)
        sensorData.setValue(humidVal)

        logging.info(
            "SensorData: name=%s, typeID=%s, value=%.2f%%",
            sensorData.getName(),
            sensorData.getSensorType(),
            sensorData.getValue()
        )

        if self.dataMsgListener:
            try:
                self.dataMsgListener.handleSensorMessage(sensorData)
            except Exception as e:
                logging.warning("Listener failed to handle humidity data: %s", e)

        return sensorData

    def setDataMessageListener(self, listener):
        """
        Registers a listener to receive sensor data updates.
        """
        self.dataMsgListener = listener
