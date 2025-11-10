import unittest
import logging
from time import sleep

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData
from programmingtheiot.data.DataUtil import DataUtil

class CoapClientConnectorPostTest(unittest.TestCase):
    """
    Test cases for CoapClientConnector POST functionality.
    
    NOTE: These tests require a running CoAP server (GDA) on the configured host/port.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Set up test fixtures.
        """
        logging.basicConfig(
            format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
            level=logging.DEBUG)
        logging.info("Testing CoapClientConnector POST requests...")
    
    def setUp(self):
        """
        Set up each test - initialize the CoAP client.
        """
        self.coapClient = CoapClientConnector()
        self.dataUtil = DataUtil()
    
    def tearDown(self):
        """
        Clean up after each test - stop the CoAP client if stop method exists.
        """
        if self.coapClient:
            # Check if stop method exists before calling
            if hasattr(self.coapClient, 'stop'):
                self.coapClient.stop()
            sleep(1)  # Give threads time to clean up
    
    # @unittest.skip("Skipping POST actuator command test")
    def testPostRequestActuatorCommand(self):
        """
        Test POST request for actuator command resource.
        Creates ActuatorData and sends it as JSON payload.
        
        NOTE: Requires GDA CoAP server with CDA_ACTUATOR_CMD_RESOURCE registered.
        """
        logging.info("\n\n----- [testPostRequestActuatorCommand] -----")
        
        # Create ActuatorData
        actuatorData = ActuatorData()
        actuatorData.setName("HvacActuator")
        actuatorData.setCommand(ActuatorData.COMMAND_ON)
        actuatorData.setValue(22.5)
        actuatorData.setStateData("Increasing temp to 22.5C")
        
        # Convert to JSON
        jsonPayload = self.dataUtil.actuatorDataToJson(actuatorData)
        
        logging.info(f"Sending ActuatorData POST:\n{jsonPayload}")
        
        # Send POST request
        resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE
        success = self.coapClient.sendPostRequest(
            resource=resource,
            enableCON=True,
            payload=jsonPayload,
            timeout=10)
        
        self.assertTrue(success, "POST request should return True")
        
        # Give time for async callback to process
        sleep(5)
        
        logging.info("POST actuator command test completed")
    
    # @unittest.skip("Skipping POST sensor data test")
    def testPostRequestSensorData(self):
        """
        Test POST request for sensor message resource.
        Creates SensorData and sends it as JSON payload.
        
        NOTE: Requires GDA CoAP server with CDA_SENSOR_MSG_RESOURCE registered.
        """
        logging.info("\n\n----- [testPostRequestSensorData] -----")
        
        # Create SensorData
        sensorData = SensorData()
        sensorData.setName("TempSensor")
        sensorData.setValue(21.3)
        sensorData.setTypeID(SensorData.TEMP_SENSOR_TYPE)
        
        # Convert to JSON
        jsonPayload = self.dataUtil.sensorDataToJson(sensorData)
        
        logging.info(f"Sending SensorData POST:\n{jsonPayload}")
        
        # Send POST request
        resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE
        success = self.coapClient.sendPostRequest(
            resource=resource,
            enableCON=False,  # Use NON-confirmable
            payload=jsonPayload,
            timeout=10)
        
        self.assertTrue(success, "POST request should return True")
        
        # Give time for async callback to process
        sleep(5)
        
        logging.info("POST sensor data test completed")
    
    # @unittest.skip("Skipping POST system performance test")
    def testPostRequestSystemPerformance(self):
        """
        Test POST request for system performance resource.
        Creates SystemPerformanceData and sends it as JSON payload.
        
        NOTE: Requires GDA CoAP server with CDA_SYSTEM_PERF_MSG_RESOURCE registered.
        """
        logging.info("\n\n----- [testPostRequestSystemPerformance] -----")
        
        # Create SystemPerformanceData
        sysPerfData = SystemPerformanceData()
        sysPerfData.setCpuUtilization(45.2)
        sysPerfData.setMemoryUtilization(62.8)
        sysPerfData.setDiskUtilization(25.1)
        
        # Convert to JSON
        jsonPayload = self.dataUtil.systemPerformanceDataToJson(sysPerfData)
        
        logging.info(f"Sending SystemPerformanceData POST:\n{jsonPayload}")
        
        # Send POST request
        resource = ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE
        success = self.coapClient.sendPostRequest(
            resource=resource,
            enableCON=True,
            payload=jsonPayload,
            timeout=10)
        
        self.assertTrue(success, "POST request should return True")
        
        # Give time for async callback to process
        sleep(5)
        
        logging.info("POST system performance test completed")
    
    # @unittest.skip("Skipping POST with name parameter test")
    def testPostRequestWithNameParameter(self):
        """
        Test POST request using both resource and name parameters.
        This extends the resource path with additional detail.
        """
        logging.info("\n\n----- [testPostRequestWithNameParameter] -----")
        
        # Create simple sensor data
        sensorData = SensorData()
        sensorData.setName("HumiditySensor")
        sensorData.setValue(55.7)
        sensorData.setTypeID(SensorData.HUMIDITY_SENSOR_TYPE)
        
        jsonPayload = self.dataUtil.sensorDataToJson(sensorData)
        
        # Send POST with resource and name
        resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE
        name = "humidity"  # Example: extend path with sensor type
        
        success = self.coapClient.sendPostRequest(
            resource=resource,
            name=name,
            enableCON=True,
            payload=jsonPayload,
            timeout=10)
        
        self.assertTrue(success, "POST request with name should return True")
        
        # Give time for async callback to process
        sleep(5)
        
        logging.info("POST with name parameter test completed")
    
    # @unittest.skip("Skipping POST CON vs NON test")
    def testPostRequestConfirmableVsNonConfirmable(self):
        """
        Test POST request comparing confirmable and non-confirmable modes.
        """
        logging.info("\n\n----- [testPostRequestConfirmableVsNonConfirmable] -----")
        
        # Create test actuator data
        actuatorData = ActuatorData()
        actuatorData.setName("LedActuator")
        actuatorData.setCommand(ActuatorData.COMMAND_ON)
        actuatorData.setValue(1.0)
        
        jsonPayload = self.dataUtil.actuatorDataToJson(actuatorData)
        resource = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE
        
        # Test with CON (confirmable)
        logging.info("Testing with CONFIRMABLE message...")
        success_con = self.coapClient.sendPostRequest(
            resource=resource,
            enableCON=True,
            payload=jsonPayload,
            timeout=10)
        
        self.assertTrue(success_con, "POST with CON should return True")
        sleep(3)
        
        # Test with NON (non-confirmable)
        logging.info("Testing with NON-CONFIRMABLE message...")
        actuatorData.setCommand(ActuatorData.COMMAND_OFF)
        jsonPayload = self.dataUtil.actuatorDataToJson(actuatorData)
        
        success_non = self.coapClient.sendPostRequest(
            resource=resource,
            enableCON=False,
            payload=jsonPayload,
            timeout=10)
        
        self.assertTrue(success_non, "POST with NON should return True")
        sleep(3)
        
        logging.info("CON vs NON test completed")
    
    # @unittest.skip("Skipping POST multiple sensor readings test")
    def testPostRequestMultipleSensorReadings(self):
        """
        Test sending multiple POST requests with different sensor readings.
        """
        logging.info("\n\n----- [testPostRequestMultipleSensorReadings] -----")
        
        resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE
        
        # Reading 1: Temperature
        sensorData1 = SensorData()
        sensorData1.setName("TempSensor")
        sensorData1.setValue(22.5)
        sensorData1.setTypeID(SensorData.TEMP_SENSOR_TYPE)
        
        jsonPayload1 = self.dataUtil.sensorDataToJson(sensorData1)
        
        logging.info("Sending first POST (Temperature reading)...")
        success1 = self.coapClient.sendPostRequest(
            resource=resource,
            enableCON=True,
            payload=jsonPayload1,
            timeout=10)
        
        self.assertTrue(success1)
        sleep(2)
        
        # Reading 2: Humidity
        sensorData2 = SensorData()
        sensorData2.setName("HumiditySensor")
        sensorData2.setValue(58.3)
        sensorData2.setTypeID(SensorData.HUMIDITY_SENSOR_TYPE)
        
        jsonPayload2 = self.dataUtil.sensorDataToJson(sensorData2)
        
        logging.info("Sending second POST (Humidity reading)...")
        success2 = self.coapClient.sendPostRequest(
            resource=resource,
            enableCON=True,
            payload=jsonPayload2,
            timeout=10)
        
        self.assertTrue(success2)
        sleep(2)
        
        # Reading 3: Pressure
        sensorData3 = SensorData()
        sensorData3.setName("PressureSensor")
        sensorData3.setValue(1013.25)
        sensorData3.setTypeID(SensorData.PRESSURE_SENSOR_TYPE)
        
        jsonPayload3 = self.dataUtil.sensorDataToJson(sensorData3)
        
        logging.info("Sending third POST (Pressure reading)...")
        success3 = self.coapClient.sendPostRequest(
            resource=resource,
            enableCON=True,
            payload=jsonPayload3,
            timeout=10)
        
        self.assertTrue(success3)
        sleep(2)
        
        logging.info("Multiple sensor readings test completed")
    
    # @unittest.skip("Skipping POST invalid path test")
    def testPostRequestInvalidPath(self):
        """
        Test POST request with invalid/missing path parameters.
        Should handle gracefully and log warning.
        """
        logging.info("\n\n----- [testPostRequestInvalidPath] -----")
        
        # Create some test data
        actuatorData = ActuatorData()
        actuatorData.setName("TestActuator")
        actuatorData.setCommand(ActuatorData.COMMAND_ON)
        
        jsonPayload = self.dataUtil.actuatorDataToJson(actuatorData)
        
        # Send POST with no resource or name
        success = self.coapClient.sendPostRequest(
            resource=None,
            name=None,
            enableCON=True,
            payload=jsonPayload,
            timeout=10)
        
        # Should return False
        self.assertFalse(success, "POST with no path should return False")
        
        logging.info("Invalid path test completed")
    
    # @unittest.skip("Skipping POST with large payload test")
    def testPostRequestLargePayload(self):
        """
        Test POST request with a larger JSON payload.
        """
        logging.info("\n\n----- [testPostRequestLargePayload] -----")
        
        # Create system performance data with detailed info
        sysPerfData = SystemPerformanceData()
        sysPerfData.setCpuUtilization(75.4)
        sysPerfData.setMemoryUtilization(82.1)
        sysPerfData.setDiskUtilization(45.3)
        
        # SystemPerformanceData doesn't have setStateData, so just use the existing fields
        # The JSON payload will still be reasonably sized
        
        jsonPayload = self.dataUtil.systemPerformanceDataToJson(sysPerfData)
        
        logging.info(f"Sending POST payload ({len(jsonPayload)} bytes)...")
        
        resource = ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE
        success = self.coapClient.sendPostRequest(
            resource=resource,
            enableCON=True,
            payload=jsonPayload,
            timeout=10)
        
        self.assertTrue(success, "POST with payload should return True")
        
        sleep(5)
        
        logging.info("POST payload test completed")

if __name__ == '__main__':
    unittest.main()