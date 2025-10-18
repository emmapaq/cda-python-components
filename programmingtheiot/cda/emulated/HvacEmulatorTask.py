"""
HVAC Actuator Emulator Task Module

This module provides HVAC actuator emulation functionality using the
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


class HvacEmulatorTask(BaseActuatorSimTask):
    """
    Emulator task for HVAC actuator using Sense HAT.
    
    This class extends BaseActuatorSimTask to provide HVAC control
    via the Sense HAT LED display, displaying activation status and values.
    """
    
    def __init__(self):
        """
        Constructor for HvacEmulatorTask.
        
        Initializes the parent class with HVAC actuator configuration
        and creates a SenseHAT instance with emulation mode based on
        the configuration file setting.
        """
        super(
            HvacEmulatorTask, self).__init__(
                name=ConfigConst.HVAC_ACTUATOR_NAME,
                typeID=ConfigConst.HVAC_ACTUATOR_TYPE,
                simpleName="HVAC")
        
        # Retrieve emulation flag from configuration file
        enableEmulation = \
            ConfigUtil().getBoolean(
                ConfigConst.CONSTRAINED_DEVICE,
                ConfigConst.ENABLE_EMULATOR_KEY)
        
        # Initialize SenseHAT with emulation mode
        self.sh = SenseHAT(emulate=enableEmulation)
    
    def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        """
        Activates the HVAC actuator by displaying a message on the Sense HAT LED screen.
        
        @param val: The actuation value (e.g., target temperature)
        @param stateData: Optional state data string
        @return: 0 on success, -1 on failure
        """
        if self.sh.screen:
            msg = self.getSimpleName() + ' ON: ' + str(val) + 'C'
            self.sh.screen.scroll_text(msg)
            return 0
        else:
            logging.warning("No SenseHAT LED screen instance to write.")
            return -1
    
    def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        """
        Deactivates the HVAC actuator by displaying an OFF message and clearing the screen.
        
        @param val: The actuation value (not used for deactivation)
        @param stateData: Optional state data string
        @return: 0 on success, -1 on failure
        """
        if self.sh.screen:
            msg = self.getSimpleName() + ' OFF'
            self.sh.screen.scroll_text(msg)
            
            # Optional sleep (5 seconds) for message to scroll before clearing display
            sleep(5)
            
            self.sh.screen.clear()
            return 0
        else:
            logging.warning("No SenseHAT LED screen instance to clear / close.")
            return -1