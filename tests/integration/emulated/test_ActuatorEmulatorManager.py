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

from programmingtheiot.common import ConfigConst
from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData

class ActuatorEmulatorManagerTest(unittest.TestCase):
    """
    This test case class contains very basic unit tests for
    ActuatorAdapterManager emulation using SenseHAT.
    
    NOTE: This test requires the sense_emu_gui to be running
    and must have access to the underlying libraries that
    support the pisense module.
    """
    
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("Testing ActuatorAdapterManager class [using SenseHAT emulator]...")

        # Default message listener to capture actuator updates
        cls.defaultMsgListener = DefaultDataMessageListener()

        # Create the ActuatorAdapterManager instance
        cls.actuatorAdapterMgr = ActuatorAdapterManager()
        cls.actuatorAdapterMgr.setDataMessageListener(cls.defaultMsgListener)

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testHumidifierEmulation(self):
        ad = ActuatorData(typeID=ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
        ad.setValue(50.0)

        # Turn on humidifier
        ad.setCommand(ConfigConst.COMMAND_ON)
        self.actuatorAdapterMgr.sendActuatorCommand(ad)

        # Turn off humidifier
        ad.setCommand(ConfigConst.COMMAND_OFF)
        self.actuatorAdapterMgr.sendActuatorCommand(ad)

    def testHvacEmulation(self):
        ad = ActuatorData(typeID=ConfigConst.HVAC_ACTUATOR_TYPE)
        ad.setValue(22.5)

        # Turn on HVAC
        ad.setCommand(ConfigConst.COMMAND_ON)
        self.actuatorAdapterMgr.sendActuatorCommand(ad)

        # Turn off HVAC
        ad.setCommand(ConfigConst.COMMAND_OFF)
        self.actuatorAdapterMgr.sendActuatorCommand(ad)

    def testLedDisplayEmulation(self):
        ad = ActuatorData(typeID=ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        
        # Turn on LED display with text
        ad.setCommand(ConfigConst.COMMAND_ON)
        ad.setStateData("What's up?")
        self.actuatorAdapterMgr.sendActuatorCommand(ad)

        # Turn off LED display
        ad.setCommand(ConfigConst.COMMAND_OFF)
        self.actuatorAdapterMgr.sendActuatorCommand(ad)

if __name__ == "__main__":
    unittest.main()
