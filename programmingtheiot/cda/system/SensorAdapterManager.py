"""
SensorAdapterManager Module
License: PIOT-DOC-LIC

This class manages sensor simulators (humidity, pressure, temperature).
It uses APScheduler to periodically generate telemetry data and forward it
to an IDataMessageListener implementation.
"""

import logging
from apscheduler.schedulers.background import BackgroundScheduler

from programmingtheiot.common import ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil

from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask


from programmingtheiot.common.IDataMessageListener import IDataMessageListener


class SensorAdapterManager:
	def __init__(self):
		self.configUtil = ConfigUtil()

		# Retrieve configuration values
		self.pollRate = self.configUtil.getInteger(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.POLL_CYCLES_KEY,
			defaultVal=ConfigConst.DEFAULT_POLL_CYCLES
		)

		self.useEmulator = self.configUtil.getBoolean(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.ENABLE_EMULATOR_KEY
		)

		self.locationID = self.configUtil.getProperty(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.DEVICE_LOCATION_ID_KEY,
			defaultVal=ConfigConst.NOT_SET
		)

		if self.pollRate <= 0:
			self.pollRate = ConfigConst.DEFAULT_POLL_CYCLES

		# Log emulator/simulator usage
		if self.useEmulator:
			logging.info("SensorAdapterManager initialized with EMULATOR mode.")
		else:
			logging.info("SensorAdapterManager initialized with SIMULATOR mode.")

		# Scheduler configuration
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job(
			self.handleTelemetry,
			'interval',
			seconds=self.pollRate,
			max_instances=2,
			coalesce=True,
			misfire_grace_time=15
		)

		# Placeholders for adapters
		self.dataMsgListener = None
		self.humidityAdapter = None
		self.pressureAdapter = None
		self.tempAdapter = None

		# Initialize tasks
		self._initEnvironmentalSensorTasks()

	def _initEnvironmentalSensorTasks(self):
		# Retrieve floor and ceiling values
		humidityFloor = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.HUMIDITY_SIM_FLOOR_KEY,
			defaultVal=SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY
		)
		humidityCeiling = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.HUMIDITY_SIM_CEILING_KEY,
			defaultVal=SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY
		)

		pressureFloor = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.PRESSURE_SIM_FLOOR_KEY,
			defaultVal=SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE
		)
		pressureCeiling = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.PRESSURE_SIM_CEILING_KEY,
			defaultVal=SensorDataGenerator.HI_NORMAL_ENV_PRESSURE
		)

		tempFloor = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.TEMP_SIM_FLOOR_KEY,
			defaultVal=SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP
		)
		tempCeiling = self.configUtil.getFloat(
			section=ConfigConst.CONSTRAINED_DEVICE,
			key=ConfigConst.TEMP_SIM_CEILING_KEY,
			defaultVal=SensorDataGenerator.HI_NORMAL_INDOOR_TEMP
		)

		if not self.useEmulator:
			self.dataGenerator = SensorDataGenerator()

			humidityData = self.dataGenerator.generateDailyEnvironmentHumidityDataSet(
				minValue=humidityFloor, maxValue=humidityCeiling, useSeconds=False
			)
			pressureData = self.dataGenerator.generateDailyEnvironmentPressureDataSet(
				minValue=pressureFloor, maxValue=pressureCeiling, useSeconds=False
			)
			tempData = self.dataGenerator.generateDailyIndoorTemperatureDataSet(
				minValue=tempFloor, maxValue=tempCeiling, useSeconds=False
			)

			# Create sensor sim tasks
			self.humidityAdapter = HumiditySensorSimTask(dataSet=humidityData)
			self.pressureAdapter = PressureSensorSimTask(dataSet=pressureData)
			self.tempAdapter = TemperatureSensorSimTask(dataSet=tempData)

	def setDataMessageListener(self, listener: IDataMessageListener):
		if listener:
			self.dataMsgListener = listener

	def startManager(self) -> bool:
		logging.info("Starting SensorAdapterManager...")
		if not self.scheduler.running:
			self.scheduler.start()
			return True
		else:
			logging.info("SensorAdapterManager scheduler already started. Ignoring.")
			return False

	def stopManager(self) -> bool:
		logging.info("Stopping SensorAdapterManager...")
		try:
			self.scheduler.shutdown()
			return True
		except Exception:
			logging.info("SensorAdapterManager scheduler already stopped. Ignoring.")
			return False

	def handleTelemetry(self):
		# Generate telemetry from each sensor
		humidityData = self.humidityAdapter.generateTelemetry()
		pressureData = self.pressureAdapter.generateTelemetry()
		tempData = self.tempAdapter.generateTelemetry()

		# Attach location ID
		humidityData.setLocationID(self.locationID)
		pressureData.setLocationID(self.locationID)
		tempData.setLocationID(self.locationID)

		# Debug logs
		logging.debug("Generated humidity data: %s", str(humidityData))
		logging.debug("Generated pressure data: %s", str(pressureData))
		logging.debug("Generated temperature data: %s", str(tempData))

		# Notify listener if set
		if self.dataMsgListener:
			self.dataMsgListener.handleSensorMessage(humidityData)
			self.dataMsgListener.handleSensorMessage(pressureData)
			self.dataMsgListener.handleSensorMessage(tempData)
