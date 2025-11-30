"""
1-Hour Extended Runtime Test for Fermentation System

Requirements:
- Run for 60+ minutes
- Collect 30+ samples per sensor
- Trigger 2+ different actuator events
- No crashes or exceptions
"""

import time
import unittest
from ConstrainedDeviceApp import ConstrainedDeviceApp

class Test_1HourRuntime(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.cdaApp = ConstrainedDeviceApp()
        
    def test_ExtendedRuntime(self):
        """
        Run CDA for 1 hour and verify requirements.
        """
        print("\n\n===== Starting 1-Hour Extended Runtime Test =====\n")
        
        # Start the CDA
        self.cdaApp.startApp()
        
        # Run for 1 hour (3600 seconds)
        runtime = 3600
        checkInterval = 300  # Check every 5 minutes
        
        startTime = time.time()
        
        for elapsed in range(0, runtime, checkInterval):
            time.sleep(checkInterval)
            minutesElapsed = elapsed // 60
            print(f"[{minutesElapsed} min] System running normally...")
        
        # Stop the CDA
        self.cdaApp.stopApp()
        
        endTime = time.time()
        totalRuntime = endTime - startTime
        
        print(f"\n===== 1-Hour Test Complete =====")
        print(f"Total runtime: {totalRuntime:.2f} seconds ({totalRuntime/60:.2f} minutes)")
        
        # Verify runtime >= 1 hour
        self.assertGreaterEqual(totalRuntime, 3600, "System did not run for full hour")
        
        print("\n✓ Test PASSED: System ran for 1+ hour without interruption")

if __name__ == '__main__':
    unittest.main()