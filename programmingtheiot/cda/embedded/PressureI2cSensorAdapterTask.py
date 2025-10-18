"""
Pressure I2C Sensor Adapter Task Module

This module provides pressure sensor functionality using direct I2C bus
communication with the LPS25H sensor on the Sense HAT hardware.

License: PIOT-DOC-LIC
@author: Your Name
"""

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

import smbus


class PressureI2cSensorAdapterTask(BaseSensorSimTask):
    """
    I2C adapter task for pressure sensor using Sense HAT hardware.
    
    This class extends BaseSensorSimTask to provide pressure readings
    directly from the LPS25H sensor via the I2C bus.
    """
    
    def __init__(self):
        """
        Constructor for PressureI2cSensorAdapterTask.
        
        Initializes the I2C bus connection to the LPS25H pressure sensor.
        """
        super(
            PressureI2cSensorAdapterTask, self).__init__(
                name=ConfigConst.PRESSURE_SENSOR_NAME,
                typeID=ConfigConst.PRESSURE_SENSOR_TYPE,
                minVal=SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE,
                maxVal=SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)
        
        # LPS25H pressure sensor I2C address
        # Read the LPS25H spec for the Sense HAT pressure sensor
        self.pressAddr = 0x5C
        
        # Initialize the I2C bus at the pressure address
        # WARNING: only use I2C bus 1 when working with the SenseHAT on the Raspberry Pi!!
        self.i2cBus = smbus.SMBus(1)
        
        # Initialize the sensor - power on and set ODR (Output Data Rate)
        # CTRL_REG1 (0x20): PD=1 (power on), ODR=011 (12.5 Hz)
        self.i2cBus.write_byte_data(self.pressAddr, 0x20, 0xB0)
        
        logging.info("LPS25H pressure sensor initialized on I2C bus 1 at address 0x%02X", self.pressAddr)
    
    def generateTelemetry(self) -> SensorData:
        """
        Generates telemetry data by reading pressure from the LPS25H sensor via I2C.
        
        @return SensorData instance with the current pressure reading
        """
        # Create new SensorData instance
        sensorData = SensorData()
        sensorData.setName(self.getName())
        sensorData.setTypeID(self.getTypeID())
        
        try:
            # Read pressure data from LPS25H sensor
            # Pressure output registers: PRESS_OUT_XL (0x28), PRESS_OUT_L (0x29), PRESS_OUT_H (0x2A)
            xl = self.i2cBus.read_byte_data(self.pressAddr, 0x28)
            l = self.i2cBus.read_byte_data(self.pressAddr, 0x29)
            h = self.i2cBus.read_byte_data(self.pressAddr, 0x2A)
            
            # Combine into 24-bit value
            raw_pressure = (h << 16) | (l << 8) | xl
            
            # Convert to hPa (hectopascals / millibars)
            # LPS25H outputs pressure in 1/4096 hPa units
            pressure = raw_pressure / 4096.0
            
            sensorData.setValue(pressure)
            self.latestSensorData = sensorData
            
            logging.debug("I2C pressure reading: %f hPa", pressure)
            
        except Exception as e:
            logging.error("Failed to read pressure from I2C sensor: %s", str(e))
            sensorData.setValue(0.0)
        
        return sensorData