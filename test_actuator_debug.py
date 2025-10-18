import sys
sys.path.insert(0, 'src/main/python')

from programmingtheiot.cda.emulated.HumidifierEmulatorTask import HumidifierEmulatorTask
from programmingtheiot.data.ActuatorData import ActuatorData
import programmingtheiot.common.ConfigConst as ConfigConst

print("=== Creating HumidifierEmulatorTask ===")
task = HumidifierEmulatorTask()
print(f"Task created: {task}")
print(f"Task name: {task.getName()}")
print(f"Task simpleName: {task.getSimpleName()}")
print(f"Task typeID: {task.getTypeID()}")

print("\n=== Creating ActuatorData ===")
ad = ActuatorData(typeID=ConfigConst.HUMIDIFIER_ACTUATOR_TYPE)
print(f"ActuatorData created: {ad}")

print("\n=== Setting Command ===")
ad.setCommand(ConfigConst.COMMAND_ON)
print(f"Command set to: {ConfigConst.COMMAND_ON}")

print("\n=== Getting Command ===")
try:
    cmd = ad.getCommand()
    print(f"getCommand() returned: {cmd}")
except Exception as e:
    print(f"ERROR calling getCommand(): {e}")

print("\n=== Setting Value ===")
ad.setValue(50.0)
print(f"Value set to: 50.0")

print("\n=== Getting Value ===")
try:
    val = ad.getValue()
    print(f"getValue() returned: {val}")
except Exception as e:
    print(f"ERROR calling getValue(): {e}")

print("\n=== Getting StateData ===")
try:
    state = ad.getStateData()
    print(f"getStateData() returned: {state}")
except Exception as e:
    print(f"ERROR calling getStateData(): {e}")

print("\n=== Calling updateActuator ===")
try:
    result = task.updateActuator(ad)
    print(f"updateActuator returned: {result}")
    print(f"Result is None: {result is None}")
    
    if result:
        print(f"Result command: {result.getCommand()}")
        print(f"Result value: {result.getValue()}")
        print(f"Result status: {result.getStatusCode()}")
except Exception as e:
    print(f"ERROR calling updateActuator: {e}")
    import traceback
    traceback.print_exc()