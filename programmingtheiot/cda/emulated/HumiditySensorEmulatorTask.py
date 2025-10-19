"""
Humidity Sensor Emulator Task Module

This module provides humidity sensor emulation functionality using the
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


class HumiditySensorEmulatorTask(BaseSensorSimTask):
    """
    Emulator task for humidity sensor using Sense HAT.

    This class extends BaseSensorSimTask to provide humidity readings
    from either the Sense HAT emulator or physical hardware, depending
    on the configuration setting.
    """

    def __init__(self):
        """
        Constructor for HumiditySensorEmulatorTask.

        Initializes the parent class with humidity sensor configuration
        and creates a SenseHAT instance with emulation mode based on
        the configuration file setting.
        """
        super(HumiditySensorEmulatorTask, self).__init__(
            name=ConfigConst.HUMIDITY_SENSOR_NAME,
            typeID=ConfigConst.HUMIDITY_SENSOR_TYPE
        )

        enableEmulation = ConfigUtil().getBoolean(
            ConfigConst.CONSTRAINED_DEVICE,
            ConfigConst.ENABLE_EMULATOR_KEY
        )

        logging.debug("Initializing SenseHAT with emulate=%s", enableEmulation)

        self.sh = SenseHAT(emulate=enableEmulation)

    def generateTelemetry(self) -> SensorData:
        """
        Generates telemetry data by reading humidity from Sense HAT.

        Returns:
            SensorData: Object containing the current humidity reading
            with metadata (name, typeID, timestamp, etc.)
        """
        sensorData = SensorData()
        sensorData.setTypeID(ConfigConst.HUMIDITY_SENSOR_TYPE)
        sensorData.setName(self.getName())

        sensorVal = self.sh.environ.humidity
        logging.debug("Raw humidity value from SenseHAT: %s", sensorVal)

        if sensorVal is None:
            logging.warning("Humidity reading returned None. Using default value.")
            sensorVal = 50.0  # Default humidity percentage

        sensorData.setValue(sensorVal)
        logging.info("Generated SensorData: %s", sensorData)

        self.latestSensorData = sensorData
        return sensorData
