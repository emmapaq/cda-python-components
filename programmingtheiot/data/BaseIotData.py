"""
Base IoT Data Module

Base class for all IoT data types in the system.
"""

from datetime import datetime

import programmingtheiot.common.ConfigConst as ConfigConst


class BaseIotData:
    """
    Base class for all IoT data containers.
    
    Provides common attributes and methods for sensor data, actuator data,
    system performance data, and other IoT data types.
    """
    
    def __init__(self, name: str = ConfigConst.NOT_SET, typeID: int = ConfigConst.DEFAULT_TYPE_ID):
        """
        Constructor for BaseIotData.
        
        Args:
            name: The name/label for this data instance
            typeID: The type identifier for this data
        """
        self.name = name
        self.typeID = typeID
        self.timeStamp = None
        self.statusCode = ConfigConst.STATUS_OK
        self.hasError = False
        self.locationID = ConfigConst.DEFAULT_LOCATION_ID
        self.latitude = 0.0
        self.longitude = 0.0
        self.elevation = 0.0
        
        self.updateTimeStamp()
    
    def getName(self) -> str:
        """
        Gets the name of this data instance.
        
        Returns:
            str: The name
        """
        return self.name
    
    def getTypeID(self) -> int:
        """
        Gets the type ID of this data instance.
        
        Returns:
            int: The type ID
        """
        return self.typeID
    
    def getTimeStamp(self) -> str:
        """
        Gets the timestamp of this data instance.
        
        Returns:
            str: The timestamp in ISO format
        """
        return self.timeStamp
    
    def getStatusCode(self) -> int:
        """
        Gets the status code.
        
        Returns:
            int: The status code
        """
        return self.statusCode
    
    def getLocationID(self) -> str:
        """
        Gets the location ID.
        
        Returns:
            str: The location ID
        """
        return self.locationID
    
    def getLatitude(self) -> float:
        """
        Gets the latitude coordinate.
        
        Returns:
            float: The latitude
        """
        return self.latitude
    
    def getLongitude(self) -> float:
        """
        Gets the longitude coordinate.
        
        Returns:
            float: The longitude
        """
        return self.longitude
    
    def getElevation(self) -> float:
        """
        Gets the elevation.
        
        Returns:
            float: The elevation in meters
        """
        return self.elevation
    
    def hasErrorFlag(self) -> bool:
        """
        Checks if an error flag is set.
        
        Returns:
            bool: True if error flag is set, False otherwise
        """
        return self.hasError
    
    def setName(self, name: str):
        """
        Sets the name of this data instance.
        
        Args:
            name: The name to set
        """
        self.name = name
        self.updateTimeStamp()
    
    def setTypeID(self, typeID: int):
        """
        Sets the type ID.
        
        Args:
            typeID: The type ID to set
        """
        self.typeID = typeID
        self.updateTimeStamp()
    
    def setStatusCode(self, statusCode: int):
        """
        Sets the status code.
        
        Args:
            statusCode: The status code to set
        """
        self.statusCode = statusCode
        self.updateTimeStamp()
    
    def setLocationID(self, locationID: str):
        """
        Sets the location ID.
        
        Args:
            locationID: The location ID to set
        """
        self.locationID = locationID
        self.updateTimeStamp()
    
    def setLatitude(self, latitude: float):
        """
        Sets the latitude coordinate.
        
        Args:
            latitude: The latitude to set
        """
        self.latitude = latitude
        self.updateTimeStamp()
    
    def setLongitude(self, longitude: float):
        """
        Sets the longitude coordinate.
        
        Args:
            longitude: The longitude to set
        """
        self.longitude = longitude
        self.updateTimeStamp()
    
    def setElevation(self, elevation: float):
        """
        Sets the elevation.
        
        Args:
            elevation: The elevation to set in meters
        """
        self.elevation = elevation
        self.updateTimeStamp()
    
    def setErrorFlag(self, hasError: bool):
        """
        Sets the error flag.
        
        Args:
            hasError: True to set error flag, False to clear it
        """
        self.hasError = hasError
        self.updateTimeStamp()
    
    def updateTimeStamp(self):
        """
        Updates the timestamp to the current time in ISO format.
        """
        self.timeStamp = datetime.now().astimezone().isoformat()
    
    def updateData(self, data):
        """
        Updates this instance with data from another instance.
        
        Args:
            data: Another BaseIotData instance to copy from
        """
        if data and isinstance(data, BaseIotData):
            self.name = data.getName()
            self.typeID = data.getTypeID()
            self.timeStamp = data.getTimeStamp()
            self.statusCode = data.getStatusCode()
            self.hasError = data.hasErrorFlag()
            self.locationID = data.getLocationID()
            self.latitude = data.getLatitude()
            self.longitude = data.getLongitude()
            self.elevation = data.getElevation()
            
            # Call subclass-specific update method
            self._handleUpdateData(data)
    
    def _handleUpdateData(self, data):
        """
        Template method for subclasses to handle additional update logic.
        
        Args:
            data: The source data instance
        """
        pass
    
    def __str__(self) -> str:
        """
        Returns a string representation of this data instance.
        
        Returns:
            str: String representation
        """
        return f"BaseIotData(name={self.name}, typeID={self.typeID}, timestamp={self.timeStamp}, statusCode={self.statusCode})"