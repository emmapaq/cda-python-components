#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# You may find it more helpful to your design to adjust the
# functionality, constants and interfaces (if there are any)
# provided within in order to meet the needs of your specific
# Programming the Internet of Things project.
# 

import logging
import random

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.ActuatorData import ActuatorData


class BaseActuatorSimTask():
    """
    Base class for actuator simulation and emulation tasks.
    """
    
    def __init__(self, name: str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, simpleName: str = "Actuator"):
        """
        Constructor for BaseActuatorSimTask.
        
        @param name The name of the actuator
        @param typeID The type ID of the actuator
        @param simpleName A simple name for display purposes
        """
        self.name = name
        self.typeID = typeID
        self.simpleName = simpleName
        self.latestActuatorData = None
        
        logging.info("Initialized actuator simulator: name=%s, typeID=%d, simpleName=%s", 
                     self.name, self.typeID, self.simpleName)
    
    def getLatestActuatorResponse(self) -> ActuatorData:
        """
        This can return the current ActuatorData response instance or a copy.
        """
        if self.latestActuatorData is None:
            logging.warning("ActuatorData is None.")
        
        return self.latestActuatorData
    
    def getSimpleName(self) -> str:
        """
        Returns the simple name of this actuator.
        """
        return self.simpleName
    
    def getName(self) -> str:
        """
        Returns the name of this actuator.
        """
        return self.name
    
    def getTypeID(self) -> int:
        """
        Returns the type ID of this actuator.
        """
        return self.typeID
    
    def updateActuator(self, data: ActuatorData) -> ActuatorData:
        """
        NOTE: If 'data' is valid, the actuator-specific work can be delegated
        as follows:
         - if command is ON: call self._activateActuator()
         - if command is OFF: call self._deactivateActuator()
        
        Both of these methods will have a generic implementation (logging only) within
        this base class, although the sub-class may override if preferable.
        """
        if data:
            logging.debug("New actuator command and value to be applied: %s %s", 
                         data.getCommand(), data.getValue())
            
            if data.getCommand() == ConfigConst.COMMAND_OFF:
                logging.info("Deactivating actuator...")
                statusCode = self._deactivateActuator(
                    val=data.getValue(),
                    stateData=data.getStateData())
            else:
                logging.info("Activating actuator...")
                statusCode = self._activateActuator(
                    val=data.getValue(),
                    stateData=data.getStateData())
            
            data.setStatusCode(statusCode)
            self.latestActuatorData = data
        
        return data
    
    def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        """
        Implement basic logging. Actuator-specific functionality should be implemented by sub-class.
        
        @param val The actuation activation value to process.
        @param stateData The string state data to use in processing the command.
        """
        logging.info("Simulating actuator activation with value: %s", val)
        return 0
    
    def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        """
        Implement basic logging. Actuator-specific functionality should be implemented by sub-class.
        
        @param val The actuation activation value to process.
        @param stateData The string state data to use in processing the command.
        """
        logging.info("Simulating actuator deactivation")
        return 0