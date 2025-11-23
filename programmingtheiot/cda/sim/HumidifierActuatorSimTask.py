import logging
import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

class HumidifierActuatorSimTask(BaseActuatorSimTask):
	"""
	This is a simple wrapper for an Actuator abstraction - it provides
	a container for the actuator's state, value, name, and status. A
	command variable is also provided to instruct the actuator to
	perform a specific function (in addition to setting a new value
	via the 'val' parameter.
	
	"""

	def __init__(self):
		pass
	
	def updateActuator(self, data: ActuatorData) -> ActuatorData:
	    """
	    Updates the Humidifier actuator state based on the command.
	    
	    Args:
	        data (ActuatorData): The actuator command
	        
	    Returns:
	        ActuatorData: The actuator response with updated state
	    """
	    if data:
	        command = data.getCommand()
	        
	        if command == ConfigConst.COMMAND_ON:
	            logging.info("Emulating Humidifier actuator ON: ")
	            print("***********")
	            print("*  O N  *")
	            print("***********")
	            print(f"HUMIDIFIER VALUE -> {data.getValue()}")
	            print("=======")
	        elif command == ConfigConst.COMMAND_OFF:
	            logging.info("Emulating Humidifier actuator OFF: ")
	            print("***********")
	            print("*  OFF  *")
	            print("***********")
	            print(f"HUMIDIFIER VALUE -> {data.getValue()}")
	            print("=======")
	        else:
	            logging.info(f"Emulating Humidifier actuator command: {command}")
	            print(f"HUMIDIFIER COMMAND -> {command}")
	            print(f"HUMIDIFIER VALUE -> {data.getValue()}")
	            print("=======")
	        
	        # CRITICAL: Set response flag and return the data
	        data.setAsResponse()
	        
	        # IMPORTANT: Return the ActuatorData
	        return data
	    else:
	        logging.warning("Received invalid ActuatorData. Ignoring.")
	        return None