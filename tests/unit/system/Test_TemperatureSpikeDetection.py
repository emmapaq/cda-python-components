"""
Unit tests for temperature spike detection in fermentation system.

This module tests the temperature spike detection logic used to identify
rapid temperature increases that may indicate fermentation problems such
as infections, equipment failures, or uncontrolled exothermic reactions.

Validation:
- Normal gradual temperature rise (no spike)
- Rapid temperature increase (spike detected)
- Temperature history tracking
- Time-based spike detection
- Threshold sensitivity
- Edge cases (insufficient data, boundary conditions)

@author: Emma
"""

import unittest
import logging
import time

from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.common.ConfigConst import ConfigConst

class Test_TemperatureSpikeDetection(unittest.TestCase):
    """
    Unit tests for temperature spike detection functionality.
    
    This test suite validates that the system can correctly detect
    rapid temperature increases that may indicate problems with
    the fermentation process.
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
        
        logging.info("\n\n===== Temperature Spike Detection Unit Tests =====\n")
    
    def setUp(self):
        """
        Set up each individual test.
        """
        self.deviceDataMgr = DeviceDataManager()
        
        # Clear temperature history
        self.deviceDataMgr.recentTemperatures = []
    
    def tearDown(self):
        """
        Clean up after each test.
        """
        pass
    
    # ========================================================================
    # Test 1: Normal Gradual Temperature Rise (No Spike)
    # ========================================================================
    
    def testNormalTemperatureRise(self):
        """
        Test that normal, gradual temperature increases do not trigger spike detection.
        Simulates typical fermentation temperature rise over time.
        """
        logging.info("\n===== Test 1: Normal Gradual Temperature Rise =====\n")
        
        # Simulate normal temperature rise: 68°F to 70°F over 16 readings (32 minutes)
        baseTemp = 68.0
        tempIncrement = 0.125  # Increase by 0.125°F per reading
        numReadings = 16
        
        currentTime = time.time()
        
        logging.info(f"Simulating {numReadings} temperature readings with gradual increase")
        logging.info(f"Starting temp: {baseTemp}°F, Increment: {tempIncrement}°F per reading")
        
        for i in range(numReadings):
            currentTemp = baseTemp + (i * tempIncrement)
            
            # Add to temperature history with timestamps spread over 30+ minutes
            self.deviceDataMgr.recentTemperatures.append({
                'value': currentTemp,
                'timestamp': currentTime - (1800 - (i * 120))  # 120 sec = 2 min intervals
            })
        
        finalTemp = self.deviceDataMgr.recentTemperatures[-1]['value']
        tempChange = finalTemp - baseTemp
        
        logging.info(f"Temperature change: {baseTemp}°F → {finalTemp}°F (+{tempChange}°F)")
        
        # Check for spike
        spikeDetected = self.deviceDataMgr._detectTemperatureSpike()
        
        self.assertFalse(spikeDetected, 
                        "Spike should NOT be detected for gradual temperature rise")
        
        logging.info(f"✓ No spike detected (correct)")
        logging.info(f"✓ Temperature change ({tempChange}°F) below threshold ({ConfigConst.TEMP_SPIKE_THRESHOLD}°F)")
        
        logging.info("\n✓✓✓ Test PASSED: Normal rise handled correctly ✓✓✓\n")
    
    # ========================================================================
    # Test 2: Rapid Temperature Spike
    # ========================================================================
    
    def testRapidTemperatureSpike(self):
        """
        Test that rapid temperature increases trigger spike detection.
        Simulates potential infection or equipment failure scenario.
        """
        logging.info("\n===== Test 2: Rapid Temperature Spike =====\n")
        
        # Simulate rapid temperature rise: 68°F to 75°F over 16 readings (32 minutes)
        baseTemp = 68.0
        tempIncrement = 0.5  # Increase by 0.5°F per reading = 8°F total
        numReadings = 16
        
        currentTime = time.time()
        
        logging.info(f"Simulating {numReadings} temperature readings with rapid increase")
        logging.info(f"Starting temp: {baseTemp}°F, Increment: {tempIncrement}°F per reading")
        
        for i in range(numReadings):
            currentTemp = baseTemp + (i * tempIncrement)
            
            # Add to temperature history with timestamps spread over 30+ minutes
            self.deviceDataMgr.recentTemperatures.append({
                'value': currentTemp,
                'timestamp': currentTime - (1800 - (i * 120))
            })
        
        finalTemp = self.deviceDataMgr.recentTemperatures[-1]['value']
        tempChange = finalTemp - baseTemp
        
        logging.info(f"Temperature change: {baseTemp}°F → {finalTemp}°F (+{tempChange}°F)")
        
        # Check for spike
        spikeDetected = self.deviceDataMgr._detectTemperatureSpike()
        
        self.assertTrue(spikeDetected, 
                       "Spike SHOULD be detected for rapid temperature rise")
        
        logging.info(f"✓ Spike detected (correct)")
        logging.info(f"✓ Temperature change ({tempChange}°F) exceeds threshold ({ConfigConst.TEMP_SPIKE_THRESHOLD}°F)")
        
        logging.info("\n✓✓✓ Test PASSED: Rapid spike detected correctly ✓✓✓\n")
    
    # ========================================================================
    # Test 3: Insufficient Temperature History
    # ========================================================================
    
    def testInsufficientTemperatureHistory(self):
        """
        Test spike detection with insufficient data points.
        Should return False when not enough readings are available.
        """
        logging.info("\n===== Test 3: Insufficient Temperature History =====\n")
        
        # Add only 1 reading
        self.deviceDataMgr.recentTemperatures.append({
            'value': 70.0,
            'timestamp': time.time()
        })
        
        logging.info("Temperature history: 1 reading only")
        
        # Check for spike
        spikeDetected = self.deviceDataMgr._detectTemperatureSpike()
        
        self.assertFalse(spikeDetected, 
                        "Spike should NOT be detected with insufficient data")
        
        logging.info("✓ No spike detected with insufficient data (correct)")
        
        logging.info("\n✓✓✓ Test PASSED: Insufficient data handled correctly ✓✓✓\n")
    
    # ========================================================================
    # Test 4: Empty Temperature History
    # ========================================================================
    
    def testEmptyTemperatureHistory(self):
        """
        Test spike detection with no temperature history.
        Should return False safely without errors.
        """
        logging.info("\n===== Test 4: Empty Temperature History =====\n")
        
        # Ensure history is empty
        self.deviceDataMgr.recentTemperatures = []
        
        logging.info("Temperature history: Empty")
        
        # Check for spike
        spikeDetected = self.deviceDataMgr._detectTemperatureSpike()
        
        self.assertFalse(spikeDetected, 
                        "Spike should NOT be detected with empty history")
        
        logging.info("✓ No spike detected with empty history (correct)")
        
        logging.info("\n✓✓✓ Test PASSED: Empty history handled correctly ✓✓✓\n")
    
    # ========================================================================
    # Test 5: Temperature Spike at Exact Threshold
    # ========================================================================
    
    def testTemperatureSpikeAtThreshold(self):
        """
        Test spike detection when temperature change exactly equals threshold.
        Should detect spike at boundary condition.
        """
        logging.info("\n===== Test 5: Temperature Spike at Exact Threshold =====\n")
        
        baseTemp = 68.0
        targetTemp = baseTemp + ConfigConst.TEMP_SPIKE_THRESHOLD  # Exactly at threshold
        
        currentTime = time.time()
        
        logging.info(f"Setting temperature change to exactly match threshold: {ConfigConst.TEMP_SPIKE_THRESHOLD}°F")
        
        # Add readings spanning 30+ minutes with exact threshold change
        numReadings = 16
        tempIncrement = ConfigConst.TEMP_SPIKE_THRESHOLD / (numReadings - 1)
        
        for i in range(numReadings):
            currentTemp = baseTemp + (i * tempIncrement)
            
            self.deviceDataMgr.recentTemperatures.append({
                'value': currentTemp,
                'timestamp': currentTime - (1800 - (i * 120))
            })
        
        finalTemp = self.deviceDataMgr.recentTemperatures[-1]['value']
        tempChange = finalTemp - baseTemp
        
        logging.info(f"Temperature change: {baseTemp}°F → {finalTemp:.2f}°F (+{tempChange:.2f}°F)")
        logging.info(f"Threshold: {ConfigConst.TEMP_SPIKE_THRESHOLD}°F")
        
        # Check for spike
        spikeDetected = self.deviceDataMgr._detectTemperatureSpike()
        
        self.assertTrue(spikeDetected, 
                       "Spike SHOULD be detected at exact threshold")
        
        logging.info("✓ Spike detected at threshold boundary (correct)")
        
        logging.info("\n✓✓✓ Test PASSED: Threshold boundary handled correctly ✓✓✓\n")
    
    # ========================================================================
    # Test 6: Temperature Spike Just Below Threshold
    # ========================================================================
    
    def testTemperatureSpikeJustBelowThreshold(self):
        """
        Test spike detection when temperature change is just below threshold.
        Should NOT detect spike.
        """
        logging.info("\n===== Test 6: Temperature Spike Just Below Threshold =====\n")
        
        baseTemp = 68.0
        # Just below threshold (4.9°F when threshold is 5.0°F)
        targetTemp = baseTemp + (ConfigConst.TEMP_SPIKE_THRESHOLD - 0.1)
        
        currentTime = time.time()
        
        logging.info(f"Setting temperature change to just below threshold")
        
        # Add readings spanning 30+ minutes
        numReadings = 16
        tempIncrement = (targetTemp - baseTemp) / (numReadings - 1)
        
        for i in range(numReadings):
            currentTemp = baseTemp + (i * tempIncrement)
            
            self.deviceDataMgr.recentTemperatures.append({
                'value': currentTemp,
                'timestamp': currentTime - (1800 - (i * 120))
            })
        
        finalTemp = self.deviceDataMgr.recentTemperatures[-1]['value']
        tempChange = finalTemp - baseTemp
        
        logging.info(f"Temperature change: {baseTemp}°F → {finalTemp:.2f}°F (+{tempChange:.2f}°F)")
        logging.info(f"Threshold: {ConfigConst.TEMP_SPIKE_THRESHOLD}°F")
        
        # Check for spike
        spikeDetected = self.deviceDataMgr._detectTemperatureSpike()
        
        self.assertFalse(spikeDetected, 
                        "Spike should NOT be detected below threshold")
        
        logging.info("✓ No spike detected below threshold (correct)")
        
        logging.info("\n✓✓✓ Test PASSED: Below threshold handled correctly ✓✓✓\n")
    
    # ========================================================================
    # Test 7: Temperature Decrease (Negative Spike)
    # ========================================================================
    
    def testTemperatureDecrease(self):
        """
        Test spike detection with temperature decrease.
        Should NOT detect spike for temperature drops.
        """
        logging.info("\n===== Test 7: Temperature Decrease =====\n")
        
        baseTemp = 75.0
        targetTemp = 68.0  # Temperature decreasing
        
        currentTime = time.time()
        
        logging.info("Simulating temperature decrease (not a spike)")
        
        numReadings = 16
        tempDecrement = (baseTemp - targetTemp) / (numReadings - 1)
        
        for i in range(numReadings):
            currentTemp = baseTemp - (i * tempDecrement)
            
            self.deviceDataMgr.recentTemperatures.append({
                'value': currentTemp,
                'timestamp': currentTime - (1800 - (i * 120))
            })
        
        finalTemp = self.deviceDataMgr.recentTemperatures[-1]['value']
        tempChange = finalTemp - baseTemp
        
        logging.info(f"Temperature change: {baseTemp}°F → {finalTemp:.2f}°F ({tempChange:.2f}°F)")
        
        # Check for spike
        spikeDetected = self.deviceDataMgr._detectTemperatureSpike()
        
        self.assertFalse(spikeDetected, 
                        "Spike should NOT be detected for temperature decrease")
        
        logging.info("✓ No spike detected for temperature decrease (correct)")
        
        logging.info("\n✓✓✓ Test PASSED: Temperature decrease handled correctly ✓✓✓\n")
    
    # ========================================================================
    # Test 8: Rapid Spike Over Short Time Period
    # ========================================================================
    
    def testRapidSpikeShortPeriod(self):
        """
        Test spike detection with rapid temperature increase over short period.
        Temperature rises quickly but time period is too short (< 30 min).
        """
        logging.info("\n===== Test 8: Rapid Spike Over Short Time Period =====\n")
        
        baseTemp = 68.0
        targetTemp = 78.0  # 10°F increase
        
        currentTime = time.time()
        
        logging.info("Simulating rapid temperature rise over SHORT time period")
        
        # Only 5 readings over 10 minutes (too short for 30-min window)
        numReadings = 5
        tempIncrement = (targetTemp - baseTemp) / (numReadings - 1)
        
        for i in range(numReadings):
            currentTemp = baseTemp + (i * tempIncrement)
            
            # Spread over only 10 minutes (600 seconds)
            self.deviceDataMgr.recentTemperatures.append({
                'value': currentTemp,
                'timestamp': currentTime - (600 - (i * 150))  # 150 sec intervals
            })
        
        finalTemp = self.deviceDataMgr.recentTemperatures[-1]['value']
        tempChange = finalTemp - baseTemp
        timeDelta = (self.deviceDataMgr.recentTemperatures[-1]['timestamp'] - 
                    self.deviceDataMgr.recentTemperatures[0]['timestamp'])
        
        logging.info(f"Temperature change: {baseTemp}°F → {finalTemp:.2f}°F (+{tempChange:.2f}°F)")
        logging.info(f"Time period: {timeDelta:.0f} seconds ({timeDelta/60:.1f} minutes)")
        logging.info(f"Required time period: 1800 seconds (30 minutes)")
        
        # Check for spike
        spikeDetected = self.deviceDataMgr._detectTemperatureSpike()
        
        self.assertFalse(spikeDetected, 
                        "Spike should NOT be detected over short time period")
        
        logging.info("✓ No spike detected for short time period (correct)")
        
        logging.info("\n✓✓✓ Test PASSED: Short time period handled correctly ✓✓✓\n")
    
    # ========================================================================
    # Test 9: Temperature History Tracking
    # ========================================================================
    
    def testTemperatureHistoryTracking(self):
        """
        Test that temperature history is properly tracked and limited.
        Verifies max history size enforcement.
        """
        logging.info("\n===== Test 9: Temperature History Tracking =====\n")
        
        maxHistorySize = self.deviceDataMgr.maxTempHistorySize
        logging.info(f"Max history size: {maxHistorySize} readings")
        
        # Add more readings than max size
        numReadings = maxHistorySize + 10
        logging.info(f"Adding {numReadings} temperature readings")
        
        for i in range(numReadings):
            self.deviceDataMgr._trackTemperatureHistory(68.0 + i)
        
        actualSize = len(self.deviceDataMgr.recentTemperatures)
        
        logging.info(f"Actual history size: {actualSize} readings")
        
        # Verify history doesn't exceed max size
        self.assertLessEqual(actualSize, maxHistorySize, 
                            "History size should not exceed maximum")
        
        logging.info(f"✓ History properly limited to {maxHistorySize} readings")
        
        # Verify oldest readings were removed (FIFO)
        if actualSize == maxHistorySize:
            oldestValue = self.deviceDataMgr.recentTemperatures[0]['value']
            newestValue = self.deviceDataMgr.recentTemperatures[-1]['value']
            
            # Oldest should be from later in sequence (10+)
            self.assertGreater(oldestValue, 68.0 + 9, 
                             "Oldest readings should have been removed")
            
            logging.info(f"✓ FIFO working correctly")
            logging.info(f"  Oldest value: {oldestValue:.1f}°F")
            logging.info(f"  Newest value: {newestValue:.1f}°F")
        
        logging.info("\n✓✓✓ Test PASSED: History tracking working correctly ✓✓✓\n")
    
    # ========================================================================
    # Test 10: Integration with Sensor Data Handler
    # ========================================================================
    
    def testIntegrationWithSensorDataHandler(self):
        """
        Test spike detection integration with sensor data handler.
        Verifies that handleSensorData properly calls spike detection.
        """
        logging.info("\n===== Test 10: Integration with Sensor Data Handler =====\n")
        
        logging.info("Building temperature history through sensor data handler")
        
        # Send series of temperature readings through handleSensorData
        baseTemp = 68.0
        numReadings = 16
        
        for i in range(numReadings):
            tempData = SensorData()
            tempData.setTypeID(ConfigConst.TEMP_SENSOR_TYPE)
            tempData.setValue(baseTemp + (i * 0.5))  # Rising temperature
            tempData.setName("TempSensor")
            
            self.deviceDataMgr.handleSensorData(tempData)
            
            time.sleep(0.05)  # Brief delay to simulate real timing
        
        historySize = len(self.deviceDataMgr.recentTemperatures)
        
        logging.info(f"✓ Temperature history built: {historySize} readings")
        
        self.assertEqual(historySize, numReadings, 
                        "All temperature readings should be tracked")
        
        # Verify temperatures are in history
        firstTemp = self.deviceDataMgr.recentTemperatures[0]['value']
        lastTemp = self.deviceDataMgr.recentTemperatures[-1]['value']
        
        logging.info(f"✓ Temperature range: {firstTemp:.1f}°F → {lastTemp:.1f}°F")
        
        self.assertAlmostEqual(firstTemp, baseTemp, delta=0.1)
        self.assertAlmostEqual(lastTemp, baseTemp + ((numReadings-1) * 0.5), delta=0.1)
        
        logging.info("\n✓✓✓ Test PASSED: Integration working correctly ✓✓✓\n")
    
    # ========================================================================
    # Test 11: Multiple Spike Detection Cycles
    # ========================================================================
    
    def testMultipleSpikeDetectionCycles(self):
        """
        Test spike detection over multiple cycles.
        Simulates normal rise, spike, then return to normal.
        """
        logging.info("\n===== Test 11: Multiple Spike Detection Cycles =====\n")
        
        currentTime = time.time()
        
        # Cycle 1: Normal rise (no spike)
        logging.info("Cycle 1: Normal temperature rise")
        self.deviceDataMgr.recentTemperatures = []
        
        for i in range(10):
            self.deviceDataMgr.recentTemperatures.append({
                'value': 68.0 + (i * 0.2),
                'timestamp': currentTime - (1800 - (i * 180))
            })
        
        spike1 = self.deviceDataMgr._detectTemperatureSpike()
        self.assertFalse(spike1, "No spike should be detected in cycle 1")
        logging.info("✓ Cycle 1: No spike detected (correct)")
        
        # Cycle 2: Rapid spike
        logging.info("\nCycle 2: Rapid temperature spike")
        self.deviceDataMgr.recentTemperatures = []
        
        for i in range(16):
            self.deviceDataMgr.recentTemperatures.append({
                'value': 68.0 + (i * 0.5),
                'timestamp': currentTime - (1800 - (i * 120))
            })
        
        spike2 = self.deviceDataMgr._detectTemperatureSpike()
        self.assertTrue(spike2, "Spike SHOULD be detected in cycle 2")
        logging.info("✓ Cycle 2: Spike detected (correct)")
        
        # Cycle 3: Return to normal
        logging.info("\nCycle 3: Return to normal temperatures")
        self.deviceDataMgr.recentTemperatures = []
        
        for i in range(10):
            self.deviceDataMgr.recentTemperatures.append({
                'value': 70.0 + (i * 0.1),
                'timestamp': currentTime - (1800 - (i * 180))
            })
        
        spike3 = self.deviceDataMgr._detectTemperatureSpike()
        self.assertFalse(spike3, "No spike should be detected in cycle 3")
        logging.info("✓ Cycle 3: No spike detected (correct)")
        
        logging.info("\n✓✓✓ Test PASSED: Multiple cycles handled correctly ✓✓✓\n")
    
    # ========================================================================
    # Test 12: Spike Detection Performance
    # ========================================================================
    
    def testSpikeDetectionPerformance(self):
        """
        Test spike detection performance with many readings.
        Verifies detection runs efficiently.
        """
        logging.info("\n===== Test 12: Spike Detection Performance =====\n")
        
        # Fill history to maximum
        maxSize = self.deviceDataMgr.maxTempHistorySize
        currentTime = time.time()
        
        logging.info(f"Building full temperature history: {maxSize} readings")
        
        for i in range(maxSize):
            self.deviceDataMgr.recentTemperatures.append({
                'value': 68.0 + (i * 0.1),
                'timestamp': currentTime - (1800 - (i * (1800/maxSize)))
            })
        
        # Time the spike detection
        iterations = 1000
        logging.info(f"Running spike detection {iterations} times")
        
        startTime = time.time()
        
        for _ in range(iterations):
            self.deviceDataMgr._detectTemperatureSpike()
        
        endTime = time.time()
        totalTime = endTime - startTime
        avgTime = (totalTime / iterations) * 1000  # Convert to milliseconds
        
        logging.info(f"✓ Total time: {totalTime:.3f} seconds")
        logging.info(f"✓ Average time per detection: {avgTime:.3f} ms")
        
        # Performance assertion (should be very fast)
        self.assertLess(avgTime, 1.0, 
                       "Spike detection should be fast (< 1ms per check)")
        
        logging.info("\n✓✓✓ Test PASSED: Performance acceptable ✓✓✓\n")

if __name__ == '__main__':
    """
    Run all temperature spike detection unit tests.
    """
    unittest.main()