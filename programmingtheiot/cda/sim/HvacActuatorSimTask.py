import logging

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask


class HvacActuatorSimTask(BaseActuatorSimTask):
    """
    HVAC (Heating, Ventilation, and Air Conditioning) actuator simulator.
    
    Simulates HVAC control for temperature regulation.
    """
    
    def __init__(self):
        """
        Constructor
        """
        super(HvacActuatorSimTask, self).__init__(
            name=ConfigConst.HVAC_ACTUATOR_NAME,
            typeID=ConfigConst.HVAC_ACTUATOR_TYPE,
            simpleName="HVAC"
        )
    
    def updateActuator(self, data: ActuatorData) -> ActuatorData:
	    """
	    Updates the HVAC actuator state.
	    """
	    if data:
	        command = data.getCommand()
	        
	        if command == ConfigConst.COMMAND_ON:
	            logging.info("Emulating HVAC actuator ON: ")
	            print("*******")
	            print("* O N *")
	            print("*******")
	            print(f"HVAC VALUE -> {data.getValue()}")
	            print("=======")
	        elif command == ConfigConst.COMMAND_OFF:
	            logging.info("Emulating HVAC actuator OFF: ")
	            print("*******")
	            print("* OFF *")
	            print("*******")
	            print(f"HVAC VALUE -> {data.getValue()}")
	            print("=======")
	        
	        # Set as response
	        data.setAsResponse()
	        
	        # MUST RETURN THE DATA!
	        return data
	    
	    return None