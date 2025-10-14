"""
Constrained Device Application

Main application entry point for the Constrained Device Application (CDA).
This application manages device data collection, processing, and communication
with cloud services via MQTT.
"""

import logging
import sys

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.app.DeviceDataManager import DeviceDataManager


class ConstrainedDeviceApp():
    """
    Main application class for the Constrained Device Application.
    
    Initializes and manages the device data manager, handling startup,
    runtime operations, and shutdown procedures.
    """
    
    def __init__(self):
        """
        Constructor for ConstrainedDeviceApp.
        
        Initializes logging and creates the DeviceDataManager instance.
        """
        logging.info("Initializing Constrained Device Application...")
        
        self.configUtil = ConfigUtil()
        self.deviceDataManager = DeviceDataManager()
        
        logging.info("Constrained Device Application initialized successfully")
    
    def startApp(self):
        """
        Starts the Constrained Device Application.
        
        Initiates the DeviceDataManager, which in turn starts all
        subsystems including MQTT connectivity, sensor monitoring,
        and actuator management.
        """
        logging.info("=" * 80)
        logging.info("Starting Constrained Device Application...")
        logging.info("=" * 80)
        
        try:
            self.deviceDataManager.startManager()
            logging.info("Constrained Device Application started successfully")
            logging.info("Application is now running. Press Ctrl+C to stop.")
            
        except Exception as e:
            logging.error(f"Failed to start Constrained Device Application: {e}")
            raise
    
    def stopApp(self, code: int = 0):
        """
        Stops the Constrained Device Application.
        
        Gracefully shuts down all subsystems including MQTT connections,
        sensor monitoring, and actuator management.
        
        Args:
            code: Exit code (default: 0 for normal termination)
        """
        logging.info("=" * 80)
        logging.info("Stopping Constrained Device Application...")
        logging.info("=" * 80)
        
        try:
            self.deviceDataManager.stopManager()
            logging.info("Constrained Device Application stopped successfully")
            
        except Exception as e:
            logging.error(f"Error during application shutdown: {e}")
            
        finally:
            logging.info("=" * 80)
            logging.info("Constrained Device Application terminated")
            logging.info("=" * 80)
            sys.exit(code)
    
    def parseArgs(self, args):
        """
        Parse command line arguments.
        
        Args:
            args: Command line arguments
        """
        # Placeholder for future command line argument parsing
        logging.info(f"Parsing command line args: {args}")


def main():
    """
    Main entry point for the Constrained Device Application.
    
    Sets up logging, creates the application instance, and manages
    the application lifecycle.
    """
    # Configure logging
    logging.basicConfig(
        format='%(asctime)s:%(name)s:%(levelname)s:%(message)s',
        level=logging.INFO
    )
    
    logging.info("=" * 80)
    logging.info("Constrained Device Application - Starting Up")
    logging.info("=" * 80)
    
    # Create application instance
    cda = ConstrainedDeviceApp()
    
    try:
        # Start the application
        cda.startApp()
        
        # Keep the application running
        # In a production environment, you might want to add signal handlers
        # for graceful shutdown on SIGTERM, SIGINT, etc.
        while True:
            sleep(5)
            
    except KeyboardInterrupt:
        logging.info("\nKeyboard interrupt detected")
        
    except Exception as e:
        logging.error(f"Unexpected error in main application: {e}", exc_info=True)
        
    finally:
        # Stop the application
        cda.stopApp()


if __name__ == '__main__':
    """
    Script execution entry point.
    
    Usage:
        python ConstrainedDeviceApp.py
    """
    main()