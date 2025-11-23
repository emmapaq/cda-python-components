#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#
# Copyright (c) 2020 - 2025 by Andrew D. King
#

import logging
import unittest

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager
from programmingtheiot.data.ActuatorData import ActuatorData


class DeviceDataManagerIntegrationTest(unittest.TestCase):
    """
    Integration test for DeviceDataManager.
    
    This test verifies the complete integration of:
    - SenseHAT emulator for sensor data collection
    - MQTT client for communication with GDA
    - Threshold-based actuation logic
    - Sensor data analysis and actuator triggering
    
    NOTE: This test REQUIRES the sense_emu_gui to be running if
    'enableEmulator' flag is True within the ConstrainedDevice section
    of PiotConfig.props.
    
    PREREQUISITES:
    1. SenseHAT emulator running (sense_emu_gui)
    2. MQTT broker running (mosquitto)
    3. PiotConfig.props configured with:
       - enableMqttClient = True
       - enableEmulator = True
       - nominalTempFloor = 18.0
       - nominalTempCeiling = 24.0
    """
    
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.INFO
        )
        logging.info("=" * 70)
        logging.info("DEVICE DATA MANAGER INTEGRATION TEST")
        logging.info("=" * 70)
        logging.info("This test will run for 5 minutes (300 seconds).")
        logging.info("")
        logging.info("INSTRUCTIONS:")
        logging.info("1. Make sure SenseHAT emulator is running")
        logging.info("2. Make sure MQTT broker (mosquitto) is running")
        logging.info("3. During the test, adjust the temperature slider on the emulator:")
        logging.info("   - Move it ABOVE the ceiling threshold (24.0°C)")
        logging.info("   - Move it BELOW the floor threshold (18.0°C)")
        logging.info("4. Watch for:")
        logging.info("   - Actuator command messages in the logs")
        logging.info("   - LED display updates on the emulator")
        logging.info("   - MQTT messages being published")
        logging.info("=" * 70)
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    #@unittest.skip("Ignore for now.")
    def testDeviceDataMgrTimedIntegration(self):
        """
        Timed integration test for DeviceDataManager.
        
        Runs the complete system for 5 minutes, allowing manual testing
        of threshold-based actuation via SenseHAT emulator.
        
        This test validates:
        - Sensor data collection from SenseHAT emulator
        - Threshold monitoring and analysis
        - Automatic actuator command triggering
        - MQTT communication with GDA
        - LED display updates on threshold crossings
        """
        logging.info("\n***** testDeviceDataMgrTimedIntegration *****\n")
        
        # OPTION 1: For MQTT testing - be sure the MQTT client is enabled in `PiotConfig.props`,
        #           and your MQTT broker is running (as per the Setup instructions above).
        # OPTION 2: For CoAP testing - be sure the CoAP client is enabled in `PiotConfig.props`,
        #           and your CoAP server is running within your GDA.
        
        logging.info("Creating DeviceDataManager...")
        ddMgr = DeviceDataManager()
        
        logging.info("Starting DeviceDataManager...")
        ddMgr.startManager()
        
        logging.info("\n" + "=" * 70)
        logging.info("SYSTEM RUNNING - Test Started")
        logging.info("=" * 70)
        logging.info("Adjust temperature on SenseHAT emulator to test thresholds:")
        logging.info("  - Ceiling: 24.0°C")
        logging.info("  - Floor: 18.0°C")
        logging.info("Test will run for 300 seconds (5 minutes)...")
        logging.info("=" * 70 + "\n")
        
        # 5 min's should be long enough to run the tests and manually adjust the emulator values
        sleep(300)
        
        logging.info("\n" + "=" * 70)
        logging.info("Test time complete. Stopping DeviceDataManager...")
        logging.info("=" * 70 + "\n")
        
        ddMgr.stopManager()
        
        logging.info("DeviceDataManager stopped. Integration test complete.")


if __name__ == "__main__":
    unittest.main()