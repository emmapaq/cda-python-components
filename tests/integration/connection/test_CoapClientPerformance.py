"""
CoAP Client Performance Test for CDA

Tests CoAP POST performance using both CON (confirmed) and NON (non-confirmed) messages.

NOTE: Due to CoAPthon3 threading limitations, this test cannot be run reliably.
See class documentation for details.

@author: Emma
"""

import logging
import unittest
import time

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.DataUtil import DataUtil


class CoapClientPerformanceTest(unittest.TestCase):
    """
    Performance test suite for CoAP client POST operations.
    
    WARNING: CoAPthon3 has threading issues - these tests are skipped.
    """
    
    NS_IN_MILLIS = 1000000
    
    # NOTE: We'll use only 10,000 requests for CoAP
    MAX_TEST_RUNS = 10000
    
    @classmethod
    def setUpClass(cls):
        logging.disable(level=logging.WARNING)
    
    def setUp(self):
        self.coapClient = CoapClientConnector()
    
    def tearDown(self):
        if self.coapClient:
            try:
                self.coapClient.stop()
            except:
                pass
    
    @unittest.skip("CoAPthon3 threading issues - library limitation")
    def testPostRequestCon(self):
        print("Testing POST - CON")
        self._execTestPost(self.MAX_TEST_RUNS, True)
    
    @unittest.skip("CoAPthon3 threading issues - library limitation")
    def testPostRequestNon(self):
        print("Testing POST - NON")
        self._execTestPost(self.MAX_TEST_RUNS, False)
    
    def _execTestPost(self, maxTestRuns: int, useCon: bool):
        sensorData = SensorData()
        payload = DataUtil().sensorDataToJson(sensorData)
        
        startTime = time.time_ns()
        
        for seqNo in range(0, maxTestRuns):
            self.coapClient.sendPostRequest(
                resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
                enableCON=useCon,
                payload=payload
            )
        
        endTime = time.time_ns()
        elapsedMillis = (endTime - startTime) / self.NS_IN_MILLIS
        
        print("POST message - useCON = " + str(useCon) + " [" + str(maxTestRuns) + "]: " + str(elapsedMillis) + " ms")


if __name__ == "__main__":
    unittest.main()