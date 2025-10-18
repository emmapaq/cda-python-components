"""
LED Display Actuator Emulator Task Module

This module provides LED display actuator emulation functionality using the
Sense HAT emulator via the pisense library.

License: PIOT-DOC-LIC
@author: Your Name
"""

import logging

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask
from pisense import SenseHAT


class LedDisplayEmulatorTask(BaseActuatorSimTask):
    """
    Emulator task for LED display actuator using Sense HAT.
    
    This class extends BaseActuatorSimTask to provide LED display control
    via the Sense HAT LED screen, displaying custom messages.
    """
    
    def __init__(self):
        """
        Constructor for LedDisplayEmulatorTask.
        
        Initializes the parent class with LED display actuator configuration
        and creates a SenseHAT instance with emulation mode based on
        the configuration file setting.
        """
        super(
            LedDisplayEmulatorTask, self).__init__(
                name=ConfigConst.LED_ACTUATOR_NAME,
                typeID=ConfigConst.LED_DISPLAY_ACTUATOR_TYPE,
                simpleName="LED_Display")
        
        # Retrieve emulation flag from configuration file
        enableEmulation = \
            ConfigUtil().getBoolean(
                ConfigConst.CONSTRAINED_DEVICE,
                ConfigConst.ENABLE_EMULATOR_KEY)
        
        # Initialize SenseHAT with emulation mode
        self.sh = SenseHAT(emulate=enableEmulation)
    
    def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        """
        Activates the LED display by scrolling the provided state data on the Sense HAT LED screen.
        
        @param val: The actuation value (not used for LED display)
        @param stateData: The message string to display on the LED screen
        @return: 0 on success, -1 on failure
        """
        if self.sh.screen:
            self.sh.screen.scroll_text(stateData, size=8)
            return 0
        else:
            logging.warning("No SenseHAT LED screen instance to write.")
            return -1
    
    def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        """
        Deactivates the LED display by clearing the Sense HAT LED screen.
        
        @param val: The actuation value (not used for deactivation)
        @param stateData: Optional state data string (not used for deactivation)
        @return: 0 on success, -1 on failure
        """
        if self.sh.screen:
            self.sh.screen.clear()
            return 0
        else:
            logging.warning("No SenseHAT LED screen instance to clear / close.")
            return -1
