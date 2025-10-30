

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.BaseIotData import BaseIotData

class SystemPerformanceData(BaseIotData):
    """
    Shell representation of class for student implementation.
    """
    DEFAULT_VAL = 0.0

    def __init__(self, d = None):
        super(SystemPerformanceData, self).__init__(
            name=ConfigConst.SYSTEM_PERF_MSG, 
            typeID=ConfigConst.SYSTEM_PERF_TYPE
        )
        
        self.cpuUtil = self.DEFAULT_VAL
        self.memUtil = self.DEFAULT_VAL
        self.diskUtil = self.DEFAULT_VAL

    def getCpuUtilization(self):
        return self.cpuUtil

    def getDiskUtilization(self):
        return self.diskUtil

    def getMemoryUtilization(self):
        return self.memUtil

    def setCpuUtilization(self, cpuUtil):
        self.cpuUtil = cpuUtil

    def setDiskUtilization(self, diskUtil):
        self.diskUtil = diskUtil

    def setMemoryUtilization(self, memUtil):
        self.memUtil = memUtil

    def _handleUpdateData(self, data):
        if data and isinstance(data, SystemPerformanceData):
            self.cpuUtil = data.getCpuUtilization()
            self.memUtil = data.getMemoryUtilization()
            self.diskUtil = data.getDiskUtilization()