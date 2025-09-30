import logging
import psutil

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.system.BaseSystemUtilTask import BaseSystemUtilTask

class SystemMemUtilTask(BaseSystemUtilTask):
	"""
	System Memory Utilization Task.

	This class collects the system memory usage as a percentage using psutil.
	It extends BaseSystemUtilTask.
	"""

	def __init__(self):
		# Initialize the base task with name and type constants
		super(SystemMemUtilTask, self).__init__(
			name = ConfigConst.MEM_UTIL_NAME,
			typeID = ConfigConst.MEM_UTIL_TYPE
		)

	def getTelemetryValue(self) -> float:
		"""
		Returns the current memory utilization percentage.
		
		:return: Memory usage as a float
		"""
		return psutil.virtual_memory().percent
