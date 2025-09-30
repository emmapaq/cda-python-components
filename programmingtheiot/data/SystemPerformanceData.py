from .BaseIotData import BaseIotData
from programmingtheiot.common import ConfigConst


class SystemPerformanceData(BaseIotData):
    """
    SystemPerformanceData represents system performance metrics such as CPU and memory utilization.
    Inherits from BaseIotData.
    """

    def __init__(self, d=None):
        super(SystemPerformanceData, self).__init__(
            name=ConfigConst.SYSTEM_PERF_MSG,
            typeID=ConfigConst.SYSTEM_PERF_TYPE,
            d=d
        )
        self.cpuUtil = ConfigConst.DEFAULT_VAL
        self.memUtil = ConfigConst.DEFAULT_VAL

    def getCpuUtilization(self) -> float:
        return self.cpuUtil

    def setCpuUtilization(self, cpuUtil: float):
        self.cpuUtil = cpuUtil
        self.updateTimeStamp()

    def getMemoryUtilization(self) -> float:
        return self.memUtil

    def setMemoryUtilization(self, memUtil: float):
        self.memUtil = memUtil
        self.updateTimeStamp()

    def _handleUpdateData(self, data):
        if data and isinstance(data, SystemPerformanceData):
            self.cpuUtil = data.getCpuUtilization()
            self.memUtil = data.getMemoryUtilization()

    def __str__(self):
        return (f"SystemPerformanceData [cpuUtil={self.cpuUtil}, memUtil={self.memUtil}, "
                f"timeStamp={self.timeStamp}]")
