import unittest
import logging
from time import sleep

from programmingtheiot.cda.connection.AsyncCoapClientConnector import AsyncCoapClientConnector
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from programmingtheiot.data.DataUtil import DataUtil

class CoapAsyncClientConnectorTest(unittest.TestCase):
    """
    Test cases for AsyncCoapClientConnector using aiocoap.
    
    NOTE: These tests require a running CoAP server (GDA) on the configured host/port.
    Start your GDA with CoAP server enabled before running these tests.
    Use Wireshark with 'coap' filter to observe the message exchanges.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Set up test fixtures.
        """
        logging.basicConfig(
            format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
            level=logging.DEBUG)
        logging.info("Testing AsyncCoapClientConnector with aiocoap...")
    
    def setUp(self):
        """
        Set up each test - initialize the async CoAP client.
        """
        self.coapClient = AsyncCoapClientConnector()
        self.dataUtil = DataUtil()
        # Give the event loop time to start
        sleep(1)
    
    def tearDown(self):
        """
        Clean up after each test - stop the async CoAP client.
        """
        if self.coapClient:
            if hasattr(self.coapClient, 'stop'):
                self.coapClient.stop()
            sleep(1)
    
    @unittest.skip("Ignore for now.")
    def testDiscoveryRequest(self):
        """
        Test async DISCOVERY request to CoAP server.
        """
        logging.info("\n\n----- [testDiscoveryRequest] -----")
        
        success = self.coapClient.sendDiscoveryRequest(timeout=10)
        
        self.assertTrue(success, "Discovery request should return True")
        
        sleep(2)
        
        logging.info("Async discovery test completed")
    
    @unittest.skip("Ignore for now.")
    def testGetRequest(self):
        """
        Test async GET request for actuator command resource.
        """
        logging.info("\n\n----- [testGetRequest] -----")
        
        resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE
        success = self.coapClient.sendGetRequest(
            resource=resource,
            enableCON=True,
            timeout=10)
        
        self.assertTrue(success, "GET request should return True")
        
        sleep(2)
        
        logging.info("Async GET test completed")
    
    #@unittest.skip("Ignore for now.")
    def testPostSensorMessageCon(self):
        """
        Test async POST request with SensorData using CONFIRMABLE message.
        This test will send a CON POST request - observe in Wireshark.
        """
        logging.info("\n\n----- [testPostSensorMessageCon] -----")
        
        data = SensorData()
        jsonData = DataUtil().sensorDataToJson(data)
        
        self.coapClient.sendPostRequest(
            resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
            enableCON=True,
            payload=jsonData,
            timeout=5)
        
        sleep(2)
        
        logging.info("Async POST SensorMessage CON test completed")
    
    #@unittest.skip("Ignore for now.")
    def testPostSensorMessageNon(self):
        """
        Test async POST request with SensorData using NON-CONFIRMABLE message.
        This test will send a NON POST request - observe in Wireshark.
        """
        logging.info("\n\n----- [testPostSensorMessageNon] -----")
        
        data = SensorData()
        jsonData = DataUtil().sensorDataToJson(data)
        
        self.coapClient.sendPostRequest(
            resource=ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE,
            enableCON=False,
            payload=jsonData,
            timeout=5)
        
        sleep(2)
        
        logging.info("Async POST SensorMessage NON test completed")
    
    @unittest.skip("Ignore for now.")
    def testPostRequestActuatorCommand(self):
        """
        Test async POST request for actuator command resource.
        """
        logging.info("\n\n----- [testPostRequestActuatorCommand] -----")
        
        # Create ActuatorData
        actuatorData = ActuatorData()
        actuatorData.setName("HvacActuator")
        actuatorData.setCommand(ActuatorData.COMMAND_ON)
        actuatorData.setValue(22.5)
        
        jsonPayload = self.dataUtil.actuatorDataToJson(actuatorData)
        
        logging.info(f"Sending async ActuatorData POST:\n{jsonPayload}")
        
        resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE
        success = self.coapClient.sendPostRequest(
            resource=resource,
            enableCON=True,
            payload=jsonPayload,
            timeout=10)
        
        self.assertTrue(success, "POST request should return True")
        
        sleep(2)
        
        logging.info("Async POST actuator test completed")
    
    @unittest.skip("Ignore for now.")
    def testPostRequestSystemPerformance(self):
        """
        Test async POST request for system performance resource.
        """
        logging.info("\n\n----- [testPostRequestSystemPerformance] -----")
        
        # Create SystemPerformanceData
        sysPerfData = SystemPerformanceData()
        sysPerfData.setCpuUtilization(45.2)
        sysPerfData.setMemoryUtilization(62.8)
        sysPerfData.setDiskUtilization(25.1)
        
        jsonPayload = self.dataUtil.systemPerformanceDataToJson(sysPerfData)
        
        logging.info(f"Sending async SystemPerformanceData POST:\n{jsonPayload}")
        
        resource = ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE
        success = self.coapClient.sendPostRequest(
            resource=resource,
            enableCON=True,
            payload=jsonPayload,
            timeout=10)
        
        self.assertTrue(success, "POST request should return True")
        
        sleep(2)
        
        logging.info("Async POST system performance test completed")
    
    @unittest.skip("Ignore for now.")
    def testPutRequest(self):
        """
        Test async PUT request for actuator command resource.
        """
        logging.info("\n\n----- [testPutRequest] -----")
        
        # Create ActuatorData
        actuatorData = ActuatorData()
        actuatorData.setName("HumidifierActuator")
        actuatorData.setCommand(ActuatorData.COMMAND_ON)
        actuatorData.setValue(50.0)
        
        jsonPayload = self.dataUtil.actuatorDataToJson(actuatorData)
        
        logging.info(f"Sending async ActuatorData PUT:\n{jsonPayload}")
        
        resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE
        success = self.coapClient.sendPutRequest(
            resource=resource,
            enableCON=True,
            payload=jsonPayload,
            timeout=10)
        
        self.assertTrue(success, "PUT request should return True")
        
        sleep(2)
        
        logging.info("Async PUT test completed")
    
    @unittest.skip("Ignore for now.")
    def testDeleteRequest(self):
        """
        Test async DELETE request for actuator command resource.
        """
        logging.info("\n\n----- [testDeleteRequest] -----")
        
        resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE
        success = self.coapClient.sendDeleteRequest(
            resource=resource,
            enableCON=True,
            timeout=10)
        
        self.assertTrue(success, "DELETE request should return True")
        
        sleep(2)
        
        logging.info("Async DELETE test completed")
    
    @unittest.skip("Ignore for now.")
    def testPostRequestConfirmableVsNonConfirmable(self):
        """
        Test async POST request comparing CON vs NON modes.
        """
        logging.info("\n\n----- [testPostRequestConfirmableVsNonConfirmable] -----")
        
        actuatorData = ActuatorData()
        actuatorData.setName("LedActuator")
        actuatorData.setCommand(ActuatorData.COMMAND_ON)
        actuatorData.setValue(1.0)
        
        jsonPayload = self.dataUtil.actuatorDataToJson(actuatorData)
        resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE
        
        # Test with CON
        logging.info("Testing async POST with CONFIRMABLE...")
        success_con = self.coapClient.sendPostRequest(
            resource=resource,
            enableCON=True,
            payload=jsonPayload,
            timeout=10)
        
        self.assertTrue(success_con)
        sleep(2)
        
        # Test with NON
        logging.info("Testing async POST with NON-CONFIRMABLE...")
        actuatorData.setCommand(ActuatorData.COMMAND_OFF)
        jsonPayload = self.dataUtil.actuatorDataToJson(actuatorData)
        
        success_non = self.coapClient.sendPostRequest(
            resource=resource,
            enableCON=False,
            payload=jsonPayload,
            timeout=10)
        
        self.assertTrue(success_non)
        sleep(2)
        
        logging.info("Async CON vs NON test completed")

if __name__ == '__main__':
    unittest.main()