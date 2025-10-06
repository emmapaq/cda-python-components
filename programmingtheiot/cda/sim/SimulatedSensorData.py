import random

class SensorDataGenerator:
    # Normal ranges for simulated environmental data
    LOW_NORMAL_ENV_HUMIDITY = 30.0
    HI_NORMAL_ENV_HUMIDITY = 70.0

    LOW_NORMAL_ENV_PRESSURE = 980.0
    HI_NORMAL_ENV_PRESSURE = 1050.0

    LOW_NORMAL_INDOOR_TEMP = 18.0
    HI_NORMAL_INDOOR_TEMP = 28.0

    def __init__(self):
        pass

    # Generate daily humidity data
    def generateDailyEnvironmentHumidityDataSet(self, minValue=None, maxValue=None, useSeconds=False):
        minValue = minValue or self.LOW_NORMAL_ENV_HUMIDITY
        maxValue = maxValue or self.HI_NORMAL_ENV_HUMIDITY
        return [random.uniform(minValue, maxValue) for _ in range(24)]

    # Generate daily pressure data
    def generateDailyEnvironmentPressureDataSet(self, minValue=None, maxValue=None, useSeconds=False):
        minValue = minValue or self.LOW_NORMAL_ENV_PRESSURE
        maxValue = maxValue or self.HI_NORMAL_ENV_PRESSURE
        return [random.uniform(minValue, maxValue) for _ in range(24)]

    # Generate daily indoor temperature data
    def generateDailyIndoorTemperatureDataSet(self, minValue=None, maxValue=None, useSeconds=False):
        minValue = minValue or self.LOW_NORMAL_INDOOR_TEMP
        maxValue = maxValue or self.HI_NORMAL_INDOOR_TEMP
        return [random.uniform(minValue, maxValue) for _ in range(24)]
