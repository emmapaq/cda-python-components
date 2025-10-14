"""
MQTT Client Connector Integration Test Module

Integration tests for MqttClientConnector functionality.
These tests require a running MQTT broker.
"""

import logging
import unittest
from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.DataUtil import DataUtil


class MqttClientConnectorTest(unittest.TestCase):
    """
    Integration test cases for MqttClientConnector.
    
    NOTE: These tests require a running MQTT broker accessible
    at the host and port specified in the configuration file.
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures for the entire test class."""
        logging.basicConfig(
            format='%(asctime)s:%(module)s:%(levelname)s:%(message)s',
            level=logging.INFO
        )
        logging.info("Testing MqttClientConnector class...")
        
        cls.cfg = ConfigUtil()
        cls.mcc = MqttClientConnector()
        cls.dataUtil = DataUtil()
        cls.listener = DefaultDataMessageListener()
        cls.mcc.setDataMessageListener(cls.listener)
    
    def setUp(self):
        """Set up for each test method."""
        pass
    
    def tearDown(self):
        """Tear down after each test method."""
        pass
    
    @unittest.skip("Ignore for now.")
    def testConnectAndDisconnect(self):
        """Test basic connect and disconnect functionality."""
        logging.info("Testing connect and disconnect...")
        
        connectResult = self.mcc.connectClient()
        self.assertTrue(connectResult, "Failed to connect to MQTT broker")
        sleep(5)
        
        disconnectResult = self.mcc.disconnectClient()
        self.assertTrue(disconnectResult, "Failed to disconnect from MQTT broker")
        
        logging.info("Connect and disconnect test completed successfully")
    
    @unittest.skip("Ignore for now.")
    def testConnectAndCDAManagementStatusPubSub(self):
        """Test publish/subscribe to CDA management status topic."""
        logging.info("Testing CDA Management Status Pub/Sub...")
        
        qos = 1
        self.mcc.connectClient()
        sleep(2)
        
        self.mcc.subscribeToTopic(
            resource=ResourceNameEnum.CDA_MGMT_STATUS,
            qos=qos
        )
        sleep(2)
        
        actuatorData = ActuatorData()
        actuatorData.setName("MgmtStatusTest")
        actuatorData.setCommand(ActuatorData.COMMAND_ON)
        actuatorData.setValue(100.0)
        
        payload = self.dataUtil.actuatorDataToJson(actuatorData)
        
        self.mcc.publishMessage(
            resource=ResourceNameEnum.CDA_MGMT_STATUS,
            msg=payload,
            qos=qos
        )
        
        sleep(5)
        
        self.mcc.unsubscribeFromTopic(
            resource=ResourceNameEnum.CDA_MGMT_STATUS
        )
        sleep(2)
        
        self.mcc.disconnectClient()
        logging.info("CDA Management Status Pub/Sub test completed")
    
    def testActuatorCmdPubSub(self):
        """Test publish/subscribe to actuator command topic."""
        logging.info("Testing Actuator Command Pub/Sub...")
        
        qos = ConfigConst.DEFAULT_QOS
        delay = self.cfg.getInteger(
            ConfigConst.MQTT_GATEWAY_SERVICE,
            ConfigConst.KEEP_ALIVE_KEY,
            ConfigConst.DEFAULT_KEEP_ALIVE
        )
        
        self.mcc.connectClient()
        sleep(2)
        
        self.mcc.subscribeToTopic(
            resource=ResourceNameEnum.CDA_ACTUATOR_CMD,
            qos=qos
        )
        sleep(2)
        
        actuatorData = ActuatorData()
        actuatorData.setName("ActuatorCommandTest")
        actuatorData.setTypeID(ActuatorData.HVAC_ACTUATOR_TYPE)
        actuatorData.setCommand(ActuatorData.COMMAND_ON)
        actuatorData.setValue(22.5)
        actuatorData.setStateData("Test actuator command from integration test")
        
        payload = self.dataUtil.actuatorDataToJson(actuatorData)
        self.mcc.publishMessage(
            resource=ResourceNameEnum.CDA_ACTUATOR_CMD,
            msg=payload,
            qos=qos
        )
        
        sleep(delay)
        
        for i in range(3):
            actuatorData.setValue(20.0 + i)
            actuatorData.setStateData(f"Test message {i+1}")
            payload = self.dataUtil.actuatorDataToJson(actuatorData)
            
            self.mcc.publishMessage(
                resource=ResourceNameEnum.CDA_ACTUATOR_CMD,
                msg=payload,
                qos=qos
            )
            sleep(2)
        
        sleep(5)
        
        self.mcc.unsubscribeFromTopic(
            resource=ResourceNameEnum.CDA_ACTUATOR_CMD
        )
        sleep(2)
        
        self.mcc.disconnectClient()
        logging.info("Actuator Command Pub/Sub test completed successfully")
    
    @unittest.skip("Ignore for now.")
    def testPublishMultipleMessages(self):
        """Test publishing multiple messages in sequence."""
        logging.info("Testing multiple message publishing...")
        
        qos = 1
        messageCount = 10
        
        self.mcc.connectClient()
        sleep(2)
        
        self.mcc.subscribeToTopic(
            resource=ResourceNameEnum.CDA_ACTUATOR_CMD,
            qos=qos
        )
        sleep(2)
        
        for i in range(messageCount):
            actuatorData = ActuatorData()
            actuatorData.setName(f"TestMessage_{i}")
            actuatorData.setValue(float(i * 10))
            
            payload = self.dataUtil.actuatorDataToJson(actuatorData)
            
            self.mcc.publishMessage(
                resource=ResourceNameEnum.CDA_ACTUATOR_CMD,
                msg=payload,
                qos=qos
            )
            sleep(0.5)
        
        sleep(5)
        
        self.mcc.unsubscribeFromTopic(
            resource=ResourceNameEnum.CDA_ACTUATOR_CMD
        )
        self.mcc.disconnectClient()
        logging.info(f"Successfully published {messageCount} messages")
    
    @unittest.skip("Ignore for now.")
    def testSubscribeMultipleTopics(self):
        """Test subscribing to multiple topics simultaneously."""
        logging.info("Testing multiple topic subscriptions...")
        
        qos = 1
        self.mcc.connectClient()
        sleep(2)
        
        topics = [
            ResourceNameEnum.CDA_ACTUATOR_CMD,
            ResourceNameEnum.CDA_SENSOR_DATA,
            ResourceNameEnum.CDA_MGMT_STATUS
        ]
        
        for topic in topics:
            self.mcc.subscribeToTopic(resource=topic, qos=qos)
            sleep(1)
        
        for topic in topics:
            actuatorData = ActuatorData()
            actuatorData.setName(f"TestFor_{topic.name}")
            actuatorData.setValue(50.0)
            
            payload = self.dataUtil.actuatorDataToJson(actuatorData)
            self.mcc.publishMessage(resource=topic, msg=payload, qos=qos)
            sleep(2)
        
        sleep(5)
        
        for topic in topics:
            self.mcc.unsubscribeFromTopic(resource=topic)
            sleep(1)
        
        self.mcc.disconnectClient()
        logging.info("Multiple topic subscription test completed")


if __name__ == "__main__":
    unittest.main()
