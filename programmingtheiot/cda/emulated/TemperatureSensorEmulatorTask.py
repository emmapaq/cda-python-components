"""
Temperature Sensor Emulator Task Module

This module provides temperature sensor emulation functionality using the
Sense HAT emulator via the pisense library.

License: PIOT-DOC-LIC
@author: Your Name
"""

import logging
from programmingtheiot.data.SensorData import SensorData
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from pisense import SenseHAT


class TemperatureSensorEmulatorTask(BaseSensorSimTask):
    """
    Emulator task for temperature sensor using Sense HAT.

    This class extends BaseSensorSimTask to provide temperature readings
    from either the Sense HAT emulator or physical hardware, depending
    on the configuration setting.
    """

    def __init__(self):
        """
        Constructor for TemperatureSensorEmulatorTask.

        Initializes the parent class with temperature sensor configuration
        and creates a SenseHAT instance with emulation mode based on
        the configuration file setting.
        """
        super(TemperatureSensorEmulatorTask, self).__init__(
            name=ConfigConst.TEMP_SENSOR_NAME,
            typeID=ConfigConst.TEMP_SENSOR_TYPE
        )

        # Retrieve emulation flag from configuration file
        enableEmulation = ConfigUtil().getBoolean(
            ConfigConst.CONSTRAINED_DEVICE,
            ConfigConst.ENABLE_EMULATOR_KEY
        )

        logging.debug("Initializing SenseHAT with emulate=%s", enableEmulation)

        # Initialize SenseHAT with emulation mode
        self.sh = SenseHAT(emulate=enableEmulation)

    def generateTelemetry(self) -> SensorData:
        """
        Generates telemetry data by reading temperature from Sense HAT.

        Returns:
            SensorData: Object containing the current temperature reading
            with metadata (name, typeID, timestamp, etc.)
        """
        sensorData = SensorData()
        sensorData.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
        sensorData.setName(self.getName())

        # Read temperature value from Sense HAT
        sensorVal = self.sh.environ.temperature
        logging.debug("Raw temperature value from SenseHAT: %s", sensorVal)

        # Provide default value if reading fails
        if sensorVal is None:
            logging.warning("Temperature reading returned None. Using default value.")
            sensorVal = 20.0  # Default temperature in Celsius

        sensorData.setValue(sensorVal)
        logging.info("Generated SensorData: %s", sensorData)

        self.latestSensorData = sensorData
        return sensorData
