import sys
sys.path.insert(0, 'src/main/python')

from programmingtheiot.cda.emulated.HumiditySensorEmulatorTask import HumiditySensorEmulatorTask
import programmingtheiot.common.ConfigConst as ConfigConst

# Create the task
task = HumiditySensorEmulatorTask()

# Check what getTypeID returns
print(f"Task getTypeID(): {task.getTypeID()}")
print(f"Expected typeID: {ConfigConst.HUMIDITY_SENSOR_TYPE}")

# Generate telemetry
sd = task.generateTelemetry()

# Check the sensor data
print(f"SensorData getName(): {sd.getName()}")
print(f"SensorData getTypeID(): {sd.getTypeID()}")
print(f"SensorData getValue(): {sd.getValue()}")