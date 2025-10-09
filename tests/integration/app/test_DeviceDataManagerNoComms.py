import logging
import unittest
from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager

# Configure logging for tests
logging.basicConfig(
    format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
    level=logging.DEBUG
)

class TestDeviceDataManagerNoComms(unittest.TestCase):
    """
    Integration test for DeviceDataManager without MQTT or CoAP communications.
    """

    def setUp(self):
        logging.info("Setting up DeviceDataManager for test...")
        self.ddm = DeviceDataManager()

    def tearDown(self):
        logging.info("Tearing down DeviceDataManager test...")
        self.ddm.stopManager()

    def testStartAndStopManager(self):
        """
        Test that the DeviceDataManager starts and stops cleanly.
        """
        logging.info("Testing DeviceDataManager start and stop...")
        self.ddm.startManager()
        sleep(2)
        self.ddm.stopManager()
        self.assertTrue(True)  # If no exception occurs, test passes

    def testRunForFixedDuration(self):
        """
        Test DeviceDataManager run loop for a short duration (no forever loop).
        """
        logging.info("Testing DeviceDataManager running for short duration...")
        self.ddm.startManager()

        runForever = ConfigUtil().getBoolean(
            ConfigConst.CONSTRAINED_DEVICE, ConfigConst.RUN_FOREVER_KEY
        )

        if not runForever:
            sleep(5)
            self.ddm.stopManager()

        self.assertTrue(True)  # Pass if no errors or exceptions occur


if __name__ == '__main__':
    unittest.main()
