"""
Pressure Sensor Emulator Task Module

This module provides pressure sensor emulation functionality using the
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


class PressureSensorEmulatorTask(BaseSensorSimTask):
    """
    Emulator task for pressure sensor using Sense HAT.

    This class extends BaseSensorSimTask to provide pressure readings
    from either the Sense HAT emulator or physical hardware, depending
    on the configuration setting.
    """

    def __init__(self):
        """
        Constructor for PressureSensorEmulatorTask.

        Initializes the parent class with pressure sensor configuration
        and creates a SenseHAT instance with emulation mode based on
        the configuration file setting.
        """
        super(PressureSensorEmulatorTask, self).__init__(
            name=ConfigConst.PRESSURE_SENSOR_NAME,
            typeID=ConfigConst.PRESSURE_SENSOR_TYPE
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
        Generates telemetry data by reading pressure from Sense HAT.

        Returns:
            SensorData: Object containing the current pressure reading
            with metadata (name, typeID, timestamp, etc.)
        """
        sensorData = SensorData()
        sensorData.setTypeID(ConfigConst.PRESSURE_SENSOR_TYPE)
        sensorData.setName(self.getName())

        # Read pressure value from Sense HAT
        sensorVal = self.sh.environ.pressure
        logging.debug("Raw pressure value from SenseHAT: %s", sensorVal)

        # Provide default value if reading fails
        if sensorVal is None:
            logging.warning("Pressure reading returned None. Using default value.")
            sensorVal = 1013.25  # Default atmospheric pressure in hPa

        sensorData.setValue(sensorVal)
        logging.info("Generated SensorData: %s", sensorData)

        self.latestSensorData = sensorData
        return sensorData
