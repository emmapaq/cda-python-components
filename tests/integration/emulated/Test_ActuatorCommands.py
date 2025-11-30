"""
Integration tests for actuator command generation and processing.

This module tests the creation, validation, and execution of actuator
commands for the fermentation control system, including HVAC control,
humidifier control, and LED display updates.

Validation:
- HVAC cooling command generation and execution
- HVAC heating command generation and execution
- HVAC off command generation and execution
- Humidifier ON/OFF commands
- LED display commands with different states
- Command parameter validation
- Multiple actuator coordination

@author: Emma
"""

# Standard imports
import unittest
import logging
import time

# PIOT imports - these should work now
from programmingtheiot.common.ConfigConst import ConfigConst
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager
from ConstrainedDeviceApp import ConstrainedDeviceApp
from programmingtheiot.cda.emulated.HvacEmulatorTask import HvacEmulatorTask
from programmingtheiot.cda.emulated.HumidifierEmulatorTask import HumidifierEmulatorTask 
from programmingtheiot.cda.emulated.LedDisplayEmulatorTask import LedDisplayEmulatorTask

class Test_ActuatorCommands(unittest.TestCase):
    """
    Integration tests for actuator command handling.
    
    This test suite validates that actuator commands are correctly
    generated, formatted, and executed by the emulated actuators.
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
        
        logging.info("\n\n===== Actuator Command Integration Tests =====\n")
        
        # Create actuator instances
        cls.hvacActuator = HvacEmulatorTask()
        cls.humidifierActuator = HumidifierEmulatorTask()
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
        time.sleep(0.3)  # Brief pause between tests
    
    # ========================================================================
    # Test 1: HVAC Cooling Command
    # ========================================================================
    
    def testHvacCoolingCommand(self):
        """
        Test HVAC cooling command generation and execution.
        """
        logging.info("\n===== Test 1: HVAC Cooling Command =====\n")
        
        # Create cooling command
        coolingCmd = ActuatorData()
        coolingCmd.setActuatorType(ConfigConst.HVAC_ACTUATOR_TYPE)
        coolingCmd.setCommand(ConfigConst.HVAC_COOLING_CMD)
        coolingCmd.setValue(1.0)
        coolingCmd.setName("HVAC Cooling")
        
        logging.info(f"Command: {coolingCmd.getCommand()}")
        logging.info(f"Value: {coolingCmd.getValue()}")
        
        # Execute command
        result = self.hvacActuator.updateActuator(coolingCmd)
        
        self.assertTrue(result, "HVAC cooling command failed")
        
        logging.info("✓ HVAC cooling command executed successfully")
        
        # Verify actuator state
        self.assertEqual(self.hvacActuator.getLatestActuatorResponse().getCommand(), 
                        ConfigConst.HVAC_COOLING_CMD)
        self.assertEqual(self.hvacActuator.getLatestActuatorResponse().getValue(), 1.0)
        
        logging.info("\n✓ Test PASSED: HVAC cooling command working\n")
    
    # ========================================================================
    # Test 2: HVAC Heating Command
    # ========================================================================
    
    def testHvacHeatingCommand(self):
        """
        Test HVAC heating command generation and execution.
        """
        logging.info("\n===== Test 2: HVAC Heating Command =====\n")
        
        # Create heating command
        heatingCmd = ActuatorData()
        heatingCmd.setActuatorType(ConfigConst.HVAC_ACTUATOR_TYPE)
        heatingCmd.setCommand(ConfigConst.HVAC_HEATING_CMD)
        heatingCmd.setValue(1.0)
        heatingCmd.setName("HVAC Heating")
        
        logging.info(f"Command: {heatingCmd.getCommand()}")
        logging.info(f"Value: {heatingCmd.getValue()}")
        
        # Execute command
        result = self.hvacActuator.updateActuator(heatingCmd)
        
        self.assertTrue(result, "HVAC heating command failed")
        
        logging.info("✓ HVAC heating command executed successfully")
        
        # Verify actuator state
        self.assertEqual(self.hvacActuator.getLatestActuatorResponse().getCommand(), 
                        ConfigConst.HVAC_HEATING_CMD)
        self.assertEqual(self.hvacActuator.getLatestActuatorResponse().getValue(), 1.0)
        
        logging.info("\n✓ Test PASSED: HVAC heating command working\n")
    
    # ========================================================================
    # Test 3: HVAC Off Command
    # ========================================================================
    
    def testHvacOffCommand(self):
        """
        Test HVAC off command generation and execution.
        """
        logging.info("\n===== Test 3: HVAC Off Command =====\n")
        
        # First turn on heating
        heatingCmd = ActuatorData()
        heatingCmd.setActuatorType(ConfigConst.HVAC_ACTUATOR_TYPE)
        heatingCmd.setCommand(ConfigConst.HVAC_HEATING_CMD)
        heatingCmd.setValue(1.0)
        
        self.hvacActuator.updateActuator(heatingCmd)
        logging.info("HVAC heating activated")
        
        time.sleep(0.5)
        
        # Now turn off
        offCmd = ActuatorData()
        offCmd.setActuatorType(ConfigConst.HVAC_ACTUATOR_TYPE)
        offCmd.setCommand(ConfigConst.HVAC_OFF_CMD)
        offCmd.setValue(0.0)
        offCmd.setName("HVAC Off")
        
        logging.info(f"Command: {offCmd.getCommand()}")
        logging.info(f"Value: {offCmd.getValue()}")
        
        # Execute command
        result = self.hvacActuator.updateActuator(offCmd)
        
        self.assertTrue(result, "HVAC off command failed")
        
        logging.info("✓ HVAC off command executed successfully")
        
        # Verify actuator state
        self.assertEqual(self.hvacActuator.getLatestActuatorResponse().getCommand(), 
                        ConfigConst.HVAC_OFF_CMD)
        self.assertEqual(self.hvacActuator.getLatestActuatorResponse().getValue(), 0.0)
        
        logging.info("\n✓ Test PASSED: HVAC off command working\n")
    
    # ========================================================================
    # Test 4: Humidifier ON Command
    # ========================================================================
    
    def testHumidifierOnCommand(self):
        """
        Test humidifier ON command generation and execution.
        """
        logging.info("\n===== Test 4: Humidifier ON Command =====\n")
        
        # Create ON command
        onCmd = ActuatorData()
        onCmd.setActuatorType(ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
        onCmd.setCommand(ConfigConst.HUMIDIFIER_ON_CMD)
        onCmd.setValue(1.0)
        onCmd.setName("Humidifier ON")
        
        logging.info(f"Command: {onCmd.getCommand()}")
        logging.info(f"Value: {onCmd.getValue()}")
        
        # Execute command
        result = self.humidifierActuator.updateActuator(onCmd)
        
        self.assertTrue(result, "Humidifier ON command failed")
        
        logging.info("✓ Humidifier ON command executed successfully")
        
        # Verify actuator state
        self.assertEqual(self.humidifierActuator.getLatestActuatorResponse().getCommand(), 
                        ConfigConst.HUMIDIFIER_ON_CMD)
        self.assertEqual(self.humidifierActuator.getLatestActuatorResponse().getValue(), 1.0)
        
        logging.info("\n✓ Test PASSED: Humidifier ON command working\n")
    
    # ========================================================================
    # Test 5: Humidifier OFF Command
    # ========================================================================
    
    def testHumidifierOffCommand(self):
        """
        Test humidifier OFF command generation and execution.
        """
        logging.info("\n===== Test 5: Humidifier OFF Command =====\n")
        
        # First turn on
        onCmd = ActuatorData()
        onCmd.setActuatorType(ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
        onCmd.setCommand(ConfigConst.HUMIDIFIER_ON_CMD)
        onCmd.setValue(1.0)
        
        self.humidifierActuator.updateActuator(onCmd)
        logging.info("Humidifier activated")
        
        time.sleep(0.5)
        
        # Now turn off
        offCmd = ActuatorData()
        offCmd.setActuatorType(ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
        offCmd.setCommand(ConfigConst.HUMIDIFIER_OFF_CMD)
        offCmd.setValue(0.0)
        offCmd.setName("Humidifier OFF")
        
        logging.info(f"Command: {offCmd.getCommand()}")
        logging.info(f"Value: {offCmd.getValue()}")
        
        # Execute command
        result = self.humidifierActuator.updateActuator(offCmd)
        
        self.assertTrue(result, "Humidifier OFF command failed")
        
        logging.info("✓ Humidifier OFF command executed successfully")
        
        # Verify actuator state
        self.assertEqual(self.humidifierActuator.getLatestActuatorResponse().getCommand(), 
                        ConfigConst.HUMIDIFIER_OFF_CMD)
        self.assertEqual(self.humidifierActuator.getLatestActuatorResponse().getValue(), 0.0)
        
        logging.info("\n✓ Test PASSED: Humidifier OFF command working\n")
    
    # ========================================================================
    # Test 6: LED Display Optimal Status
    # ========================================================================
    
    def testLedDisplayOptimalStatus(self):
        """
        Test LED display with optimal status (green).
        """
        logging.info("\n===== Test 6: LED Display Optimal Status =====\n")
        
        # Create optimal status command
        ledCmd = ActuatorData()
        ledCmd.setActuatorType(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_OPTIMAL_CMD)
        ledCmd.setStateData("Temp: 70.0°F, Humidity: 65% - OPTIMAL")
        ledCmd.setName("LED Display")
        
        logging.info(f"Command: {ledCmd.getCommand()}")
        logging.info(f"Message: {ledCmd.getStateData()}")
        
        # Execute command
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "LED optimal display command failed")
        
        logging.info("✓ LED optimal status displayed successfully")
        
        logging.info("\n✓ Test PASSED: LED optimal display working\n")
    
    # ========================================================================
    # Test 7: LED Display Active Status
    # ========================================================================
    
    def testLedDisplayActiveStatus(self):
        """
        Test LED display with active fermentation status (yellow).
        """
        logging.info("\n===== Test 7: LED Display Active Status =====\n")
        
        # Create active status command
        ledCmd = ActuatorData()
        ledCmd.setActuatorType(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_ACTIVE_CMD)
        ledCmd.setStateData("Fermenting: Temp Rising - 73.5°F")
        ledCmd.setName("LED Display")
        
        logging.info(f"Command: {ledCmd.getCommand()}")
        logging.info(f"Message: {ledCmd.getStateData()}")
        
        # Execute command
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "LED active display command failed")
        
        logging.info("✓ LED active status displayed successfully")
        
        logging.info("\n✓ Test PASSED: LED active display working\n")
    
    # ========================================================================
    # Test 8: LED Display Alert Status
    # ========================================================================
    
    def testLedDisplayAlertStatus(self):
        """
        Test LED display with alert status (red).
        """
        logging.info("\n===== Test 8: LED Display Alert Status =====\n")
        
        # Create alert status command
        ledCmd = ActuatorData()
        ledCmd.setActuatorType(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_ALERT_CMD)
        ledCmd.setStateData("⚠ ALERT: Temperature Critical - 85°F!")
        ledCmd.setName("LED Display")
        
        logging.info(f"Command: {ledCmd.getCommand()}")
        logging.info(f"Message: {ledCmd.getStateData()}")
        
        # Execute command
        result = self.ledDisplay.updateActuator(ledCmd)
        
        self.assertTrue(result, "LED alert display command failed")
        
        logging.info("✓ LED alert status displayed successfully")
        
        logging.info("\n✓ Test PASSED: LED alert display working\n")
    
    # ========================================================================
    # Test 9: Emergency HVAC Commands
    # ========================================================================
    
    def testEmergencyHvacCommands(self):
        """
        Test emergency HVAC commands with higher power values.
        """
        logging.info("\n===== Test 9: Emergency HVAC Commands =====\n")
        
        # Test emergency cooling
        logging.info("Testing emergency cooling")
        emergencyCooling = ActuatorData()
        emergencyCooling.setActuatorType(ConfigConst.HVAC_ACTUATOR_TYPE)
        emergencyCooling.setCommand(ConfigConst.HVAC_COOLING_CMD)
        emergencyCooling.setValue(2.0)  # Emergency power level
        emergencyCooling.setName("Emergency Cooling")
        
        result = self.hvacActuator.updateActuator(emergencyCooling)
        self.assertTrue(result, "Emergency cooling command failed")
        
        logging.info(f"✓ Emergency cooling: Power level {emergencyCooling.getValue()}")
        
        time.sleep(0.5)
        
        # Test emergency heating
        logging.info("\nTesting emergency heating")
        emergencyHeating = ActuatorData()
        emergencyHeating.setActuatorType(ConfigConst.HVAC_ACTUATOR_TYPE)
        emergencyHeating.setCommand(ConfigConst.HVAC_HEATING_CMD)
        emergencyHeating.setValue(2.0)  # Emergency power level
        emergencyHeating.setName("Emergency Heating")
        
        result = self.hvacActuator.updateActuator(emergencyHeating)
        self.assertTrue(result, "Emergency heating command failed")
        
        logging.info(f"✓ Emergency heating: Power level {emergencyHeating.getValue()}")
        
        logging.info("\n✓ Test PASSED: Emergency HVAC commands working\n")
    
    # ========================================================================
    # Test 10: Multiple Actuator Coordination
    # ========================================================================
    
    def testMultipleActuatorCoordination(self):
        """
        Test coordination of multiple actuators simultaneously.
        """
        logging.info("\n===== Test 10: Multiple Actuator Coordination =====\n")
        
        # Activate HVAC cooling
        logging.info("Activating HVAC cooling")
        hvacCmd = ActuatorData()
        hvacCmd.setActuatorType(ConfigConst.HVAC_ACTUATOR_TYPE)
        hvacCmd.setCommand(ConfigConst.HVAC_COOLING_CMD)
        hvacCmd.setValue(1.0)
        
        result1 = self.hvacActuator.updateActuator(hvacCmd)
        self.assertTrue(result1, "HVAC command failed")
        
        # Activate humidifier
        logging.info("Activating humidifier")
        humidCmd = ActuatorData()
        humidCmd.setActuatorType(ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
        humidCmd.setCommand(ConfigConst.HUMIDIFIER_ON_CMD)
        humidCmd.setValue(1.0)
        
        result2 = self.humidifierActuator.updateActuator(humidCmd)
        self.assertTrue(result2, "Humidifier command failed")
        
        # Update LED display
        logging.info("Updating LED display")
        ledCmd = ActuatorData()
        ledCmd.setActuatorType(ConfigConst.LED_DISPLAY_ACTUATOR_TYPE)
        ledCmd.setCommand(ConfigConst.LED_ACTIVE_CMD)
        ledCmd.setStateData("Multiple systems active - Cooling + Humidifying")
        
        result3 = self.ledDisplay.updateActuator(ledCmd)
        self.assertTrue(result3, "LED command failed")
        
        logging.info("✓ All actuators coordinated successfully")
        logging.info("  - HVAC: Cooling")
        logging.info("  - Humidifier: ON")
        logging.info("  - LED: Active status")
        
        logging.info("\n✓ Test PASSED: Multiple actuator coordination working\n")
    
    # ========================================================================
    # Test 11: Actuator Command Validation
    # ========================================================================
    
    def testActuatorCommandValidation(self):
        """
        Test that invalid actuator commands are handled properly.
        """
        logging.info("\n===== Test 11: Actuator Command Validation =====\n")
        
        # Test with None command
        logging.info("Testing None command")
        result = self.hvacActuator.updateActuator(None)
        self.assertFalse(result, "None command should be rejected")
        logging.info("✓ None command rejected correctly")
        
        # Test with empty ActuatorData
        logging.info("\nTesting empty ActuatorData")
        emptyCmd = ActuatorData()
        # Don't set any properties
        
        result = self.hvacActuator.updateActuator(emptyCmd)
        # Should handle gracefully (may return True or False depending on implementation)
        logging.info(f"✓ Empty command handled: result={result}")
        
        logging.info("\n✓ Test PASSED: Command validation working\n")
    
    # ========================================================================
    # Test 12: Rapid Command Sequence
    # ========================================================================
    
    def testRapidCommandSequence(self):
        """
        Test rapid sequence of actuator commands.
        """
        logging.info("\n===== Test 12: Rapid Command Sequence =====\n")
        
        commands = [
            (ConfigConst.HVAC_COOLING_CMD, 1.0),
            (ConfigConst.HVAC_OFF_CMD, 0.0),
            (ConfigConst.HVAC_HEATING_CMD, 1.0),
            (ConfigConst.HVAC_OFF_CMD, 0.0),
            (ConfigConst.HVAC_COOLING_CMD, 1.0)
        ]
        
        logging.info(f"Executing {len(commands)} rapid commands")
        
        for i, (cmd, value) in enumerate(commands, 1):
            actuatorCmd = ActuatorData()
            actuatorCmd.setActuatorType(ConfigConst.HVAC_ACTUATOR_TYPE)
            actuatorCmd.setCommand(cmd)
            actuatorCmd.setValue(value)
            
            result = self.hvacActuator.updateActuator(actuatorCmd)
            self.assertTrue(result, f"Command {i} failed")
            
            logging.info(f"  {i}. {cmd} (value={value}) ✓")
            
            time.sleep(0.1)  # Brief delay between commands
        
        logging.info(f"✓ All {len(commands)} commands executed successfully")
        
        logging.info("\n✓ Test PASSED: Rapid command sequence handled\n")

if __name__ == '__main__':
    """
    Run all actuator command integration tests.
    """
    unittest.main()