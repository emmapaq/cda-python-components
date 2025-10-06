import logging
from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

from pisense import SenseHAT

class HumidifierEmulatorTask(BaseActuatorSimTask):
    def __init__(self):
        super(HumidifierEmulatorTask, self).__init__(
            name=ConfigConst.HUMIDIFIER_ACTUATOR_NAME,
            typeID=ConfigConst.HUMIDIFIER_ACTUATOR_TYPE,
            simpleName="HUMIDIFIER"
        )
        enableEmulation = ConfigUtil().getBoolean(
            ConfigConst.CONSTRAINED_DEVICE,
            ConfigConst.ENABLE_EMULATOR_KEY
        )
        self.sh = SenseHAT(emulate=enableEmulation)

    def _activateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        if self.sh.screen:
            msg = self.getSimpleName() + ' ON: ' + str(val) + 'C'
            self.sh.screen.scroll_text(msg)
            return 0
        else:
            logging.warning("No SenseHAT LED screen instance to write.")
            return -1

    def _deactivateActuator(self, val: float = ConfigConst.DEFAULT_VAL, stateData: str = None) -> int:
        if self.sh.screen:
            msg = self.getSimpleName() + ' OFF'
            self.sh.screen.scroll_text(msg)
            sleep(5)
            self.sh.screen.clear()
            return 0
        else:
            logging.warning("No SenseHAT LED screen instance to clear / close.")
            return -1
