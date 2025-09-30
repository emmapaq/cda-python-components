import logging
from programmingtheiot.data.ActuatorData import ActuatorData

class LedActuatorSimTask:
    def __init__(self):
        logging.info("LED Actuator Simulator initialized")

    def updateActuator(self, data: ActuatorData) -> ActuatorData:
        logging.info("LED Actuator Simulator received command: %s", str(data))
        # Simply return the same data for testing purposes
        return data
