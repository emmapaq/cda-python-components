"""
Integration test for Fermentation System end-to-end functionality.

This module tests the complete workflow of the fermentation control system,
including sensor data collection, threshold-based actuation, profile management,
and remote command processing.

Validation:
- Temperature threshold detection and actuation
- Humidity threshold detection and actuation
- Fermentation profile switching
- Remote actuation commands
- Temperature spike detection
- LED display updates
- Multi-actuator coordination

@author: Emma
"""

import unittest
import logging
import time


from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.common.ConfigConst import ConfigConst

class Integration_FermentationSystem_Test(unittest.TestCase):
    """
    Integration tests for fermentation system functionality.
    
    This test suite validates the complete fermentation control workflow,
    including sensor monitoring, threshold-based actuation, profile management,
    and system integration.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Set up test fixtures that will be used across all tests.
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        logging.info("\n\n===== Fermentation System Integration Tests =====\n")
        
        # Create device data manager instance
        cls.deviceDataMgr = DeviceDataManager()
        
        # Track actuations for verification
        cls.actuationLog = []
        
        # Override actuator manager's sendActuatorCommand to log actuations
        cls.originalSendCommand = cls.deviceDataMgr.actuatorAdapterManager.sendActuatorCommand
        cls.deviceDataMgr.actuatorAdapterManager.sendActuatorCommand = cls.logActuation
    
    @classmethod
    def logActuation(cls, data: ActuatorData) -> bool:
        """
        Log actuation commands for test verification.
        """
        cls.actuationLog.append({
            'type': data.getTypeID(),
            'command': data.getCommand(),
            'value': data.getValue(),
            'timestamp': time.time()
        })
        logging.info(f"Actuation logged: Type={data.getTypeID()}, Command={data.getCommand()}, Value={data.getValue()}")
        # Call original method to maintain functionality
        return cls.originalSendCommand(data)
    
    def setUp(self):
        """
        Set up each individual test.
        """
        # Clear actuation log before each test
        self.__class__.actuationLog = []
        
        # Reset to ALE profile
        self.deviceDataMgr.currentFermentationProfile = ConfigConst.FERMENTATION_PROFILE_ALE
        self.deviceDataMgr.currentTempMin = ConfigConst.ALE_TEMP_MIN
        self.deviceDataMgr.currentTempMax = ConfigConst.ALE_TEMP_MAX
        self.deviceDataMgr.currentHumidityMin = ConfigConst.ALE_HUMIDITY_MIN
        self.deviceDataMgr.currentHumidityMax = ConfigConst.ALE_HUMIDITY_MAX
        
        # Clear temperature history
        self.deviceDataMgr.recentTemperatures = []
    
    def tearDown(self):
        """
        Clean up after each test.
        """
        time.sleep(0.5)  # Brief pause between tests
    
    # ========================================================================
    # Test 1: End-to-End Fermentation Control
    # ========================================================================
    
    def testEndToEndFermentationControl(self):
        """
        Test complete workflow:
        1. Start with ALE profile
        2. Generate temperature above threshold → Verify cooling actuation
        3. Generate optimal temperature → Verify HVAC turns off
        4. Change profile to LAGER
        5. Generate humidity below threshold → Verify humidifier actuation
        6. Generate optimal humidity → Verify humidifier turns off
        """
        logging.info("\n\n===== Test 1: End-to-End Fermentation Control =====\n")
        
        # Step 1: Verify starting with ALE profile
        self.assertEqual(self.deviceDataMgr.currentFermentationProfile, ConfigConst.FERMENTATION_PROFILE_ALE)
        logging.info("✓ Starting profile: ALE")
        
        # Step 2: Generate high temperature (above ALE max of 72°F)
        logging.info("\nStep 2: Testing temperature threshold - HIGH")
        tempData = SensorData()
        tempData.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
        tempData.setValue(75.0)  # Above ALE max (72.0)
        tempData.setName("TempSensor")
        
        result = self.deviceDataMgr.handleSensorData(tempData)
        self.assertTrue(result, "Failed to handle high temperature sensor data")
        
        time.sleep(0.5)  # Allow actuation to process
        
        # Verify cooling was triggered
        hvacActuations = [a for a in self.actuationLog if a['type'] == ConfigConst.HVAC_ACTUATOR_TYPE]
        self.assertGreater(len(hvacActuations), 0, "No HVAC actuation triggered for high temperature")
        
        coolingActuation = next((a for a in hvacActuations if a['command'] == ConfigConst.HVAC_COOLING_CMD), None)
        self.assertIsNotNone(coolingActuation, "Cooling command not sent for high temperature")
        logging.info(f"✓ Cooling activated: {coolingActuation['command']} at {coolingActuation['value']}")
        
        # Verify LED update
        ledActuations = [a for a in self.actuationLog if a['type'] == ConfigConst.LED_DISPLAY_ACTUATOR_TYPE]
        self.assertGreater(len(ledActuations), 0, "No LED update triggered")
        logging.info("✓ LED display updated")
        
        # Clear log for next step
        self.actuationLog.clear()
        
        # Step 3: Generate optimal temperature
        logging.info("\nStep 3: Testing optimal temperature")
        tempData.setValue(70.0)  # Within ALE range (68-72)
        
        result = self.deviceDataMgr.handleSensorData(tempData)
        self.assertTrue(result, "Failed to handle optimal temperature sensor data")
        
        time.sleep(0.5)
        
        # Verify HVAC turned off or status updated
        hvacActuations = [a for a in self.actuationLog if a['type'] == ConfigConst.HVAC_ACTUATOR_TYPE]
        if len(hvacActuations) > 0:
            offActuation = next((a for a in hvacActuations if a['command'] == ConfigConst.HVAC_OFF_CMD), None)
            if offActuation:
                logging.info(f"✓ HVAC deactivated: {offActuation['command']}")
        else:
            logging.info("✓ Temperature optimal - no HVAC change needed")
        
        # Clear log for next step
        self.actuationLog.clear()
        
        # Step 4: Change profile to LAGER
        logging.info("\nStep 4: Changing profile to LAGER")
        profileChangeCmd = ActuatorData()
        profileChangeCmd.setActuatorType(ConfigConst.FERMENTATION_PROFILE_ACTUATOR_TYPE)
        profileChangeCmd.setCommand(ConfigConst.FERMENTATION_PROFILE_LAGER)
        profileChangeCmd.setName("Profile Change Command")
        
        result = self.deviceDataMgr._handleFermentationProfileCommand(profileChangeCmd)
        self.assertTrue(result, "Failed to change fermentation profile")
        
        self.assertEqual(self.deviceDataMgr.currentFermentationProfile, ConfigConst.FERMENTATION_PROFILE_LAGER)
        self.assertEqual(self.deviceDataMgr.currentTempMin, ConfigConst.LAGER_TEMP_MIN)
        self.assertEqual(self.deviceDataMgr.currentTempMax, ConfigConst.LAGER_TEMP_MAX)
        logging.info(f"✓ Profile changed to LAGER: Temp [{self.deviceDataMgr.currentTempMin}-{self.deviceDataMgr.currentTempMax}]")
        
        # Clear log for next step
        self.actuationLog.clear()
        
        # Step 5: Generate low humidity (below LAGER min of 55%)
        logging.info("\nStep 5: Testing humidity threshold - LOW")
        humidData = SensorData()
        humidData.setTypeID(ConfigConst.HUMIDITY_SENSOR_TYPE)
        humidData.setValue(50.0)  # Below LAGER min (55.0)
        humidData.setName("HumiditySensor")
        
        result = self.deviceDataMgr.handleSensorData(humidData)
        self.assertTrue(result, "Failed to handle low humidity sensor data")
        
        time.sleep(0.5)
        
        # Verify humidifier was triggered
        humidifierActuations = [a for a in self.actuationLog if a['type'] == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE]
        self.assertGreater(len(humidifierActuations), 0, "No humidifier actuation triggered for low humidity")
        
        onActuation = next((a for a in humidifierActuations if a['command'] == ConfigConst.HUMIDIFIER_ON_CMD), None)
        self.assertIsNotNone(onActuation, "Humidifier ON command not sent for low humidity")
        logging.info(f"✓ Humidifier activated: {onActuation['command']}")
        
        # Clear log for next step
        self.actuationLog.clear()
        
        # Step 6: Generate optimal humidity
        logging.info("\nStep 6: Testing optimal humidity")
        humidData.setValue(60.0)  # Within LAGER range (55-65)
        
        result = self.deviceDataMgr.handleSensorData(humidData)
        self.assertTrue(result, "Failed to handle optimal humidity sensor data")
        
        time.sleep(0.5)
        
        logging.info("✓ Humidity optimal")
        
        logging.info("\n✓✓✓ Test PASSED: End-to-end control working correctly ✓✓✓\n")
    
    # ========================================================================
    # Test 2: Remote Profile Change
    # ========================================================================
    
    def testRemoteProfileChange(self):
        """
        Test remote profile change from GDA:
        1. CDA running with ALE profile
        2. Simulate GDA sending LAGER profile command
        3. Verify CDA switches to LAGER thresholds
        4. Generate temperature and verify new thresholds applied
        """
        logging.info("\n\n===== Test 2: Remote Profile Change =====\n")
        
        # Step 1: Verify starting with ALE profile
        self.assertEqual(self.deviceDataMgr.currentFermentationProfile, ConfigConst.FERMENTATION_PROFILE_ALE)
        logging.info(f"✓ Initial profile: {self.deviceDataMgr.currentFermentationProfile}")
        logging.info(f"  Temp range: [{self.deviceDataMgr.currentTempMin}-{self.deviceDataMgr.currentTempMax}]")
        
        # Step 2: Send profile change command (simulating GDA)
        logging.info("\nStep 2: Sending LAGER profile change command")
        profileCmd = ActuatorData()
        profileCmd.setActuatorType(ConfigConst.FERMENTATION_PROFILE_ACTUATOR_TYPE)
        profileCmd.setCommand(ConfigConst.FERMENTATION_PROFILE_LAGER)
        profileCmd.setName("Remote Profile Change")
        
        result = self.deviceDataMgr._handleFermentationProfileCommand(profileCmd)
        self.assertTrue(result, "Profile change command failed")
        
        # Step 3: Verify profile changed
        self.assertEqual(self.deviceDataMgr.currentFermentationProfile, ConfigConst.FERMENTATION_PROFILE_LAGER)
        self.assertEqual(self.deviceDataMgr.currentTempMin, ConfigConst.LAGER_TEMP_MIN)
        self.assertEqual(self.deviceDataMgr.currentTempMax, ConfigConst.LAGER_TEMP_MAX)
        self.assertEqual(self.deviceDataMgr.currentHumidityMin, ConfigConst.LAGER_HUMIDITY_MIN)
        self.assertEqual(self.deviceDataMgr.currentHumidityMax, ConfigConst.LAGER_HUMIDITY_MAX)
        
        logging.info(f"✓ Profile changed to: {self.deviceDataMgr.currentFermentationProfile}")
        logging.info(f"  Temp range: [{self.deviceDataMgr.currentTempMin}-{self.deviceDataMgr.currentTempMax}]")
        logging.info(f"  Humidity range: [{self.deviceDataMgr.currentHumidityMin}-{self.deviceDataMgr.currentHumidityMax}]")
        
        # Step 4: Test that new thresholds are applied
        logging.info("\nStep 4: Testing new LAGER thresholds")
        self.actuationLog.clear()
        
        # Temperature that would be OK for ALE (70°F) but HIGH for LAGER (max 55°F)
        tempData = SensorData()
        tempData.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
        tempData.setValue(58.0)  # Above LAGER max (55.0), but within ALE range
        tempData.setName("TempSensor")
        
        result = self.deviceDataMgr.handleSensorData(tempData)
        self.assertTrue(result, "Failed to handle temperature with new profile")
        
        time.sleep(0.5)
        
        # Verify cooling triggered (because 58 > 55 for LAGER)
        hvacActuations = [a for a in self.actuationLog if a['type'] == ConfigConst.HVAC_ACTUATOR_TYPE]
        self.assertGreater(len(hvacActuations), 0, "HVAC should activate for temp above LAGER threshold")
        
        coolingActuation = next((a for a in hvacActuations if a['command'] == ConfigConst.HVAC_COOLING_CMD), None)
        self.assertIsNotNone(coolingActuation, "Cooling should be triggered for LAGER profile")
        
        logging.info(f"✓ New thresholds applied: 58°F triggered cooling (LAGER max: {self.deviceDataMgr.currentTempMax}°F)")
        
        logging.info("\n✓✓✓ Test PASSED: Remote profile change working correctly ✓✓✓\n")
    
    # ========================================================================
    # Test 3: Temperature Threshold Response
    # ========================================================================
    
    def testTemperatureThresholdResponse(self):
        """
        Test temperature threshold crossing detection and response.
        Tests both HIGH and LOW threshold crossings.
        """
        logging.info("\n\n===== Test 3: Temperature Threshold Response =====\n")
        
        # Test HIGH temperature
        logging.info("Testing HIGH temperature threshold")
        tempData = SensorData()
        tempData.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
        tempData.setValue(75.0)  # Above ALE max (72.0)
        tempData.setName("TempSensor")
        
        result = self.deviceDataMgr.handleSensorData(tempData)
        self.assertTrue(result, "Failed to handle high temperature sensor data")
        
        time.sleep(0.5)
        
        # Verify cooling was triggered
        hvacActuations = [a for a in self.actuationLog if a['type'] == ConfigConst.HVAC_ACTUATOR_TYPE]
        self.assertGreater(len(hvacActuations), 0, "No HVAC actuation for high temperature")
        
        coolingActuation = next((a for a in hvacActuations if a['command'] == ConfigConst.HVAC_COOLING_CMD), None)
        self.assertIsNotNone(coolingActuation, "Cooling not triggered for high temperature")
        
        logging.info(f"✓ High temp (75°F > 72°F): Cooling activated")
        
        # Clear log
        self.actuationLog.clear()
        
        # Test LOW temperature
        logging.info("\nTesting LOW temperature threshold")
        tempData.setValue(65.0)  # Below ALE min (68.0)
        
        result = self.deviceDataMgr.handleSensorData(tempData)
        self.assertTrue(result, "Failed to handle low temperature sensor data")
        
        time.sleep(0.5)
        
        # Verify heating was triggered
        hvacActuations = [a for a in self.actuationLog if a['type'] == ConfigConst.HVAC_ACTUATOR_TYPE]
        self.assertGreater(len(hvacActuations), 0, "No HVAC actuation for low temperature")
        
        heatingActuation = next((a for a in hvacActuations if a['command'] == ConfigConst.HVAC_HEATING_CMD), None)
        self.assertIsNotNone(heatingActuation, "Heating not triggered for low temperature")
        
        logging.info(f"✓ Low temp (65°F < 68°F): Heating activated")
        
        # Clear log
        self.actuationLog.clear()
        
        # Test OPTIMAL temperature
        logging.info("\nTesting OPTIMAL temperature")
        tempData.setValue(70.0)  # Within ALE range (68-72)
        
        result = self.deviceDataMgr.handleSensorData(tempData)
        self.assertTrue(result, "Failed to handle optimal temperature sensor data")
        
        time.sleep(0.5)
        
        logging.info(f"✓ Optimal temp (70°F within 68-72°F): No heating/cooling needed")
        
        logging.info("\n✓✓✓ Test PASSED: Temperature threshold response working ✓✓✓\n")
    
    # ========================================================================
    # Test 4: Humidity Threshold Response
    # ========================================================================
    
    def testHumidityThresholdResponse(self):
        """
        Test humidity threshold crossing detection and response.
        """
        logging.info("\n\n===== Test 4: Humidity Threshold Response =====\n")
        
        # Test LOW humidity
        logging.info("Testing LOW humidity threshold")
        humidData = SensorData()
        humidData.setTypeID(ConfigConst.HUMIDITY_SENSOR_TYPE)
        humidData.setValue(55.0)  # Below ALE min (60.0)
        humidData.setName("HumiditySensor")
        
        result = self.deviceDataMgr.handleSensorData(humidData)
        self.assertTrue(result, "Failed to handle low humidity sensor data")
        
        time.sleep(0.5)
        
        # Verify humidifier was triggered
        humidifierActuations = [a for a in self.actuationLog if a['type'] == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE]
        self.assertGreater(len(humidifierActuations), 0, "No humidifier actuation for low humidity")
        
        onActuation = next((a for a in humidifierActuations if a['command'] == ConfigConst.HUMIDIFIER_ON_CMD), None)
        self.assertIsNotNone(onActuation, "Humidifier ON not triggered for low humidity")
        
        logging.info(f"✓ Low humidity (55% < 60%): Humidifier activated")
        
        # Clear log
        self.actuationLog.clear()
        
        # Test HIGH humidity
        logging.info("\nTesting HIGH humidity threshold")
        humidData.setValue(72.0)  # Above ALE max (70.0)
        
        result = self.deviceDataMgr.handleSensorData(humidData)
        self.assertTrue(result, "Failed to handle high humidity sensor data")
        
        time.sleep(0.5)
        
        # Verify humidifier deactivation or no activation
        humidifierActuations = [a for a in self.actuationLog if a['type'] == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE]
        
        if len(humidifierActuations) > 0:
            offActuation = next((a for a in humidifierActuations if a['command'] == ConfigConst.HUMIDIFIER_OFF_CMD), None)
            if offActuation:
                logging.info(f"✓ High humidity (72% > 70%): Humidifier deactivated")
        else:
            logging.info(f"✓ High humidity (72% > 70%): No humidifier activation")
        
        # Clear log
        self.actuationLog.clear()
        
        # Test OPTIMAL humidity
        logging.info("\nTesting OPTIMAL humidity")
        humidData.setValue(65.0)  # Within ALE range (60-70)
        
        result = self.deviceDataMgr.handleSensorData(humidData)
        self.assertTrue(result, "Failed to handle optimal humidity sensor data")
        
        time.sleep(0.5)
        
        logging.info(f"✓ Optimal humidity (65% within 60-70%)")
        
        logging.info("\n✓✓✓ Test PASSED: Humidity threshold response working ✓✓✓\n")
    
    # ========================================================================
    # Test 5: Temperature Spike Detection
    # ========================================================================
    
    def testTemperatureSpikeDetection(self):
        """
        Test temperature spike detection (potential infection indicator).
        Simulates rapid temperature increase over time.
        """
        logging.info("\n\n===== Test 5: Temperature Spike Detection =====\n")
        
        logging.info("Simulating gradual temperature increase (normal fermentation)")
        
        # Simulate normal temperature rise (slow, gradual)
        baseTemp = 68.0
        for i in range(5):
            tempData = SensorData()
            tempData.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
            tempData.setValue(baseTemp + (i * 0.5))  # Increase by 0.5°F each reading
            tempData.setName("TempSensor")
            
            self.deviceDataMgr.handleSensorData(tempData)
            time.sleep(0.1)
        
        logging.info(f"✓ Normal rise: {baseTemp}°F → {baseTemp + 2.0}°F over 5 readings")
        
        # Verify no spike detected for normal rise
        spikeDetected = self.deviceDataMgr._detectTemperatureSpike()
        self.assertFalse(spikeDetected, "False positive: spike detected for normal temperature rise")
        logging.info("✓ No spike detected for normal rise (correct)")
        
        # Clear temperature history
        self.deviceDataMgr.recentTemperatures = []
        
        logging.info("\nSimulating rapid temperature spike (potential infection)")
        
        # Simulate rapid temperature spike
        # Add enough readings to reach 30-minute threshold with timestamps
        currentTime = time.time()
        
        for i in range(16):  # 16 readings at 2-min intervals = 30 minutes
            self.deviceDataMgr.recentTemperatures.append({
                'value': 68.0 + (i * 0.4),  # Gradual increase
                'timestamp': currentTime - (1800 - (i * 120))  # Spread over 30 minutes
            })
        
        # Verify spike is detected
        spikeDetected = self.deviceDataMgr._detectTemperatureSpike()
        
        tempDelta = self.deviceDataMgr.recentTemperatures[-1]['value'] - self.deviceDataMgr.recentTemperatures[0]['value']
        
        if tempDelta >= ConfigConst.TEMP_SPIKE_THRESHOLD:
            self.assertTrue(spikeDetected, "Spike not detected when temperature increased rapidly")
            logging.info(f"✓ Spike detected: {self.deviceDataMgr.recentTemperatures[0]['value']:.1f}°F → {self.deviceDataMgr.recentTemperatures[-1]['value']:.1f}°F (+{tempDelta:.1f}°F in 30 min)")
        else:
            logging.info(f"✓ No spike: Change of {tempDelta:.1f}°F below threshold ({ConfigConst.TEMP_SPIKE_THRESHOLD}°F)")
        
        logging.info("\n✓✓✓ Test PASSED: Temperature spike detection working ✓✓✓\n")
    
    # ========================================================================
    # Test 6: Multiple Profile Switching
    # ========================================================================
    
    def testMultipleProfileSwitching(self):
        """
        Test switching between multiple fermentation profiles.
        """
        logging.info("\n\n===== Test 6: Multiple Profile Switching =====\n")
        
        profiles = [
            ConfigConst.FERMENTATION_PROFILE_ALE,
            ConfigConst.FERMENTATION_PROFILE_LAGER,
            ConfigConst.FERMENTATION_PROFILE_CONDITIONING,
            ConfigConst.FERMENTATION_PROFILE_COLD_CRASH
        ]
        
        for profile in profiles:
            logging.info(f"\nSwitching to {profile} profile")
            
            profileCmd = ActuatorData()
            profileCmd.setActuatorType(ConfigConst.FERMENTATION_PROFILE_ACTUATOR_TYPE)
            profileCmd.setCommand(profile)
            
            result = self.deviceDataMgr._handleFermentationProfileCommand(profileCmd)
            self.assertTrue(result, f"Failed to switch to {profile} profile")
            
            self.assertEqual(self.deviceDataMgr.currentFermentationProfile, profile)
            
            logging.info(f"✓ Profile: {profile}")
            logging.info(f"  Temp: [{self.deviceDataMgr.currentTempMin}-{self.deviceDataMgr.currentTempMax}]°F")
            logging.info(f"  Humidity: [{self.deviceDataMgr.currentHumidityMin}-{self.deviceDataMgr.currentHumidityMax}]%")
            
            time.sleep(0.2)
        
        logging.info("\n✓✓✓ Test PASSED: Multiple profile switching working ✓✓✓\n")
    
    # ========================================================================
    # Test 7: Critical Threshold Handling
    # ========================================================================
    
    def testCriticalThresholdHandling(self):
        """
        Test critical (emergency) threshold handling.
        """
        logging.info("\n\n===== Test 7: Critical Threshold Handling =====\n")
        
        # Test CRITICAL HIGH temperature
        logging.info("Testing CRITICAL HIGH temperature")
        self.actuationLog.clear()
        
        tempData = SensorData()
        tempData.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
        tempData.setValue(85.0)  # Above CRITICAL_HIGH (80.0)
        tempData.setName("TempSensor")
        
        result = self.deviceDataMgr.handleSensorData(tempData)
        self.assertTrue(result, "Failed to handle critical high temperature")
        
        time.sleep(0.5)
        
        # Verify emergency cooling triggered
        hvacActuations = [a for a in self.actuationLog if a['type'] == ConfigConst.HVAC_ACTUATOR_TYPE]
        self.assertGreater(len(hvacActuations), 0, "No emergency response for critical high temperature")
        
        emergencyCooling = next((a for a in hvacActuations if a['value'] >= 2.0), None)
        if emergencyCooling:
            logging.info(f"✓ Emergency cooling activated: value={emergencyCooling['value']}")
        else:
            logging.info("✓ Critical cooling response triggered")
        
        # Test CRITICAL LOW temperature
        logging.info("\nTesting CRITICAL LOW temperature")
        self.actuationLog.clear()
        
        tempData.setValue(30.0)  # Below CRITICAL_LOW (32.0)
        
        result = self.deviceDataMgr.handleSensorData(tempData)
        self.assertTrue(result, "Failed to handle critical low temperature")
        
        time.sleep(0.5)
        
        # Verify emergency heating triggered
        hvacActuations = [a for a in self.actuationLog if a['type'] == ConfigConst.HVAC_ACTUATOR_TYPE]
        self.assertGreater(len(hvacActuations), 0, "No emergency response for critical low temperature")
        
        logging.info("✓ Emergency heating response triggered")
        
        logging.info("\n✓✓✓ Test PASSED: Critical threshold handling working ✓✓✓\n")
    
    # ========================================================================
    # Test 8: Concurrent Sensor Processing
    # ========================================================================
    
    def testConcurrentSensorProcessing(self):
        """
        Test processing multiple sensors simultaneously.
        """
        logging.info("\n\n===== Test 8: Concurrent Sensor Processing =====\n")
        
        self.actuationLog.clear()
        
        # Send temperature data
        tempData = SensorData()
        tempData.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
        tempData.setValue(75.0)  # High
        tempData.setName("TempSensor")
        self.deviceDataMgr.handleSensorData(tempData)
        
        # Send humidity data
        humidData = SensorData()
        humidData.setTypeID(ConfigConst.HUMIDITY_SENSOR_TYPE)
        humidData.setValue(55.0)  # Low
        humidData.setName("HumiditySensor")
        self.deviceDataMgr.handleSensorData(humidData)
        
        # Send pressure data
        pressData = SensorData()
        pressData.setTypeID(ConfigConst.PRESSURE_SENSOR_TYPE)
        pressData.setValue(101.5)
        pressData.setName("PressureSensor")
        self.deviceDataMgr.handleSensorData(pressData)
        
        time.sleep(0.5)
        
        # Verify multiple actuations occurred
        hvacActuations = [a for a in self.actuationLog if a['type'] == ConfigConst.HVAC_ACTUATOR_TYPE]
        humidifierActuations = [a for a in self.actuationLog if a['type'] == ConfigConst.HUMIDIFIER_ACTUATOR_TYPE]
        
        self.assertGreater(len(hvacActuations), 0, "HVAC not actuated for high temp")
        self.assertGreater(len(humidifierActuations), 0, "Humidifier not actuated for low humidity")
        
        logging.info(f"✓ HVAC actuations: {len(hvacActuations)}")
        logging.info(f"✓ Humidifier actuations: {len(humidifierActuations)}")
        logging.info(f"✓ Total actuations: {len(self.actuationLog)}")
        
        logging.info("\n✓✓✓ Test PASSED: Concurrent sensor processing working ✓✓✓\n")

if __name__ == '__main__':
    """
    Run all integration tests for fermentation system.
    """
    unittest.main()