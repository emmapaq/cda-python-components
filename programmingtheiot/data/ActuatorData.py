

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.BaseIotData import BaseIotData


class ActuatorData(BaseIotData):
    """
    Represents actuator data including command, value, and state information.
    """

    def __init__(self, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, name=ConfigConst.NOT_SET, d=None):
        """
        Constructor for ActuatorData.
        
        @param typeID The type ID of the actuator
        @param name The name of the actuator
        @param d Optional ActuatorData instance to copy from
        """
        super(ActuatorData, self).__init__(name=name, typeID=typeID, d=d)
        
        self.command = ConfigConst.DEFAULT_COMMAND
        self.stateData = None
        self.value = ConfigConst.DEFAULT_VAL
        self.isResponse = False
        
        # If initializing from another ActuatorData instance
        if d:
            self._handleUpdateData(d)

    def getCommand(self) -> int:
        """
        Returns the command value.
        
        @return The command (e.g., COMMAND_ON, COMMAND_OFF)
        """
        return self.command

    def getStateData(self) -> str:
        """
        Returns the state data string.
        
        @return The state data
        """
        return self.stateData

    def getValue(self) -> float:
        """
        Returns the actuation value.
        
        @return The actuation value
        """
        return self.value

    def isResponseFlagEnabled(self) -> bool:
        """
        Returns whether this is a response message.
        
        @return True if response flag is enabled, False otherwise
        """
        return self.isResponse

    def setCommand(self, command: int):
        """
        Sets the command value.
        
        @param command The command to set (e.g., COMMAND_ON, COMMAND_OFF)
        """
        self.command = command

    def setAsResponse(self):
        """
        Sets this ActuatorData as a response message.
        """
        self.isResponse = True

    def setStateData(self, stateData: str):
        """
        Sets the state data string.
        
        @param stateData The state data to set
        """
        self.stateData = stateData

    def setValue(self, val: float):
        """
        Sets the actuation value.
        
        @param val The value to set
        """
        self.value = val

    def _handleUpdateData(self, data):
        """
        Handles updating this instance from another ActuatorData instance.
        
        @param data The ActuatorData instance to copy from
        """
        if data and isinstance(data, ActuatorData):
            self.command = data.command
            self.stateData = data.stateData
            self.value = data.value
            self.isResponse = data.isResponse