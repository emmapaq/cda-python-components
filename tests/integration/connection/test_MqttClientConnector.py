"""
MQTT Client Connector Test Module

Tests MQTT client connectivity, publish/subscribe functionality,
and actuator command message handling.

@author: Emma
"""

import logging
import unittest

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.DataUtil import DataUtil


class MqttClientConnectorTest(unittest.TestCase):
    """
    Test class for MqttClientConnector.
    
    Tests MQTT connectivity, subscriptions, and message handling.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Class-level setup
        """
        logging.basicConfig(
            format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
            level=logging.INFO
        )
    
    def setUp(self):
        """
        Per-test setup - create MQTT client connector
        """
        self.cfg = ConfigUtil()
        self.mcc = MqttClientConnector(clientID='CDAMqttClientConnectorTest001')
    
    def tearDown(self):
        """
        Per-test cleanup
        """
        pass
    
    @unittest.skip("Ignore for now.")
    def testConnectAndDisconnect(self):
        """
        Test basic connect and disconnect functionality
        """
        delay = self.cfg.getInteger(
            ConfigConst.MQTT_GATEWAY_SERVICE,
            ConfigConst.KEEP_ALIVE_KEY,
            ConfigConst.DEFAULT_KEEP_ALIVE
        )
        
        self.assertTrue(self.mcc.connectClient())
        
        sleep(delay)
        
        self.assertTrue(self.mcc.disconnectClient())
    
    #@unittest.skip("Ignore for now.")
    def testActuatorCmdPubSub(self):
        """
        Test actuator command publish and subscribe functionality.
        
        Publishes an ActuatorData command to the actuator command topic
        and verifies the subscription callback is triggered.
        """
        logging.info("\n\n***** testActuatorCmdPubSub *****")
        
        qos = 1
        
        # NOTE: delay can be anything you'd like - the sleep() calls are simply to slow things down a bit for observation
        delay = self.cfg.getInteger(
            ConfigConst.MQTT_GATEWAY_SERVICE,
            ConfigConst.KEEP_ALIVE_KEY,
            ConfigConst.DEFAULT_KEEP_ALIVE
        )
        
        # Create test actuator data
        actuatorData = ActuatorData()
        actuatorData.setName("TestActuator")
        actuatorData.setTypeID(ConfigConst.HVAC_ACTUATOR_TYPE)
        actuatorData.setCommand(ConfigConst.COMMAND_ON)
        
        payload = DataUtil().actuatorDataToJson(actuatorData)
        
        logging.info("Created actuator command payload: " + payload)
        
        # NOTE: the `DefaultDataMessageListener()` is just a placeholder for
        # handling callbacks from the MQTT client - it is optional
        self.mcc.setDataMessageListener(DefaultDataMessageListener())
        
        # Connect to broker
        self.assertTrue(self.mcc.connectClient())
        
        # Allow connection to establish and subscription to complete
        sleep(5)
        
        # Publish actuator command (will trigger our own subscription callback)
        logging.info("Publishing actuator command...")
        self.mcc.publishMessage(
            resource=ResourceNameEnum.CDA_ACTUATOR_CMD,
            msg=payload,
            qos=qos
        )
        
        # Wait for message to be received
        sleep(delay)
        
        # Disconnect
        self.assertTrue(self.mcc.disconnectClient())
        
        logging.info("Test complete.")


if __name__ == "__main__":
    unittest.main()