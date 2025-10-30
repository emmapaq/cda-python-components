#!/usr/bin/env python3
"""
Constrained Device Application (CDA) Main Entry Point

This is the main entry point for the Constrained Device Application.
It initializes and starts the DeviceDataManager which manages all
sensors, actuators, MQTT connectivity, and CoAP server.

Location: ConstrainedDeviceApp.py (project root)
"""

import logging
import sys
import os
import time

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager

def main():
    """
    Main application entry point.
    
    Creates and starts the DeviceDataManager, then keeps the application
    running until a keyboard interrupt (Ctrl+C) is received.
    """
    logging.info("=" * 70)
    logging.info("Starting Constrained Device Application (CDA)...")
    logging.info("=" * 70)
    
    deviceDataManager = None
    
    try:
        # Create the device data manager
        deviceDataManager = DeviceDataManager()
        
        # Start the manager (this starts all sub-components)
        deviceDataManager.startManager()
        
        # Keep the application running
        logging.info("\n" + "=" * 70)
        logging.info("CDA is running. Press Ctrl+C to stop.")
        logging.info("=" * 70 + "\n")
        
        # Infinite loop to keep application alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        logging.info("\n" + "=" * 70)
        logging.info("Shutdown signal received. Stopping CDA...")
        logging.info("=" * 70)
        
        # Stop the device data manager
        if deviceDataManager:
            deviceDataManager.stopManager()
        
        logging.info("=" * 70)
        logging.info("CDA stopped successfully.")
        logging.info("=" * 70)
        
    except Exception as e:
        logging.error(f"Error starting CDA: {e}", exc_info=True)
        if deviceDataManager:
            deviceDataManager.stopManager()
        sys.exit(1)

if __name__ == "__main__":
    main()
