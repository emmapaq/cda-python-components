import logging
from importlib import import_module

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil

# Simulated actuator tasks
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask
from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask

class ActuatorAdapterManager:
    def __init__(self):
        self.configUtil = ConfigUtil()
        self.useEmulator = self.configUtil.getBoolean(
            ConfigConst.CONSTRAINED_DEVICE,
            ConfigConst.ENABLE_EMULATOR_KEY
        )
        logging.info(f"ActuatorAdapterManager initialized (useEmulator={self.useEmulator})")

        self.dataMsgListener = None

        # Initialize actuator adapters
        self._initEnvironmentalActuationTasks()

    def setDataMessageListener(self, listener):
        """Register a listener object that implements handleActuatorMessage(msg)."""
        self.dataMsgListener = listener
        logging.info("Data message listener has been set.")

    def sendActuatorCommand(self, actuatorData):
        """Send command to the appropriate actuator."""
        typeID = actuatorData.getTypeID()

        # Humidifier
        if typeID == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE:
            self._executeActuatorCommand(self.humidifierActuator, actuatorData)

        # HVAC
        elif typeID == ConfigConst.HVAC_ACTUATOR_TYPE:
            self._executeActuatorCommand(self.hvacActuator, actuatorData)

        # LED display (if implemented)
        elif hasattr(self, "ledDisplayActuator") and typeID == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE:
            self._executeActuatorCommand(self.ledDisplayActuator, actuatorData)

        else:
            logging.warning(f"No actuator available for typeID: {typeID}")

    def _executeActuatorCommand(self, actuator, actuatorData):
        """Call the correct method for either emulator or simulator."""
        if hasattr(actuator, "applyCommand"):
            actuator.applyCommand(actuatorData)
        elif hasattr(actuator, "activateActuator"):
            actuator.activateActuator(actuatorData)
        else:
            logging.warning(f"Actuator {actuator} has no valid command method")

    def _initEnvironmentalActuationTasks(self):
        """Initialize all actuator tasks (simulated or emulated)."""
        if not self.useEmulator:
            # Simulated actuators
            self.humidifierActuator = HumidifierActuatorSimTask()
            self.hvacActuator = HvacActuatorSimTask()
        else:
            # Emulated actuators via SenseHAT
            hueModule = import_module('programmingtheiot.cda.emulated.HumidifierEmulatorTask')
            hueClazz = getattr(hueModule, 'HumidifierEmulatorTask')
            self.humidifierActuator = hueClazz()

            hveModule = import_module('programmingtheiot.cda.emulated.HvacEmulatorTask')
            hveClazz = getattr(hveModule, 'HvacEmulatorTask')
            self.hvacActuator = hveClazz()

            # Optional: LED display emulator
            try:
                leModule = import_module('programmingtheiot.cda.emulated.LedDisplayEmulatorTask')
                leClazz = getattr(leModule, 'LedDisplayEmulatorTask')
                self.ledDisplayActuator = leClazz()
            except ModuleNotFoundError:
                logging.info("LED display emulator not found; skipping.")
