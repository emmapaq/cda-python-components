"""
MQTT Client Performance Test for CDA

Tests MQTT publish performance across different QoS levels.
Should be run with and without TLS encryption enabled.

CRITICAL: Only run against LOCAL brokers - DO NOT test against public servers!

@author: Emma
"""

import logging
import unittest
import time

from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.DataUtil import DataUtil


class MqttClientPerformanceTest(unittest.TestCase):
    """
    Performance test suite for MQTT client publish operations.
    
    Tests QoS 0, 1, and 2 performance with configurable TLS encryption.
    
    WARNING: Only run these tests against a LOCAL MQTT broker!
    """
    
    NS_IN_MILLIS = 1000000
    
    # NOTE: We'll use only 10,000 requests for MQTT
    MAX_TEST_RUNS = 10000
    
    @classmethod
    def setUpClass(cls):
        """
        Class-level setup - configure logging
        """
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.DEBUG
        )
        logging.info("=" * 70)
        logging.info("MQTT CLIENT PERFORMANCE TEST SUITE")
        logging.info("=" * 70)
        logging.warning("⚠️  ENSURE YOU ARE TESTING AGAINST A LOCAL BROKER ONLY! ⚠️")
        logging.info("=" * 70)
    
    def setUp(self):
        """
        Set up test fixture - create MQTT client for each test
        """
        self.mqttClient = MqttClientConnector(clientID='CDAMqttClientPerformanceTest001')
    
    def tearDown(self):
        """
        Clean up after each test
        """
        pass
    
    #@unittest.skip("Ignore for now.")
    def testConnectAndDisconnect(self):
        """
        Test connection and disconnection performance baseline
        """
        logging.info("\n" + "=" * 70)
        logging.info("TEST: Connect and Disconnect Performance")
        logging.info("=" * 70)
        
        startTime = time.time_ns()
        
        self.assertTrue(self.mqttClient.connectClient())
        
        # CRITICAL: Allow connection to fully establish
        # The Paho MQTT client uses loop_start() which runs in background thread
        # We need to give it time to complete the connection handshake
        time.sleep(2)
        
        self.assertTrue(self.mqttClient.disconnectClient())
        
        endTime = time.time_ns()
        elapsedMillis = (endTime - startTime) / self.NS_IN_MILLIS
        
        logging.info("Connect and Disconnect: " + str(elapsedMillis) + " ms")
        logging.info("=" * 70)
    
    #@unittest.skip("Ignore for now.")
    def testPublishQoS0(self):
        """
        Test publish performance with QoS 0 (at most once delivery)
        No acknowledgment - fastest but no delivery guarantee
        """
        logging.info("\n" + "=" * 70)
        logging.info("TEST: QoS 0 Performance (At Most Once)")
        logging.info("=" * 70)
        self._execTestPublish(self.MAX_TEST_RUNS, 0)
    
    #@unittest.skip("Ignore for now.")
    def testPublishQoS1(self):
        """
        Test publish performance with QoS 1 (at least once delivery)
        Single acknowledgment - balanced performance and reliability
        """
        logging.info("\n" + "=" * 70)
        logging.info("TEST: QoS 1 Performance (At Least Once)")
        logging.info("=" * 70)
        self._execTestPublish(self.MAX_TEST_RUNS, 1)
    
    #@unittest.skip("Ignore for now.")
    def testPublishQoS2(self):
        """
        Test publish performance with QoS 2 (exactly once delivery)
        Two-phase commit - slowest but guaranteed exactly-once delivery
        """
        logging.info("\n" + "=" * 70)
        logging.info("TEST: QoS 2 Performance (Exactly Once)")
        logging.info("=" * 70)
        self._execTestPublish(self.MAX_TEST_RUNS, 2)
    
    def _execTestPublish(self, maxTestRuns: int, qos: int):
        """
        Execute publish performance test for specified QoS level
        
        Args:
            maxTestRuns (int): Number of messages to publish
            qos (int): Quality of Service level (0, 1, or 2)
        """
        # Connect to broker
        logging.info(f"Connecting to broker...")
        self.assertTrue(self.mqttClient.connectClient())
        
        # CRITICAL: Allow connection to stabilize before publishing
        # This ensures the MQTT connection is fully established
        time.sleep(2)
        
        # Create test payload - realistic sensor data
        sensorData = SensorData()
        payload = DataUtil().sensorDataToJson(sensorData)
        
        logging.info(f"Publishing {maxTestRuns} messages with QoS {qos}...")
        logging.info(f"Payload size: {len(payload)} bytes")
        
        # Start timing
        startTime = time.time_ns()
        
        # Publish messages
        for seqNo in range(0, maxTestRuns):
            self.mqttClient.publishMessage(
                resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
                msg=payload,
                qos=qos
            )
        
        # End timing
        endTime = time.time_ns()
        elapsedMillis = (endTime - startTime) / self.NS_IN_MILLIS
        
        # Disconnect
        self.assertTrue(self.mqttClient.disconnectClient())
        
        # Calculate and log results
        avgMillisPerMsg = elapsedMillis / maxTestRuns
        messagesPerSecond = (maxTestRuns / elapsedMillis) * 1000
        
        logging.info("-" * 70)
        logging.info(f"RESULTS - QoS {qos}")
        logging.info("-" * 70)
        logging.info("Publish message - QoS " + str(qos) + 
                    " [" + str(maxTestRuns) + "]: " + 
                    str(elapsedMillis) + " ms")
        logging.info(f"Average time per message: {avgMillisPerMsg:.4f} ms")
        logging.info(f"Messages per second: {messagesPerSecond:.2f} msg/s")
        logging.info(f"Total throughput: {(len(payload) * messagesPerSecond / 1024):.2f} KB/s")
        logging.info("=" * 70)


if __name__ == "__main__":
    unittest.main()