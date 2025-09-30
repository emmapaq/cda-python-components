from .BaseIotData import BaseIotData
# import src.main.python.programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common import ConfigConst


class ActuatorData(BaseIotData):
    """
    ActuatorData represents actuator command data with numeric and state information.
    Inherits from BaseIotData.
    """

    def __init__(self, typeID: int = ConfigConst.DEFAULT_ACTUATOR_TYPE, name=ConfigConst.NOT_SET, d=None):
        super(ActuatorData, self).__init__(name=name, typeID=typeID, d=d)

        self.value = ConfigConst.DEFAULT_VAL
        self.command = ConfigConst.DEFAULT_COMMAND
        self.stateData = ""
        self.isResponse = False

    def getCommand(self) -> int:
        return self.command

    def setCommand(self, command: int):
        self.command = command
        self.updateTimeStamp()

    def getStateData(self) -> str:
        return self.stateData

    def setStateData(self, stateData: str):
        if stateData:
            self.stateData = stateData
            self.updateTimeStamp()

    def getValue(self) -> float:
        return self.value

    def setValue(self, val: float):
        self.value = val
        self.updateTimeStamp()

    def isResponseFlagEnabled(self) -> bool:
        return self.isResponse

    def setAsResponse(self):
        self.isResponse = True
        self.updateTimeStamp()

    def _handleUpdateData(self, data):
        if data and isinstance(data, ActuatorData):
            self.command = data.getCommand()
            self.stateData = data.getStateData()
            self.value = data.getValue()
            self.isResponse = data.isResponseFlagEnabled()

    def __str__(self):
        return (f"ActuatorData [name={self.getName()}, typeID={self.getTypeID()}, "
                f"value={self.value}, command={self.command}, stateData={self.stateData}, "
                f"isResponse={self.isResponse}, timeStamp={self.timeStamp}]")
