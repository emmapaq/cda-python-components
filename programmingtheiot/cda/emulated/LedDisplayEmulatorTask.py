
import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

from programmingtheiot.data.ActuatorData import ActuatorData

from pisense import SenseHAT

class LedDisplayEmulatorTask(BaseActuatorSimTask):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		pass

	def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		pass

	def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
		pass
	
	def updateActuator(self, data: ActuatorData) -> bool:
	    """
	    Enhanced LED display with fermentation-specific formatting.
	    """
	    if data:
	        command = data.getCommand()
	        message = data.getStateData() if data.getStateData() else "No message"
	        
	        # Color coding based on command
	        if command == ConfigConst.LED_OPTIMAL_CMD:
	            displayColor = "\033[92m"  # Green
	            prefix = "✓ "
	        elif command == ConfigConst.LED_ACTIVE_CMD:
	            displayColor = "\033[93m"  # Yellow
	            prefix = "⚡ "
	        elif command == ConfigConst.LED_ALERT_CMD:
	            displayColor = "\033[91m"  # Red
	            prefix = "⚠ "
	        else:
	            displayColor = "\033[0m"   # Default
	            prefix = ""
	        
	        resetColor = "\033[0m"
	        
	        # Display on console (simulated LED)
	        print(f"\n{'='*50}")
	        print(f"{displayColor}{prefix}{message}{resetColor}")
	        print(f"{'='*50}\n")
	        
	        # If using SenseHAT emulator, show message there too
	        if self.sh:
	            self.sh.show_message(message, scroll_speed=0.05)
	        
	        return True
	    
	    return False
	