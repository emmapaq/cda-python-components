import logging
import psutil

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask

class SystemCpuUtilTask(BaseSystemUtilTask):
	"""
	System CPU Utilization Task.

	This class is responsible for retrieving the system's CPU usage
	as a percentage using the psutil library.
	"""

	def __init__(self):
		# Call the base constructor with proper telemetry name and type
		super(SystemCpuUtilTask, self).__init__(
			name = ConfigConst.CPU_UTIL_NAME,
			typeID = ConfigConst.CPU_UTIL_TYPE
		)

	def getTelemetryValue(self) -> float:
		"""
		Returns the current CPU utilization percentage.
		
		:return: CPU usage as a float
		"""
		return psutil.cpu_percent()
