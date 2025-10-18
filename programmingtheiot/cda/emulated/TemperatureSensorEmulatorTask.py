"""
Temperature Sensor Emulator Task Module

This module provides temperature sensor emulation functionality using the
Sense HAT emulator via the pisense library.

License: PIOT-DOC-LIC
@author: Your Name
"""

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
        super(
            TemperatureSensorEmulatorTask, self).__init__(
                name=ConfigConst.TEMP_SENSOR_NAME,
                typeID=ConfigConst.TEMP_SENSOR_TYPE)
        
        # Retrieve emulation flag from configuration file
        # Default to True if not found in config
        enableEmulation = \
            ConfigUtil().getBoolean(
                ConfigConst.CONSTRAINED_DEVICE, 
                ConfigConst.ENABLE_EMULATOR_KEY)
        
        # Force emulation mode to True (uncomment if needed for debugging)
        # enableEmulation = True
        
        # Initialize SenseHAT with emulation mode
        # If enableEmulation is True, uses emulator
        # If False, attempts to use physical Sense HAT hardware
        self.sh = SenseHAT(emulate=enableEmulation)
    
    def generateTelemetry(self) -> SensorData:
        """
        Generates telemetry data by reading temperature from Sense HAT.
        
        This method retrieves the current temperature reading from the
        Sense HAT emulator or hardware, wraps it in a SensorData object,
        and updates the internal latestSensorData reference.
        
        Returns:
            SensorData: Object containing the current temperature reading
                       with metadata (name, typeID, timestamp, etc.)
        """
        # Create new SensorData instance
        sensorData = SensorData()
        
        # Set all metadata
        sensorData.setName(self.getName())
        sensorData.setTypeID(self.getTypeID())
        
        # Read temperature value from Sense HAT
        sensorVal = self.sh.environ.temperature
        
        # Set the sensor value
        sensorData.setValue(sensorVal)
        self.latestSensorData = sensorData
        
        return sensorData
