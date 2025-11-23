"""
Test class for DeviceDataManager actuator command callback functionality.

This test verifies that the DeviceDataManager correctly processes actuator
command messages without requiring network connectivity (MQTT/CoAP disabled).

@author: Emma
"""

import logging
import unittest

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager
from programmingtheiot.data.ActuatorData import ActuatorData


class DeviceDataManagerCallbackTest(unittest.TestCase):
    """
    Test class for DeviceDataManager callback methods.
    
    Tests actuator command message handling with all communications disabled.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Class-level setup
        """
        logging.basicConfig(
            format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO  # Changed from DEBUG to reduce noise
        )
    
    def setUp(self):
        """
        Per-test setup
        """
        pass
    
    def tearDown(self):
        """
        Per-test cleanup
        """
        pass
    
    #@unittest.skip("Ignore for now.")
    def testActuatorDataCallback(self):
        """
        Test actuator command message handling.
        """
        logging.info("\n\n***** testActuatorDataCallback *****")
        
        ddMgr = DeviceDataManager(disableAllComms=True)
        
        # DEBUG: Check what was initialized
        logging.info(f"DeviceDataManager created")
        logging.info(f"  - actuatorAdapterManager: {ddMgr.actuatorAdapterManager}")
        logging.info(f"  - actuatorAdapterManager type: {type(ddMgr.actuatorAdapterManager)}")
        
        if ddMgr.actuatorAdapterManager:
            logging.info(f"  - hvacActuator: {ddMgr.actuatorAdapterManager.hvacActuator}")
            logging.info(f"  - humidifierActuator: {ddMgr.actuatorAdapterManager.humidifierActuator}")
        
        # Create actuator command data
        actuatorData = ActuatorData()
        actuatorData.setTypeID(ConfigConst.HVAC_ACTUATOR_TYPE)
        actuatorData.setName("HvacActuator")
        actuatorData.setCommand(ConfigConst.COMMAND_ON)
        actuatorData.setStateData("This is a test.")
        
        logging.info(f"Created actuator command:")
        logging.info(f"  - TypeID: {actuatorData.getTypeID()}")
        logging.info(f"  - Command: {actuatorData.getCommand()}")
        logging.info(f"  - StateData: {actuatorData.getStateData()}")
        
        # Send command through DeviceDataManager
        logging.info("Calling handleActuatorCommandMessage...")
        response = ddMgr.handleActuatorCommandMessage(actuatorData)
        
        logging.info(f"Response received: {response}")
        logging.info(f"Response type: {type(response)}")
        
        # Verify response
        if response:
            logging.info("Actuator command processed successfully.")
            logging.info("Response: " + str(response))
            self.assertIsNotNone(response)
            self.assertTrue(response.isResponseFlagEnabled())
        else:
            logging.error("FAILED: No response received from actuator.")
            logging.error("Check if ActuatorAdapterManager is properly initialized")
            logging.error("Check if sendActuatorCommand() is implemented")
            self.fail("Expected actuator response but got None")
        
        sleep(10)

if __name__ == "__main__":
    unittest.main()