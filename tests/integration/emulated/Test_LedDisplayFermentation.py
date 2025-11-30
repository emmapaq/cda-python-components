"""
Integration tests for LED display with fermentation-specific features.

This module tests the LED display emulator's ability to show fermentation
system status, including color-coded displays, status messages, temperature
and humidity information, and alert notifications.

Validation:
- Optimal status display (green)
- Active fermentation display (yellow)
- Alert status display (red)
- Profile change notifications
- Temperature/humidity value display
- Color coding functionality
- Message formatting
- Rapid status changes

@author: Emma
"""

import unittest
import logging
import time

from programmingtheiot.cda.emulated.LedDisplayEmulatorTask import LedDisplayEmulatorTask
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.common.ConfigConst import ConfigConst

class Test_LedDisplayFermentation(unittest.TestCase):
    """
    Integration tests for LED display fermentation features.
    
    This test suite validates that the LED display correctly shows
    fermentation system status with appropriate color coding and
    formatted messages.
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
        
        logging.info("\n\n===== LED Display Fermentation Integration Tests =====\n")
        
        # Create LED display instance
        cls.ledDisplay = LedDisplayEmulatorTask()
    
    def setUp(self):
        """
        Set up each individual test.
        """
        pass
    
    def tearDown(self):
        """
        Clean up after each test.
        """
        time.sleep(0.5)  # Brief pause between tests for display
    
    # ========================================================================
    # Test 1: Optimal Status Display
    # ========================================================================
    
    def testOptimalStatusDisplay(self):
        """
        Test LED display showing optimal fermentation conditions (green).
        """
        logging.info("\n===== Test 1: Optimal Status Display =====\n")
        
        # Create optimal status display command
        ledCmd = ActuatorData()
        ledCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_OPTIMAL_CMD)
        ledCmd.setStateData("Temp: 70.0°F, Humidity: 65% - OPTIMAL")
        ledCmd.setName("LED Optimal Status")
        
        logging.info("Displaying: " + ledCmd.getStateData())
        logging.info("Status: OPTIMAL (Green)")
        
        # Execute command
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "LED display command should succeed")
        
        # Verify latest response
        latestResponse = self.ledDisplay.getLatestActuatorResponse()
        self.assertIsNotNone(latestResponse, "Latest response should be set")
        self.assertEqual(latestResponse.getCommand(), ConfigConst.LED_OPTIMAL_CMD)
        
        logging.info("✓ Optimal status displayed successfully")
        
        logging.info("\n✓✓✓ Test PASSED: Optimal display working ✓✓✓\n")
    
    # ========================================================================
    # Test 2: Active Fermentation Display
    # ========================================================================
    
    def testActiveFermentationDisplay(self):
        """
        Test LED display showing active fermentation status (yellow).
        """
        logging.info("\n===== Test 2: Active Fermentation Display =====\n")
        
        # Create active status display command
        ledCmd = ActuatorData()
        ledCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_ACTIVE_CMD)
        ledCmd.setStateData("Fermenting Active - Temp: 73.5°F")
        ledCmd.setName("LED Active Status")
        
        logging.info("Displaying: " + ledCmd.getStateData())
        logging.info("Status: ACTIVE (Yellow)")
        
        # Execute command
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "LED display command should succeed")
        
        # Verify latest response
        latestResponse = self.ledDisplay.getLatestActuatorResponse()
        self.assertEqual(latestResponse.getCommand(), ConfigConst.LED_ACTIVE_CMD)
        
        logging.info("✓ Active fermentation status displayed successfully")
        
        logging.info("\n✓✓✓ Test PASSED: Active display working ✓✓✓\n")
    
    # ========================================================================
    # Test 3: Alert Status Display
    # ========================================================================
    
    def testAlertStatusDisplay(self):
        """
        Test LED display showing alert status (red).
        """
        logging.info("\n===== Test 3: Alert Status Display =====\n")
        
        # Create alert status display command
        ledCmd = ActuatorData()
        ledCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_ALERT_CMD)
        ledCmd.setStateData("⚠ ALERT: Temperature Critical - 85°F!")
        ledCmd.setName("LED Alert Status")
        
        logging.info("Displaying: " + ledCmd.getStateData())
        logging.info("Status: ALERT (Red)")
        
        # Execute command
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "LED display command should succeed")
        
        # Verify latest response
        latestResponse = self.ledDisplay.getLatestActuatorResponse()
        self.assertEqual(latestResponse.getCommand(), ConfigConst.LED_ALERT_CMD)
        
        logging.info("✓ Alert status displayed successfully")
        
        logging.info("\n✓✓✓ Test PASSED: Alert display working ✓✓✓\n")
    
    # ========================================================================
    # Test 4: Temperature High Alert
    # ========================================================================
    
    def testTemperatureHighAlert(self):
        """
        Test LED display showing high temperature alert.
        """
        logging.info("\n===== Test 4: Temperature High Alert =====\n")
        
        ledCmd = ActuatorData()
        ledCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_ALERT_CMD)
        ledCmd.setStateData("ALERT: TEMP HIGH 78°F!")
        ledCmd.setName("Temp High Alert")
        
        logging.info("Alert: High Temperature")
        logging.info("Message: " + ledCmd.getStateData())
        
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "Temperature high alert should display")
        
        logging.info("✓ High temperature alert displayed")
        
        logging.info("\n✓✓✓ Test PASSED: Temp high alert working ✓✓✓\n")
    
    # ========================================================================
    # Test 5: Temperature Low Alert
    # ========================================================================
    
    def testTemperatureLowAlert(self):
        """
        Test LED display showing low temperature alert.
        """
        logging.info("\n===== Test 5: Temperature Low Alert =====\n")
        
        ledCmd = ActuatorData()
        ledCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_ALERT_CMD)
        ledCmd.setStateData("ALERT: TEMP LOW 62°F!")
        ledCmd.setName("Temp Low Alert")
        
        logging.info("Alert: Low Temperature")
        logging.info("Message: " + ledCmd.getStateData())
        
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "Temperature low alert should display")
        
        logging.info("✓ Low temperature alert displayed")
        
        logging.info("\n✓✓✓ Test PASSED: Temp low alert working ✓✓✓\n")
    
    # ========================================================================
    # Test 6: Humidity Low Alert
    # ========================================================================
    
    def testHumidityLowAlert(self):
        """
        Test LED display showing low humidity alert.
        """
        logging.info("\n===== Test 6: Humidity Low Alert =====\n")
        
        ledCmd = ActuatorData()
        ledCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_ALERT_CMD)
        ledCmd.setStateData("ALERT: HUMIDITY LOW 45%!")
        ledCmd.setName("Humidity Low Alert")
        
        logging.info("Alert: Low Humidity")
        logging.info("Message: " + ledCmd.getStateData())
        
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "Humidity low alert should display")
        
        logging.info("✓ Low humidity alert displayed")
        
        logging.info("\n✓✓✓ Test PASSED: Humidity low alert working ✓✓✓\n")
    
    # ========================================================================
    # Test 7: Profile Change Notification
    # ========================================================================
    
    def testProfileChangeNotification(self):
        """
        Test LED display showing fermentation profile change.
        """
        logging.info("\n===== Test 7: Profile Change Notification =====\n")
        
        profiles = [
            ConfigConst.FERMENTATION_PROFILE_ALE,
            ConfigConst.FERMENTATION_PROFILE_LAGER,
            ConfigConst.FERMENTATION_PROFILE_CONDITIONING,
            ConfigConst.FERMENTATION_PROFILE_COLD_CRASH
        ]
        
        for profile in profiles:
            logging.info(f"\nChanging to {profile} profile")
            
            ledCmd = ActuatorData()
            ledCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
            ledCmd.setCommand(ConfigConst.LED_OPTIMAL_CMD)
            ledCmd.setStateData(f"Profile: {profile}")
            ledCmd.setName("Profile Change")
            
            result = self.ledDisplay.updateActuator(ledCmd)
            
            self.assertTrue(result, f"Profile change to {profile} should display")
            
            logging.info(f"✓ {profile} profile change displayed")
            
            time.sleep(0.3)  # Brief pause between profile changes
        
        logging.info("\n✓✓✓ Test PASSED: Profile changes displayed correctly ✓✓✓\n")
    
    # ========================================================================
    # Test 8: Cooling Active Status
    # ========================================================================
    
    def testCoolingActiveStatus(self):
        """
        Test LED display showing HVAC cooling active status.
        """
        logging.info("\n===== Test 8: Cooling Active Status =====\n")
        
        ledCmd = ActuatorData()
        ledCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_ACTIVE_CMD)
        ledCmd.setStateData("Cooling Active - Temp: 74°F")
        ledCmd.setName("Cooling Status")
        
        logging.info("Status: Cooling system active")
        logging.info("Message: " + ledCmd.getStateData())
        
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "Cooling active status should display")
        
        logging.info("✓ Cooling status displayed")
        
        logging.info("\n✓✓✓ Test PASSED: Cooling status working ✓✓✓\n")
    
    # ========================================================================
    # Test 9: Heating Active Status
    # ========================================================================
    
    def testHeatingActiveStatus(self):
        """
        Test LED display showing HVAC heating active status.
        """
        logging.info("\n===== Test 9: Heating Active Status =====\n")
        
        ledCmd = ActuatorData()
        ledCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_ACTIVE_CMD)
        ledCmd.setStateData("Heating Active - Temp: 64°F")
        ledCmd.setName("Heating Status")
        
        logging.info("Status: Heating system active")
        logging.info("Message: " + ledCmd.getStateData())
        
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "Heating active status should display")
        
        logging.info("✓ Heating status displayed")
        
        logging.info("\n✓✓✓ Test PASSED: Heating status working ✓✓✓\n")
    
    # ========================================================================
    # Test 10: Humidifier Active Status
    # ========================================================================
    
    def testHumidifierActiveStatus(self):
        """
        Test LED display showing humidifier active status.
        """
        logging.info("\n===== Test 10: Humidifier Active Status =====\n")
        
        ledCmd = ActuatorData()
        ledCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_ACTIVE_CMD)
        ledCmd.setStateData("Humidifier Active - Humidity: 52%")
        ledCmd.setName("Humidifier Status")
        
        logging.info("Status: Humidifier active")
        logging.info("Message: " + ledCmd.getStateData())
        
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "Humidifier active status should display")
        
        logging.info("✓ Humidifier status displayed")
        
        logging.info("\n✓✓✓ Test PASSED: Humidifier status working ✓✓✓\n")
    
    # ========================================================================
    # Test 11: Multiple Systems Active
    # ========================================================================
    
    def testMultipleSystemsActive(self):
        """
        Test LED display showing multiple systems active simultaneously.
        """
        logging.info("\n===== Test 11: Multiple Systems Active =====\n")
        
        ledCmd = ActuatorData()
        ledCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_ACTIVE_CMD)
        ledCmd.setStateData("Active: Cooling + Humidifier - 73°F, 55%")
        ledCmd.setName("Multiple Systems")
        
        logging.info("Status: Multiple systems active")
        logging.info("Message: " + ledCmd.getStateData())
        
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "Multiple systems status should display")
        
        logging.info("✓ Multiple systems status displayed")
        
        logging.info("\n✓✓✓ Test PASSED: Multiple systems display working ✓✓✓\n")
    
    # ========================================================================
    # Test 12: Rapid Status Changes
    # ========================================================================
    
    def testRapidStatusChanges(self):
        """
        Test LED display handling rapid status changes.
        """
        logging.info("\n===== Test 12: Rapid Status Changes =====\n")
        
        statuses = [
            (ConfigConst.LED_OPTIMAL_CMD, "Optimal: 70°F, 65%"),
            (ConfigConst.LED_ACTIVE_CMD, "Cooling Active: 73°F"),
            (ConfigConst.LED_ALERT_CMD, "ALERT: HIGH TEMP 78°F!"),
            (ConfigConst.LED_ACTIVE_CMD, "Emergency Cooling: 78°F"),
            (ConfigConst.LED_OPTIMAL_CMD, "Stabilized: 72°F")
        ]
        
        logging.info(f"Testing {len(statuses)} rapid status changes")
        
        for i, (cmd, msg) in enumerate(statuses, 1):
            ledCmd = ActuatorData()
            ledCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
            ledCmd.setCommand(cmd)
            ledCmd.setStateData(msg)
            ledCmd.setName(f"Status Change {i}")
            
            result = self.ledDisplay.updateActuator(ledCmd)
            
            self.assertTrue(result, f"Status change {i} should display")
            
            logging.info(f"  {i}. {cmd}: {msg} ✓")
            
            time.sleep(0.2)  # Brief delay between changes
        
        logging.info(f"\n✓ All {len(statuses)} status changes displayed successfully")
        
        logging.info("\n✓✓✓ Test PASSED: Rapid status changes handled ✓✓✓\n")
    
    # ========================================================================
    # Test 13: Temperature Spike Alert
    # ========================================================================
    
    def testTemperatureSpikeAlert(self):
        """
        Test LED display showing temperature spike detection alert.
        """
        logging.info("\n===== Test 13: Temperature Spike Alert =====\n")
        
        ledCmd = ActuatorData()
        ledCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_ALERT_CMD)
        ledCmd.setStateData("⚠ ALERT: TEMP_SPIKE - Possible infection!")
        ledCmd.setName("Temp Spike Alert")
        
        logging.info("Alert: Temperature spike detected")
        logging.info("Message: " + ledCmd.getStateData())
        
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "Temperature spike alert should display")
        
        logging.info("✓ Temperature spike alert displayed")
        
        logging.info("\n✓✓✓ Test PASSED: Temp spike alert working ✓✓✓\n")
    
    # ========================================================================
    # Test 14: Empty Message Handling
    # ========================================================================
    
    def testEmptyMessageHandling(self):
        """
        Test LED display handling empty or missing messages.
        """
        logging.info("\n===== Test 14: Empty Message Handling =====\n")
        
        # Test with no state data
        ledCmd = ActuatorData()
        ledCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_OPTIMAL_CMD)
        # Don't set state data
        ledCmd.setName("Empty Message Test")
        
        logging.info("Testing display with no message")
        
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "Display should handle empty message gracefully")
        
        logging.info("✓ Empty message handled gracefully")
        
        logging.info("\n✓✓✓ Test PASSED: Empty message handling working ✓✓✓\n")
    
    # ========================================================================
    # Test 15: Long Message Display
    # ========================================================================
    
    def testLongMessageDisplay(self):
        """
        Test LED display with long message text.
        """
        logging.info("\n===== Test 15: Long Message Display =====\n")
        
        longMessage = "Fermentation Active: ALE Profile - Temperature 70.5°F (Target: 68-72°F), Humidity 65% (Target: 60-70%), Pressure 101.3 kPa - All systems optimal"
        
        ledCmd = ActuatorData()
        ledCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_OPTIMAL_CMD)
        ledCmd.setStateData(longMessage)
        ledCmd.setName("Long Message Test")
        
        logging.info("Testing display with long message")
        logging.info(f"Message length: {len(longMessage)} characters")
        
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "Display should handle long message")
        
        logging.info("✓ Long message displayed successfully")
        
        logging.info("\n✓✓✓ Test PASSED: Long message handling working ✓✓✓\n")
    
    # ========================================================================
    # Test 16: Off Command
    # ========================================================================
    
    def testOffCommand(self):
        """
        Test LED display OFF command.
        """
        logging.info("\n===== Test 16: Off Command =====\n")
        
        # First show something
        onCmd = ActuatorData()
        onCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        onCmd.setCommand(ConfigConst.LED_OPTIMAL_CMD)
        onCmd.setStateData("Fermentation Active")
        
        self.ledDisplay.updateActuator(onCmd)
        logging.info("LED display activated")
        
        time.sleep(0.5)
        
        # Now turn off
        offCmd = ActuatorData()
        offCmd.setTypeID(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        offCmd.setCommand(ConfigConst.LED_OFF_CMD)
        offCmd.setStateData("")
        offCmd.setName("LED Off")
        
        logging.info("Sending OFF command")
        
        result = self.ledDisplay.updateActuator(offCmd)
        
        self.assertTrue(result, "OFF command should succeed")
        
        logging.info("✓ LED display turned off")
        
        logging.info("\n✓✓✓ Test PASSED: Off command working ✓✓✓\n")

if __name__ == '__main__':
    """
    Run all LED display fermentation integration tests.
    """
    unittest.main()