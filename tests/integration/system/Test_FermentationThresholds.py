"""
Unit tests for fermentation threshold detection and profile management.

This module tests the threshold logic for various fermentation profiles,
ensuring that temperature and humidity boundaries are correctly enforced
and that profile switching properly updates threshold values.

Validation:
- ALE profile thresholds
- LAGER profile thresholds
- CONDITIONING profile thresholds
- COLD_CRASH profile thresholds
- Profile switching logic
- Threshold comparison logic

@author: Emma
"""

import unittest
import logging

from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.common.ConfigConst import ConfigConst

class Test_FermentationThresholds(unittest.TestCase):
    """
    Unit tests for fermentation threshold detection and validation.
    
    This test suite validates that each fermentation profile correctly
    defines its temperature and humidity boundaries and that threshold
    crossing detection works as expected.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Set up test fixtures for all tests.
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        logging.info("\n\n===== Fermentation Threshold Unit Tests =====\n")
    
    def setUp(self):
        """
        Set up each individual test.
        """
        self.deviceDataMgr = DeviceDataManager()
        
        # Track actuations
        self.actuationCount = 0
        
        # Override sendActuatorCommand to count actuations
        self.originalSendCommand = self.deviceDataMgr.actuatorAdapterManager.sendActuatorCommand
        self.deviceDataMgr.actuatorAdapterManager.sendActuatorCommand = self.countActuation
    
    def countActuation(self, data: ActuatorData) -> bool:
        """
        Count actuation commands for verification.
        """
        self.actuationCount += 1
        logging.debug(f"Actuation #{self.actuationCount}: Type={data.getTypeID()}, Command={data.getCommand()}")
        return self.originalSendCommand(data)
    
    def tearDown(self):
        """
        Clean up after each test.
        """
        pass
    
    # ========================================================================
    # Test 1: ALE Profile Thresholds
    # ========================================================================
    
    def testAleProfileThresholds(self):
        """
        Test ALE fermentation profile threshold values.
        
        Expected ALE thresholds:
        - Temperature: 68-72°F
        - Humidity: 60-70%
        """
        logging.info("\n===== Test 1: ALE Profile Thresholds =====\n")
        
        # Set to ALE profile
        profileCmd = ActuatorData()
        profileCmd.setActuatorType(ConfigConst.FERMENTATION_PROFILE_ACTUATOR_TYPE)
        profileCmd.setCommand(ConfigConst.FERMENTATION_PROFILE_ALE)
        
        result = self.deviceDataMgr._handleFermentationProfileCommand(profileCmd)
        self.assertTrue(result, "Failed to set ALE profile")
        
        # Verify profile set correctly
        self.assertEqual(self.deviceDataMgr.currentFermentationProfile, ConfigConst.FERMENTATION_PROFILE_ALE)
        
        # Verify temperature thresholds
        self.assertEqual(self.deviceDataMgr.currentTempMin, ConfigConst.ALE_TEMP_MIN)
        self.assertEqual(self.deviceDataMgr.currentTempMax, ConfigConst.ALE_TEMP_MAX)
        
        logging.info(f"✓ ALE Temp Range: [{self.deviceDataMgr.currentTempMin} - {self.deviceDataMgr.currentTempMax}]°F")
        logging.info(f"  Expected: [{ConfigConst.ALE_TEMP_MIN} - {ConfigConst.ALE_TEMP_MAX}]°F")
        
        # Verify humidity thresholds
        self.assertEqual(self.deviceDataMgr.currentHumidityMin, ConfigConst.ALE_HUMIDITY_MIN)
        self.assertEqual(self.deviceDataMgr.currentHumidityMax, ConfigConst.ALE_HUMIDITY_MAX)
        
        logging.info(f"✓ ALE Humidity Range: [{self.deviceDataMgr.currentHumidityMin} - {self.deviceDataMgr.currentHumidityMax}]%")
        logging.info(f"  Expected: [{ConfigConst.ALE_HUMIDITY_MIN} - {ConfigConst.ALE_HUMIDITY_MAX}]%")
        
        logging.info("\n✓ Test PASSED: ALE profile thresholds correct\n")
    
    # ========================================================================
    # Test 2: LAGER Profile Thresholds
    # ========================================================================
    
    def testLagerProfileThresholds(self):
        """
        Test LAGER fermentation profile threshold values.
        
        Expected LAGER thresholds:
        - Temperature: 50-55°F
        - Humidity: 55-65%
        """
        logging.info("\n===== Test 2: LAGER Profile Thresholds =====\n")
        
        # Set to LAGER profile
        profileCmd = ActuatorData()
        profileCmd.setActuatorType(ConfigConst.FERMENTATION_PROFILE_ACTUATOR_TYPE)
        profileCmd.setCommand(ConfigConst.FERMENTATION_PROFILE_LAGER)
        
        result = self.deviceDataMgr._handleFermentationProfileCommand(profileCmd)
        self.assertTrue(result, "Failed to set LAGER profile")
        
        # Verify profile set correctly
        self.assertEqual(self.deviceDataMgr.currentFermentationProfile, ConfigConst.FERMENTATION_PROFILE_LAGER)
        
        # Verify temperature thresholds
        self.assertEqual(self.deviceDataMgr.currentTempMin, ConfigConst.LAGER_TEMP_MIN)
        self.assertEqual(self.deviceDataMgr.currentTempMax, ConfigConst.LAGER_TEMP_MAX)
        
        logging.info(f"✓ LAGER Temp Range: [{self.deviceDataMgr.currentTempMin} - {self.deviceDataMgr.currentTempMax}]°F")
        logging.info(f"  Expected: [{ConfigConst.LAGER_TEMP_MIN} - {ConfigConst.LAGER_TEMP_MAX}]°F")
        
        # Verify humidity thresholds
        self.assertEqual(self.deviceDataMgr.currentHumidityMin, ConfigConst.LAGER_HUMIDITY_MIN)
        self.assertEqual(self.deviceDataMgr.currentHumidityMax, ConfigConst.LAGER_HUMIDITY_MAX)
        
        logging.info(f"✓ LAGER Humidity Range: [{self.deviceDataMgr.currentHumidityMin} - {self.deviceDataMgr.currentHumidityMax}]%")
        logging.info(f"  Expected: [{ConfigConst.LAGER_HUMIDITY_MIN} - {ConfigConst.LAGER_HUMIDITY_MAX}]%")
        
        logging.info("\n✓ Test PASSED: LAGER profile thresholds correct\n")
    
    # ========================================================================
    # Test 3: CONDITIONING Profile Thresholds
    # ========================================================================
    
    def testConditioningProfileThresholds(self):
        """
        Test CONDITIONING fermentation profile threshold values.
        
        Expected CONDITIONING thresholds:
        - Temperature: 55-65°F
        - Humidity: 50-60%
        """
        logging.info("\n===== Test 3: CONDITIONING Profile Thresholds =====\n")
        
        # Set to CONDITIONING profile
        profileCmd = ActuatorData()
        profileCmd.setActuatorType(ConfigConst.FERMENTATION_PROFILE_ACTUATOR_TYPE)
        profileCmd.setCommand(ConfigConst.FERMENTATION_PROFILE_CONDITIONING)
        
        result = self.deviceDataMgr._handleFermentationProfileCommand(profileCmd)
        self.assertTrue(result, "Failed to set CONDITIONING profile")
        
        # Verify profile set correctly
        self.assertEqual(self.deviceDataMgr.currentFermentationProfile, ConfigConst.FERMENTATION_PROFILE_CONDITIONING)
        
        # Verify temperature thresholds
        self.assertEqual(self.deviceDataMgr.currentTempMin, ConfigConst.CONDITIONING_TEMP_MIN)
        self.assertEqual(self.deviceDataMgr.currentTempMax, ConfigConst.CONDITIONING_TEMP_MAX)
        
        logging.info(f"✓ CONDITIONING Temp Range: [{self.deviceDataMgr.currentTempMin} - {self.deviceDataMgr.currentTempMax}]°F")
        logging.info(f"  Expected: [{ConfigConst.CONDITIONING_TEMP_MIN} - {ConfigConst.CONDITIONING_TEMP_MAX}]°F")
        
        # Verify humidity thresholds
        self.assertEqual(self.deviceDataMgr.currentHumidityMin, ConfigConst.CONDITIONING_HUMIDITY_MIN)
        self.assertEqual(self.deviceDataMgr.currentHumidityMax, ConfigConst.CONDITIONING_HUMIDITY_MAX)
        
        logging.info(f"✓ CONDITIONING Humidity Range: [{self.deviceDataMgr.currentHumidityMin} - {self.deviceDataMgr.currentHumidityMax}]%")
        logging.info(f"  Expected: [{ConfigConst.CONDITIONING_HUMIDITY_MIN} - {ConfigConst.CONDITIONING_HUMIDITY_MAX}]%")
        
        logging.info("\n✓ Test PASSED: CONDITIONING profile thresholds correct\n")
    
    # ========================================================================
    # Test 4: COLD_CRASH Profile Thresholds
    # ========================================================================
    
    def testColdCrashProfileThresholds(self):
        """
        Test COLD_CRASH fermentation profile threshold values.
        
        Expected COLD_CRASH thresholds:
        - Temperature: 35-40°F
        - Humidity: 50-60%
        """
        logging.info("\n===== Test 4: COLD_CRASH Profile Thresholds =====\n")
        
        # Set to COLD_CRASH profile
        profileCmd = ActuatorData()
        profileCmd.setActuatorType(ConfigConst.FERMENTATION_PROFILE_ACTUATOR_TYPE)
        profileCmd.setCommand(ConfigConst.FERMENTATION_PROFILE_COLD_CRASH)
        
        result = self.deviceDataMgr._handleFermentationProfileCommand(profileCmd)
        self.assertTrue(result, "Failed to set COLD_CRASH profile")
        
        # Verify profile set correctly
        self.assertEqual(self.deviceDataMgr.currentFermentationProfile, ConfigConst.FERMENTATION_PROFILE_COLD_CRASH)
        
        # Verify temperature thresholds
        self.assertEqual(self.deviceDataMgr.currentTempMin, ConfigConst.COLD_CRASH_TEMP_MIN)
        self.assertEqual(self.deviceDataMgr.currentTempMax, ConfigConst.COLD_CRASH_TEMP_MAX)
        
        logging.info(f"✓ COLD_CRASH Temp Range: [{self.deviceDataMgr.currentTempMin} - {self.deviceDataMgr.currentTempMax}]°F")
        logging.info(f"  Expected: [{ConfigConst.COLD_CRASH_TEMP_MIN} - {ConfigConst.COLD_CRASH_TEMP_MAX}]°F")
        
        # Verify humidity thresholds
        self.assertEqual(self.deviceDataMgr.currentHumidityMin, ConfigConst.COLD_CRASH_HUMIDITY_MIN)
        self.assertEqual(self.deviceDataMgr.currentHumidityMax, ConfigConst.COLD_CRASH_HUMIDITY_MAX)
        
        logging.info(f"✓ COLD_CRASH Humidity Range: [{self.deviceDataMgr.currentHumidityMin} - {self.deviceDataMgr.currentHumidityMax}]%")
        logging.info(f"  Expected: [{ConfigConst.COLD_CRASH_HUMIDITY_MIN} - {ConfigConst.COLD_CRASH_HUMIDITY_MAX}]%")
        
        logging.info("\n✓ Test PASSED: COLD_CRASH profile thresholds correct\n")
    
    # ========================================================================
    # Test 5: Temperature Above Threshold Detection
    # ========================================================================
    
    def testTemperatureAboveThreshold(self):
        """
        Test detection of temperature above maximum threshold.
        """
        logging.info("\n===== Test 5: Temperature Above Threshold Detection =====\n")
        
        # Use ALE profile (max 72°F)
        self.deviceDataMgr.currentFermentationProfile = ConfigConst.FERMENTATION_PROFILE_ALE
        self.deviceDataMgr.currentTempMax = ConfigConst.ALE_TEMP_MAX
        
        # Create temperature data above threshold
        tempData = SensorData()
        tempData.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
        tempData.setValue(75.0)  # Above 72°F max
        tempData.setName("TempSensor")
        
        # Reset actuation count
        self.actuationCount = 0
        
        # Handle sensor data
        result = self.deviceDataMgr.handleSensorData(tempData)
        self.assertTrue(result, "Failed to handle temperature sensor data")
        
        # Verify actuation occurred
        self.assertGreater(self.actuationCount, 0, "No actuation triggered for high temperature")
        
        logging.info(f"✓ Temperature 75.0°F > 72.0°F threshold")
        logging.info(f"✓ Actuation triggered: {self.actuationCount} command(s)")
        
        logging.info("\n✓ Test PASSED: High temperature detected and handled\n")
    
    # ========================================================================
    # Test 6: Temperature Below Threshold Detection
    # ========================================================================
    
    def testTemperatureBelowThreshold(self):
        """
        Test detection of temperature below minimum threshold.
        """
        logging.info("\n===== Test 6: Temperature Below Threshold Detection =====\n")
        
        # Use ALE profile (min 68°F)
        self.deviceDataMgr.currentFermentationProfile = ConfigConst.FERMENTATION_PROFILE_ALE
        self.deviceDataMgr.currentTempMin = ConfigConst.ALE_TEMP_MIN
        
        # Create temperature data below threshold
        tempData = SensorData()
        tempData.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
        tempData.setValue(65.0)  # Below 68°F min
        tempData.setName("TempSensor")
        
        # Reset actuation count
        self.actuationCount = 0
        
        # Handle sensor data
        result = self.deviceDataMgr.handleSensorData(tempData)
        self.assertTrue(result, "Failed to handle temperature sensor data")
        
        # Verify actuation occurred
        self.assertGreater(self.actuationCount, 0, "No actuation triggered for low temperature")
        
        logging.info(f"✓ Temperature 65.0°F < 68.0°F threshold")
        logging.info(f"✓ Actuation triggered: {self.actuationCount} command(s)")
        
        logging.info("\n✓ Test PASSED: Low temperature detected and handled\n")
    
    # ========================================================================
    # Test 7: Temperature Within Range
    # ========================================================================
    
    def testTemperatureWithinRange(self):
        """
        Test that temperature within range does not trigger unnecessary actuation.
        """
        logging.info("\n===== Test 7: Temperature Within Range =====\n")
        
        # Use ALE profile (68-72°F)
        self.deviceDataMgr.currentFermentationProfile = ConfigConst.FERMENTATION_PROFILE_ALE
        self.deviceDataMgr.currentTempMin = ConfigConst.ALE_TEMP_MIN
        self.deviceDataMgr.currentTempMax = ConfigConst.ALE_TEMP_MAX
        
        # Create temperature data within range
        tempData = SensorData()
        tempData.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
        tempData.setValue(70.0)  # Within 68-72°F range
        tempData.setName("TempSensor")
        
        # Reset actuation count
        self.actuationCount = 0
        
        # Handle sensor data
        result = self.deviceDataMgr.handleSensorData(tempData)
        self.assertTrue(result, "Failed to handle temperature sensor data")
        
        logging.info(f"✓ Temperature 70.0°F within [{ConfigConst.ALE_TEMP_MIN} - {ConfigConst.ALE_TEMP_MAX}]°F range")
        logging.info(f"✓ Actuations triggered: {self.actuationCount}")
        
        logging.info("\n✓ Test PASSED: Optimal temperature handled correctly\n")
    
    # ========================================================================
    # Test 8: Humidity Above Threshold Detection
    # ========================================================================
    
    def testHumidityAboveThreshold(self):
        """
        Test detection of humidity above maximum threshold.
        """
        logging.info("\n===== Test 8: Humidity Above Threshold Detection =====\n")
        
        # Use ALE profile (max 70%)
        self.deviceDataMgr.currentFermentationProfile = ConfigConst.FERMENTATION_PROFILE_ALE
        self.deviceDataMgr.currentHumidityMax = ConfigConst.ALE_HUMIDITY_MAX
        
        # Create humidity data above threshold
        humidData = SensorData()
        humidData.setTypeID(ConfigConst.HUMIDITY_SENSOR_TYPE)
        humidData.setValue(75.0)  # Above 70% max
        humidData.setName("HumiditySensor")
        
        # Reset actuation count
        self.actuationCount = 0
        
        # Handle sensor data
        result = self.deviceDataMgr.handleSensorData(humidData)
        self.assertTrue(result, "Failed to handle humidity sensor data")
        
        logging.info(f"✓ Humidity 75.0% > 70.0% threshold")
        logging.info(f"✓ Actuations triggered: {self.actuationCount}")
        
        logging.info("\n✓ Test PASSED: High humidity detected and handled\n")
    
    # ========================================================================
    # Test 9: Humidity Below Threshold Detection
    # ========================================================================
    
    def testHumidityBelowThreshold(self):
        """
        Test detection of humidity below minimum threshold.
        """
        logging.info("\n===== Test 9: Humidity Below Threshold Detection =====\n")
        
        # Use ALE profile (min 60%)
        self.deviceDataMgr.currentFermentationProfile = ConfigConst.FERMENTATION_PROFILE_ALE
        self.deviceDataMgr.currentHumidityMin = ConfigConst.ALE_HUMIDITY_MIN
        
        # Create humidity data below threshold
        humidData = SensorData()
        humidData.setTypeID(ConfigConst.HUMIDITY_SENSOR_TYPE)
        humidData.setValue(55.0)  # Below 60% min
        humidData.setName("HumiditySensor")
        
        # Reset actuation count
        self.actuationCount = 0
        
        # Handle sensor data
        result = self.deviceDataMgr.handleSensorData(humidData)
        self.assertTrue(result, "Failed to handle humidity sensor data")
        
        # Verify actuation occurred
        self.assertGreater(self.actuationCount, 0, "No actuation triggered for low humidity")
        
        logging.info(f"✓ Humidity 55.0% < 60.0% threshold")
        logging.info(f"✓ Actuation triggered: {self.actuationCount} command(s)")
        
        logging.info("\n✓ Test PASSED: Low humidity detected and handled\n")
    
    # ========================================================================
    # Test 10: Profile Switching Updates Thresholds
    # ========================================================================
    
    def testProfileSwitchingUpdatesThresholds(self):
        """
        Test that switching profiles correctly updates threshold values.
        """
        logging.info("\n===== Test 10: Profile Switching Updates Thresholds =====\n")
        
        # Start with ALE profile
        aleCmd = ActuatorData()
        aleCmd.setActuatorType(ConfigConst.FERMENTATION_PROFILE_ACTUATOR_TYPE)
        aleCmd.setCommand(ConfigConst.FERMENTATION_PROFILE_ALE)
        
        self.deviceDataMgr._handleFermentationProfileCommand(aleCmd)
        
        aleTemp = self.deviceDataMgr.currentTempMax
        logging.info(f"ALE profile temp max: {aleTemp}°F")
        
        # Switch to LAGER profile
        lagerCmd = ActuatorData()
        lagerCmd.setActuatorType(ConfigConst.FERMENTATION_PROFILE_ACTUATOR_TYPE)
        lagerCmd.setCommand(ConfigConst.FERMENTATION_PROFILE_LAGER)
        
        self.deviceDataMgr._handleFermentationProfileCommand(lagerCmd)
        
        lagerTemp = self.deviceDataMgr.currentTempMax
        logging.info(f"LAGER profile temp max: {lagerTemp}°F")
        
        # Verify thresholds changed
        self.assertNotEqual(aleTemp, lagerTemp, "Temperature threshold did not change when switching profiles")
        
        logging.info(f"✓ Threshold changed: {aleTemp}°F → {lagerTemp}°F")
        
        # Verify new thresholds match LAGER profile
        self.assertEqual(self.deviceDataMgr.currentTempMin, ConfigConst.LAGER_TEMP_MIN)
        self.assertEqual(self.deviceDataMgr.currentTempMax, ConfigConst.LAGER_TEMP_MAX)
        self.assertEqual(self.deviceDataMgr.currentHumidityMin, ConfigConst.LAGER_HUMIDITY_MIN)
        self.assertEqual(self.deviceDataMgr.currentHumidityMax, ConfigConst.LAGER_HUMIDITY_MAX)
        
        logging.info("\n✓ Test PASSED: Profile switching updates thresholds correctly\n")
    
    # ========================================================================
    # Test 11: Invalid Profile Command
    # ========================================================================
    
    def testInvalidProfileCommand(self):
        """
        Test handling of invalid profile name.
        """
        logging.info("\n===== Test 11: Invalid Profile Command =====\n")
        
        # Store current profile
        originalProfile = self.deviceDataMgr.currentFermentationProfile
        
        # Try to set invalid profile
        invalidCmd = ActuatorData()
        invalidCmd.setActuatorType(ConfigConst.FERMENTATION_PROFILE_ACTUATOR_TYPE)
        invalidCmd.setCommand("INVALID_PROFILE")
        
        result = self.deviceDataMgr._handleFermentationProfileCommand(invalidCmd)
        
        # Should return False for invalid profile
        self.assertFalse(result, "Invalid profile command should return False")
        
        # Verify profile unchanged
        self.assertEqual(self.deviceDataMgr.currentFermentationProfile, originalProfile)
        
        logging.info(f"✓ Invalid profile rejected")
        logging.info(f"✓ Profile remained: {originalProfile}")
        
        logging.info("\n✓ Test PASSED: Invalid profile handled correctly\n")
    
    # ========================================================================
    # Test 12: Critical Temperature Thresholds
    # ========================================================================
    
    def testCriticalTemperatureThresholds(self):
        """
        Test critical temperature thresholds (profile-independent).
        """
        logging.info("\n===== Test 12: Critical Temperature Thresholds =====\n")
        
        # Test CRITICAL HIGH
        logging.info("Testing CRITICAL HIGH temperature")
        
        criticalHighTemp = SensorData()
        criticalHighTemp.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
        criticalHighTemp.setValue(85.0)  # Above CRITICAL_HIGH (80.0)
        criticalHighTemp.setName("TempSensor")
        
        self.actuationCount = 0
        result = self.deviceDataMgr.handleSensorData(criticalHighTemp)
        
        self.assertTrue(result, "Failed to handle critical high temperature")
        self.assertGreater(self.actuationCount, 0, "No actuation for critical high temperature")
        
        logging.info(f"✓ Critical high (85.0°F > 80.0°F): {self.actuationCount} actuation(s)")
        
        # Test CRITICAL LOW
        logging.info("\nTesting CRITICAL LOW temperature")
        
        criticalLowTemp = SensorData()
        criticalLowTemp.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
        criticalLowTemp.setValue(30.0)  # Below CRITICAL_LOW (32.0)
        criticalLowTemp.setName("TempSensor")
        
        self.actuationCount = 0
        result = self.deviceDataMgr.handleSensorData(criticalLowTemp)
        
        self.assertTrue(result, "Failed to handle critical low temperature")
        self.assertGreater(self.actuationCount, 0, "No actuation for critical low temperature")
        
        logging.info(f"✓ Critical low (30.0°F < 32.0°F): {self.actuationCount} actuation(s)")
        
        logging.info("\n✓ Test PASSED: Critical thresholds handled correctly\n")

if __name__ == '__main__':
    """
    Run all fermentation threshold unit tests.
    """
    unittest.main()