import logging
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SimulatedSensorData import SensorDataGenerator

class PressureSensorEmulatorTask(BaseSensorSimTask):
    """
    Simulated Pressure Sensor Emulator Task.
    """

    def __init__(self):
        super(PressureSensorEmulatorTask, self).__init__(
            typeID=SensorData.PRESSURE_SENSOR_TYPE,
            minVal=SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE,
            maxVal=SensorDataGenerator.HI_NORMAL_ENV_PRESSURE
        )
        self.dataMsgListener = None
        logging.info("PressureSensorEmulatorTask initialized.")

    def setDataMessageListener(self, listener):
        """Attach a data message listener for callback."""
        self.dataMsgListener = listener

    def getDataMessageListener(self):
        return self.dataMsgListener

    def generateTelemetry(self) -> SensorData:
        sensorData = super().generateTelemetry()
        if sensorData:
            logging.info("Pressure Sensor Reading: %.2f hPa", sensorData.getValue())
            if self.dataMsgListener:
                try:
                    self.dataMsgListener.handleSensorData(sensorData)
                except Exception as e:
                    logging.warning("Listener failed to handle pressure data: %s", e)
        return sensorData
