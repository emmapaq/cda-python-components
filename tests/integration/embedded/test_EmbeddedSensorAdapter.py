#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License.
# 

import logging
import unittest
from time import sleep

from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from programmingtheiot.common.ConfigConst import CONSTRAINED_DEVICE, ENABLE_SENSE_HAT_KEY
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.data.SensorData import SensorData

class EmbeddedSensorAdapterTest(unittest.TestCase):
    """
    Integration test class for Humidity, Pressure, and Temperature
    I2C sensor adapters on the Raspberry Pi Sense HAT.
    
    NOTE: The Sense HAT must be attached, or the Sense-Emu
    emulator must be running if using the emulator flag.
    """

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Starting Embedded Sensor Adapter tests...")

        cls.configUtil = ConfigUtil()
        cls.useI2C = cls.configUtil.getBoolean(CONSTRAINED_DEVICE, ENABLE_SENSE_HAT_KEY)

        cls.defaultMsgListener = DefaultDataMessageListener()
        cls.sensorAdapterMgr = SensorAdapterManager()
        cls.sensorAdapterMgr.setDataMessageListener(cls.defaultMsgListener)

    def testHumidityI2CAdapter(self):
        if not self.useI2C:
            self.skipTest("I2C Humidity Adapter not enabled in config")
        
        humidityData = self.sensorAdapterMgr.humidityAdapter.generateTelemetry()
        logging.info(f"Humidity Sensor Reading: {humidityData.getValue()}%")
        self.assertIsInstance(humidityData, SensorData)
        self.assertTrue(0.0 <= humidityData.getValue() <= 100.0)

    def testPressureI2CAdapter(self):
        if not self.useI2C:
            self.skipTest("I2C Pressure Adapter not enabled in config")
        
        pressureData = self.sensorAdapterMgr.pressureAdapter.generateTelemetry()
        logging.info(f"Pressure Sensor Reading: {pressureData.getValue()} hPa")
        self.assertIsInstance(pressureData, SensorData)
        self.assertTrue(300.0 <= pressureData.getValue() <= 1100.0)  # realistic range

    def testTemperatureI2CAdapter(self):
        if not self.useI2C:
            self.skipTest("I2C Temperature Adapter not enabled in config")
        
        tempData = self.sensorAdapterMgr.tempAdapter.generateTelemetry()
        logging.info(f"Temperature Sensor Reading: {tempData.getValue()} °C")
        self.assertIsInstance(tempData, SensorData)
        self.assertTrue(-40.0 <= tempData.getValue() <= 120.0)  # realistic range

if __name__ == "__main__":
    unittest.main()
