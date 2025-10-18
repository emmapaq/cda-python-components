"""
Temperature I2C Sensor Adapter Task Module

This module provides temperature sensor functionality using direct I2C bus
communication with the HTS221 sensor on the Sense HAT hardware.

License: PIOT-DOC-LIC
@author: Your Name
"""

import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

import smbus


class TemperatureI2cSensorAdapterTask(BaseSensorSimTask):
    """
    I2C adapter task for temperature sensor using Sense HAT hardware.
    
    This class extends BaseSensorSimTask to provide temperature readings
    directly from the HTS221 sensor via the I2C bus.
    """
    
    def __init__(self):
        """
        Constructor for TemperatureI2cSensorAdapterTask.
        
        Initializes the I2C bus connection to the HTS221 temperature sensor.
        """
        super(
            TemperatureI2cSensorAdapterTask, self).__init__(
                name=ConfigConst.TEMP_SENSOR_NAME,
                typeID=ConfigConst.TEMP_SENSOR_TYPE,
                minVal=SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP,
                maxVal=SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
        
        # HTS221 temperature sensor I2C address (same chip as humidity)
        # Read the HTS221 spec for the Sense HAT temperature sensor
        self.tempAddr = 0x5F
        
        # Initialize the I2C bus at the temperature address
        # WARNING: only use I2C bus 1 when working with the SenseHAT on the Raspberry Pi!!
        self.i2cBus = smbus.SMBus(1)
        
        # Initialize the sensor - power on
        # CTRL_REG1 (0x20): PD=1 (power on), BDU=1 (block data update)
        self.i2cBus.write_byte_data(self.tempAddr, 0x20, 0x87)
        
        logging.info("HTS221 temperature sensor initialized on I2C bus 1 at address 0x%02X", self.tempAddr)
    
    def generateTelemetry(self) -> SensorData:
        """
        Generates telemetry data by reading temperature from the HTS221 sensor via I2C.
        
        @return SensorData instance with the current temperature reading
        """
        # Create new SensorData instance
        sensorData = SensorData()
        sensorData.setName(self.getName())
        sensorData.setTypeID(self.getTypeID())
        
        try:
            # Read temperature calibration data from HTS221 sensor
            # T0_degC_x8 (0x32) and T1_degC_x8 (0x33) - calibration values
            t0_degC_x8 = self.i2cBus.read_byte_data(self.tempAddr, 0x32)
            t1_degC_x8 = self.i2cBus.read_byte_data(self.tempAddr, 0x33)
            
            # T1/T0 msb (0x35) - most significant bits for T0 and T1
            t1_t0_msb = self.i2cBus.read_byte_data(self.tempAddr, 0x35)
            
            # Combine to get full calibration temperatures
            t0_degC = ((t1_t0_msb & 0x03) << 8 | t0_degC_x8) / 8.0
            t1_degC = ((t1_t0_msb & 0x0C) << 6 | t1_degC_x8) / 8.0
            
            # T0_OUT (0x3C, 0x3D) and T1_OUT (0x3E, 0x3F) - calibration outputs
            t0_out = self._readS16(0x3C)
            t1_out = self._readS16(0x3E)
            
            # Read current temperature output (0x2A, 0x2B)
            t_out = self._readS16(0x2A)
            
            # Calculate temperature using linear interpolation
            temperature = t0_degC + (t1_degC - t0_degC) * (t_out - t0_out) / (t1_out - t0_out)
            
            sensorData.setValue(temperature)
            self.latestSensorData = sensorData
            
            logging.debug("I2C temperature reading: %f°C", temperature)
            
        except Exception as e:
            logging.error("Failed to read temperature from I2C sensor: %s", str(e))
            sensorData.setValue(0.0)
        
        return sensorData
    
    def _readS16(self, register: int) -> int:
        """
        Reads a signed 16-bit value from two consecutive I2C registers.
        
        @param register The starting register address
        @return The signed 16-bit integer value
        """
        # Read low byte and high byte
        low = self.i2cBus.read_byte_data(self.tempAddr, register)
        high = self.i2cBus.read_byte_data(self.tempAddr, register + 1)
        
        # Combine into 16-bit value
        value = (high << 8) | low
        
        # Convert to signed value
        if value >= 32768:
            value -= 65536
        
        return value