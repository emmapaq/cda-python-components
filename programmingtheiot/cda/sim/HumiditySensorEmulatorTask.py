import logging
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SimulatedSensorData import SensorDataGenerator

class HumiditySensorEmulatorTask(BaseSensorSimTask):
    """
    Simulated Humidity Sensor Emulator Task.
    """

    def __init__(self):
        super(HumiditySensorEmulatorTask, self).__init__(
            typeID=SensorData.HUMIDITY_SENSOR_TYPE,
            minVal=SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY,
            maxVal=SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY
        )
        self.dataMsgListener = None
        logging.info("HumiditySensorEmulatorTask initialized.")

    def setDataMessageListener(self, listener):
        """Attach a data message listener for callback."""
        self.dataMsgListener = listener

    def getDataMessageListener(self):
        return self.dataMsgListener

    def generateTelemetry(self) -> SensorData:
        sensorData = super().generateTelemetry()
        if sensorData:
            logging.info("Humidity Sensor Reading: %.2f %%", sensorData.getValue())
            if self.dataMsgListener:
                try:
                    self.dataMsgListener.handleSensorData(sensorData)
                except Exception as e:
                    logging.warning("Listener failed to handle humidity data: %s", e)
        return sensorData
