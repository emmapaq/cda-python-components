"""
Actuator Data Module

Represents actuator data including commands, values, and state information.
"""

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.BaseIotData import BaseIotData


class ActuatorData(BaseIotData):
    """
    Encapsulates actuator data and commands.
    
    This class represents data and commands for various actuator types
    including HVAC, humidifiers, LED displays, and other controllable devices.
    """
    
    # Actuator type constants
    DEFAULT_ACTUATOR_TYPE = ConfigConst.DEFAULT_TYPE_ID
    HVAC_ACTUATOR_TYPE = ConfigConst.HVAC_ACTUATOR_TYPE
    HUMIDIFIER_ACTUATOR_TYPE = ConfigConst.HUMIDIFIER_ACTUATOR_TYPE
    LED_DISPLAY_ACTUATOR_TYPE = ConfigConst.LED_DISPLAY_ACTUATOR_TYPE
    
    # Command constants
    COMMAND_OFF = ConfigConst.COMMAND_OFF
    COMMAND_ON = ConfigConst.COMMAND_ON
    COMMAND_UPDATE = ConfigConst.COMMAND_UPDATE
    COMMAND_SET_VALUE = ConfigConst.COMMAND_SET_VALUE
    COMMAND_GET_VALUE = ConfigConst.COMMAND_GET_VALUE
    
    def __init__(self, typeID: int = DEFAULT_ACTUATOR_TYPE, name: str = ConfigConst.NOT_SET):
        """
        Constructor for ActuatorData.
        
        Args:
            typeID: The actuator type ID (default: DEFAULT_ACTUATOR_TYPE)
            name: The actuator name (default: "Not Set")
        """
        super(ActuatorData, self).__init__(name=name, typeID=typeID)
        
        self.command = self.COMMAND_OFF
        self.stateData = None
        self.value = ConfigConst.DEFAULT_VAL
        self.isResponse = False
    
    def getCommand(self) -> int:
        """
        Gets the actuator command.
        
        Returns:
            int: The command value
        """
        return self.command
    
    def getStateData(self) -> str:
        """
        Gets the actuator state data.
        
        Returns:
            str: The state data as a string
        """
        return self.stateData
    
    def getValue(self) -> float:
        """
        Gets the actuator value.
        
        Returns:
            float: The actuator value
        """
        return self.value
    
    def isResponseFlagEnabled(self) -> bool:
        """
        Checks if this is a response message.
        
        Returns:
            bool: True if this is a response, False otherwise
        """
        return self.isResponse
    
    def setCommand(self, command: int):
        """
        Sets the actuator command.
        
        Args:
            command: The command value (COMMAND_OFF, COMMAND_ON, etc.)
        """
        self.command = command
        self.updateTimeStamp()
    
    def setStateData(self, stateData: str):
        """
        Sets the actuator state data.
        
        Args:
            stateData: The state data as a string
        """
        self.stateData = stateData
        self.updateTimeStamp()
    
    def setValue(self, val: float):
        """
        Sets the actuator value.
        
        Args:
            val: The value to set
        """
        self.value = val
        self.updateTimeStamp()
    
    def setAsResponse(self):
        """
        Marks this actuator data as a response message.
        """
        self.isResponse = True
    
    def __str__(self) -> str:
        """
        Returns a string representation of the ActuatorData.
        
        Returns:
            str: String representation
        """
        return f"ActuatorData(name={self.name}, typeID={self.typeID}, command={self.command}, value={self.value}, stateData={self.stateData}, timestamp={self.timeStamp})"
    
    def _handleUpdateData(self, data):
        """
        Internal method to update data from another ActuatorData instance.
        
        Args:
            data: Another ActuatorData instance to copy from
        """
        if data and isinstance(data, ActuatorData):
            self.command = data.getCommand()
            self.stateData = data.getStateData()
            self.value = data.getValue()
            self.isResponse = data.isResponseFlagEnabled()