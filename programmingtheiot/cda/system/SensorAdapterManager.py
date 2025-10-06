import logging
from programmingtheiot.common import ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil

# I2C sensor imports (if available)
try:
    from programmingtheiot.cda.embedded.HumidityI2cSensorAdapterTask import HumidityI2cSensorAdapterTask
    from programmingtheiot.cda.embedded.PressureI2cSensorAdapterTask import PressureI2cSensorAdapterTask
    from programmingtheiot.cda.embedded.TemperatureI2cSensorAdapterTask import TemperatureI2cSensorAdapterTask
    I2C_AVAILABLE = True
except ImportError:
    I2C_AVAILABLE = False
    logging.warning("I2C sensor modules not available; will use emulators.")

# Emulator imports
from programmingtheiot.cda.sim.HumiditySensorEmulatorTask import HumiditySensorEmulatorTask
from programmingtheiot.cda.sim.PressureSensorEmulatorTask import PressureSensorEmulatorTask
from programmingtheiot.cda.sim.TemperatureSensorEmulatorTask import TemperatureSensorEmulatorTask

class SensorAdapterManager:
    """
    Manages sensor adapter tasks for humidity, pressure, and temperature.
    Automatically falls back to emulators if I2C sensors are unavailable.
    Provides test-compatible adapter attributes.
    """

    def __init__(self, useEmulator=True, useI2C=True):
        self.config = ConfigUtil()
        self.useEmulator = useEmulator
        self.useI2C = useI2C and I2C_AVAILABLE

        # Adapter attributes expected by tests
        self.humidityAdapter = None
        self.pressureAdapter = None
        self.tempAdapter = None

        self._initSensors()

    def _initSensors(self):
        if self.useI2C:
            try:
                self.humidityAdapter = HumidityI2cSensorAdapterTask()
                self.pressureAdapter = PressureI2cSensorAdapterTask()
                self.tempAdapter = TemperatureI2cSensorAdapterTask()
                logging.info("Loaded I2C sensor adapters.")
                return
            except Exception as e:
                logging.warning("I2C sensors unavailable, falling back to emulator: %s", e)

        if self.useEmulator:
            self.humidityAdapter = HumiditySensorEmulatorTask()
            self.pressureAdapter = PressureSensorEmulatorTask()
            self.tempAdapter = TemperatureSensorEmulatorTask()
            logging.info("Loaded simulator/emulator sensor adapters.")

    def generateAllTelemetry(self):
        """
        Generates telemetry data for all available sensors.
        Returns a dictionary with keys: 'humidity', 'pressure', 'temperature'.
        """
        data = {}
        if self.humidityAdapter:
            data['humidity'] = self.humidityAdapter.generateTelemetry()
        if self.pressureAdapter:
            data['pressure'] = self.pressureAdapter.generateTelemetry()
        if self.tempAdapter:
            data['temperature'] = self.tempAdapter.generateTelemetry()
        return data

    def setDataMessageListener(self, listener):
        """
        Set a listener object that implements handleSensorData(sensorData)
        for all available sensors.
        """
        if self.humidityAdapter:
            self.humidityAdapter.setDataMessageListener(listener)
        if self.pressureAdapter:
            self.pressureAdapter.setDataMessageListener(listener)
        if self.tempAdapter:
            self.tempAdapter.setDataMessageListener(listener)
