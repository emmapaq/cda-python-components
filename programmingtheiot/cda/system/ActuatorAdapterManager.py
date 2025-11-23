#####
#
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
#
# You may find it more helpful to your design to adjust the
# functionality, constants and interfaces (if there are any)
# provided within in order to meet the needs of your specific
# Programming the Internet of Things project.
#

import logging

from importlib import import_module

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask


class ActuatorAdapterManager(object):
    """
    Manager for actuator adapters.
    
    Manages all actuator instances (HVAC, Humidifier, LED, etc.) and routes
    actuator commands to the appropriate actuator based on type.
    """
    
    def __init__(self, useEmulator: bool = False):
        """
        Constructor for ActuatorAdapterManager.
        
        Initializes all actuator simulators based on configuration.
        
        Args:
            useEmulator (bool): If True, uses hardware emulator; otherwise uses simulators
        """
        self.configUtil = ConfigUtil()
        self.dataMsgListener = None
        self.useEmulator = useEmulator
        
        # Load actuator configuration
        self.enableHvacActuator = \
            self.configUtil.getBoolean(
                ConfigConst.ACTUATOR_SIMULATOR,
                ConfigConst.ENABLE_HVAC_ACTUATOR_KEY
            )
        
        self.enableHumidifierActuator = \
            self.configUtil.getBoolean(
                ConfigConst.ACTUATOR_SIMULATOR,
                ConfigConst.ENABLE_HUMIDIFIER_ACTUATOR_KEY
            )
        
        self.enableLedActuator = \
            self.configUtil.getBoolean(
                ConfigConst.ACTUATOR_SIMULATOR,
                ConfigConst.ENABLE_LED_ACTUATOR_KEY
            )
        
        # Initialize actuators
        self.hvacActuator = None
        self.humidifierActuator = None
        self.ledActuator = None
        
        if self.enableHvacActuator:
            logging.info("HVAC actuator enabled. Initializing...")
            self.hvacActuator = HvacActuatorSimTask()
            logging.info("HVAC actuator initialized.")
        
        if self.enableHumidifierActuator:
            logging.info("Humidifier actuator enabled. Initializing...")
            self.humidifierActuator = HumidifierActuatorSimTask()
            logging.info("Humidifier actuator initialized.")
        
        if self.enableLedActuator:
            logging.info("LED actuator enabled. Initializing...")
            # TODO: Initialize LED actuator when available
            logging.info("LED actuator initialized.")
        
        logging.info("ActuatorAdapterManager initialized.")
    
    def sendActuatorCommand(self, data: ActuatorData) -> ActuatorData:
        """
        Sends an actuator command to the appropriate actuator.
        
        Routes the command to the correct actuator based on the actuator type ID,
        executes the command, and returns the actuator's response.
        
        Args:
            data (ActuatorData): The actuator command to execute
            
        Returns:
            ActuatorData: The actuator response with updated state, or None if failed
        """
        if not data:
            logging.warning("Actuator command is None. Ignoring.")
            return None
        
        logging.info("Actuator command received. Processing...")
        logging.debug(f"Actuator Type: {data.getTypeID()}, Command: {data.getCommand()}")
        
        # Get actuator type
        actuatorType = data.getTypeID()
        response = None
        
        # Route to appropriate actuator based on type
        if actuatorType == ConfigConst.HVAC_ACTUATOR_TYPE:
            if self.hvacActuator:
                logging.info("Routing command to HVAC actuator...")
                response = self.hvacActuator.updateActuator(data)
            else:
                logging.warning("HVAC actuator not initialized or disabled.")
        
        elif actuatorType == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE:
            if self.humidifierActuator:
                logging.info("Routing command to Humidifier actuator...")
                response = self.humidifierActuator.updateActuator(data)
            else:
                logging.warning("Humidifier actuator not initialized or disabled.")
        
        elif actuatorType == ConfigConst.LED_ACTUATOR_TYPE:
            if self.ledActuator:
                logging.info("Routing command to LED actuator...")
                response = self.ledActuator.updateActuator(data)
            else:
                logging.warning("LED actuator not initialized or disabled.")
        
        else:
            logging.warning(f"Unknown actuator type: {actuatorType}. Ignoring command.")
        
        # Notify listener if response received
        if response and self.dataMsgListener:
            logging.info("Notifying listener of actuator response...")
            self.dataMsgListener.handleActuatorCommandResponse(response)
        
        return response
    
    def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
        """
        Sets the data message listener for actuator responses.
        
        Args:
            listener (IDataMessageListener): The listener to notify of actuator responses
            
        Returns:
            bool: True if listener was set successfully
        """
        if listener:
            self.dataMsgListener = listener
            logging.info("Data message listener set for ActuatorAdapterManager.")
            return True
        else:
            logging.warning("No data message listener provided.")
            return False