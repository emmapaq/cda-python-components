import logging
from apscheduler.schedulers.background import BackgroundScheduler

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.system.SystemCpuUtilTask import SystemCpuUtilTask
from programmingtheiot.cda.system.SystemMemUtilTask import SystemMemUtilTask

from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class SystemPerformanceManager:
    """
    SystemPerformanceManager collects system performance metrics
    such as CPU and memory utilization, stores them in
    SystemPerformanceData, and notifies a listener if set.
    """

    def __init__(self, locationID: str = None, pollRate: int = 5):
        # Initialize tasks
        self.cpuUtilTask = SystemCpuUtilTask()
        self.memUtilTask = SystemMemUtilTask()
        
        # Telemetry values
        self.cpuUtilPct = 0.0
        self.memUtilPct = 0.0
        
        # Optional location ID for system
        self.locationID = locationID
        
        # Listener for callbacks
        self.dataMsgListener: IDataMessageListener | None = None
        
        # Scheduler for periodic telemetry collection
        self.scheduler = BackgroundScheduler()
        self.pollRate = pollRate  # seconds

    def handleTelemetry(self):
        """Collect CPU and memory usage and notify listener if set."""
        self.cpuUtilPct = self.cpuUtilTask.getTelemetryValue()
        self.memUtilPct = self.memUtilTask.getTelemetryValue()
        
        logging.debug(
            "CPU utilization: %s%%, Memory utilization: %s%%",
            self.cpuUtilPct, self.memUtilPct
        )
        
        # Create SystemPerformanceData object
        sysPerfData = SystemPerformanceData()
        sysPerfData.setLocationID(self.locationID)
        sysPerfData.setCpuUtilization(self.cpuUtilPct)
        sysPerfData.setMemoryUtilization(self.memUtilPct)
        
        # Notify listener
        if self.dataMsgListener:
            self.dataMsgListener.handleSystemPerformanceMessage(data=sysPerfData)

    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        """Set the listener for telemetry callbacks."""
        if listener:
            self.dataMsgListener = listener
            return True
        return False

    def startManager(self):
        """Start periodic telemetry collection."""
        self.scheduler.add_job(self.handleTelemetry, 'interval', seconds=self.pollRate)
        self.scheduler.start()
        logging.info("SystemPerformanceManager started with poll rate %s seconds.", self.pollRate)

    def stopManager(self):
        """Stop periodic telemetry collection."""
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            logging.info("SystemPerformanceManager stopped.")
