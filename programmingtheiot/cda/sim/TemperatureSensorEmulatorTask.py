import logging
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SimulatedSensorData import SensorDataGenerator

class TemperatureSensorEmulatorTask(BaseSensorSimTask):
    """
    Simulated Temperature Sensor Emulator Task.
    """

    def __init__(self):
        super(TemperatureSensorEmulatorTask, self).__init__(
            typeID=SensorData.TEMPERATURE_SENSOR_TYPE,
            minVal=SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP,
            maxVal=SensorDataGenerator.HI_NORMAL_INDOOR_TEMP
        )
        self.dataMsgListener = None
        logging.info("TemperatureSensorEmulatorTask initialized.")

    def setDataMessageListener(self, listener):
        """Attach a data message listener for callback."""
        self.dataMsgListener = listener

    def getDataMessageListener(self):
        return self.dataMsgListener

    def generateTelemetry(self) -> SensorData:
        sensorData = super().generateTelemetry()
        if sensorData:
            logging.info("Temperature Sensor Reading: %.2f °C", sensorData.getValue())
            if self.dataMsgListener:
                try:
                    self.dataMsgListener.handleSensorData(sensorData)
                except Exception as e:
                    logging.warning("Listener failed to handle temperature data: %s", e)
        return sensorData
