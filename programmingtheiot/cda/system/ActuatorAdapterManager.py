"""
ActuatorAdapterManager Module
License: PIOT-DOC-LIC

This class manages actuator simulators (for now).
Later, emulator support will be added.
"""

import logging

from programmingtheiot.common import ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData

# Simulated actuator tasks
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask
from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.LedActuatorSimTask import LedActuatorSimTask


class ActuatorAdapterManager:
	def __init__(self, dataMsgListener: IDataMessageListener = None):
		self.dataMsgListener = dataMsgListener
		self.configUtil = ConfigUtil()

		self.useSimulator = self.configUtil.getBoolean(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.ENABLE_SIMULATOR_KEY
		)

		self.useEmulator = self.configUtil.getBoolean(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.ENABLE_EMULATOR_KEY
		)

		self.deviceID = self.configUtil.getProperty(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.DEVICE_LOCATION_ID_KEY,
			defaultVal=ConfigConst.NOT_SET
		)

		self.locationID = self.configUtil.getProperty(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.DEVICE_LOCATION_ID_KEY,
			defaultVal=ConfigConst.NOT_SET
		)

		# Placeholders for actuators
		self.humidifierActuator = None
		self.hvacActuator = None
		self.ledDisplayActuator = None

		if self.useEmulator:
			logging.info("ActuatorAdapterManager initialized with EMULATOR mode.")
		else:
			logging.info("ActuatorAdapterManager initialized with SIMULATOR mode.")

		# Initialize actuator tasks
		self._initEnvironmentalActuationTasks()

	def _initEnvironmentalActuationTasks(self):
		"""
		Instantiate actuator tasks (simulators for now).
		"""
		if not self.useEmulator:
			# load the environmental tasks for simulated actuation
			self.humidifierActuator = HumidifierActuatorSimTask()
			self.hvacActuator = HvacActuatorSimTask()
			self.ledDisplayActuator = LedActuatorSimTask()

	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		if listener:
			self.dataMsgListener = listener
			return True
		return False

	def sendActuatorCommand(self, data: ActuatorData) -> ActuatorData:
		"""
		Dispatch actuator command to the correct actuator task.
		Validates location ID and ensures this is not a response message.
		"""
		if data and not data.isResponseFlagEnabled():
			# Ensure this actuation event is meant for this device
			if data.getLocationID() == self.locationID:
				logging.info(
					"Actuator command received for location ID %s. Processing...",
					str(data.getLocationID())
				)

				aType = data.getTypeID()
				responseData = None

				if aType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE and self.humidifierActuator:
					responseData = self.humidifierActuator.updateActuator(data)

				elif aType == ConfigConst.HVAC_ACTUATOR_TYPE and self.hvacActuator:
					responseData = self.hvacActuator.updateActuator(data)

				elif aType == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE and self.ledDisplayActuator:
					responseData = self.ledDisplayActuator.updateActuator(data)

				else:
					logging.warning(
						"No valid actuator type. Ignoring actuation for type: %s",
						data.getTypeID()
					)

				# Future: send responseData to DeviceDataManager via listener
				if self.dataMsgListener and responseData:
					self.dataMsgListener.handleActuatorCommandResponse(responseData)

				return responseData

			else:
				logging.warning(
					"Location ID doesn't match. Ignoring actuation: (me) %s != (you) %s",
					str(self.locationID),
					str(data.getLocationID())
				)
		else:
			logging.warning("Actuator request received. Message is empty or response. Ignoring.")

		return None
