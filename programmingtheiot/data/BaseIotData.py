import time
import logging

class BaseIotData():
	"""
	Base class for all IoT data containers.
	Provides common properties and methods shared across all data types.
	"""
	
	DEFAULT_NAME = "DefaultIoTData"
	DEFAULT_TYPE_ID = 0
	DEFAULT_STATUS_CODE = 0
	DEFAULT_LOCATION_ID = "constraineddevice001"
	
	def __init__(self, name=DEFAULT_NAME, typeID=DEFAULT_TYPE_ID, d=None):
		"""
		Constructor for BaseIotData.
		
		@param name The name of the data instance.
		@param typeID The type ID of the data.
		@param d Optional BaseIotData instance to copy from.
		"""
		# CRITICAL: Store timestamp as numeric (milliseconds since epoch)
		# This matches the Java implementation and ensures cross-platform compatibility
		self.timeStamp = self._getCurrentTimeStamp()
		
		self.hasError = False
		self.name = name
		self.typeID = typeID
		self.statusCode = self.DEFAULT_STATUS_CODE
		self.latitude = 0.0
		self.longitude = 0.0
		self.elevation = 0.0
		self.locationID = self.DEFAULT_LOCATION_ID
		
		if d:
			self.updateData(d)
	
	def _getCurrentTimeStamp(self) -> int:
		"""
		Gets the current timestamp as milliseconds since epoch.
		This matches the Java implementation format.
		
		@return Current timestamp in milliseconds (integer).
		"""
		# IMPORTANT: Return as integer milliseconds, NOT as ISO string
		return int(time.time() * 1000)
	
	def updateTimeStamp(self):
		"""
		Updates the timestamp to the current time.
		"""
		self.timeStamp = self._getCurrentTimeStamp()
	
	def getTimeStamp(self) -> int:
		"""
		Returns the timestamp.
		
		@return Timestamp in milliseconds since epoch.
		"""
		return self.timeStamp
	
	def setTimeStamp(self, timeStamp: int):
		"""
		Sets the timestamp.
		
		@param timeStamp Timestamp in milliseconds since epoch.
		"""
		self.timeStamp = timeStamp
	
	def getName(self) -> str:
		"""
		Returns the name of this data instance.
		
		@return The name.
		"""
		return self.name
	
	def setName(self, name: str):
		"""
		Sets the name of this data instance.
		
		@param name The name to set.
		"""
		self.name = name
	
	def getTypeID(self) -> int:
		"""
		Returns the type ID.
		
		@return The type ID.
		"""
		return self.typeID
	
	def setTypeID(self, typeID: int):
		"""
		Sets the type ID.
		
		@param typeID The type ID to set.
		"""
		self.typeID = typeID
	
	def getStatusCode(self) -> int:
		"""
		Returns the status code.
		
		@return The status code.
		"""
		return self.statusCode
	
	def setStatusCode(self, statusCode: int):
		"""
		Sets the status code.
		
		@param statusCode The status code to set.
		"""
		self.updateTimeStamp()
		self.statusCode = statusCode
	
	def getLocationID(self) -> str:
		"""
		Returns the location ID.
		
		@return The location ID.
		"""
		return self.locationID
	
	def setLocationID(self, locationID: str):
		"""
		Sets the location ID.
		
		@param locationID The location ID to set.
		"""
		self.locationID = locationID
	
	def hasErrorFlag(self) -> bool:
		"""
		Returns the error flag.
		
		@return True if error flag is set, False otherwise.
		"""
		return self.hasError
	
	def setErrorFlag(self, hasError: bool):
		"""
		Sets the error flag.
		
		@param hasError The error flag value.
		"""
		self.hasError = hasError
	
	def getLatitude(self) -> float:
		"""
		Returns the latitude.
		
		@return The latitude.
		"""
		return self.latitude
	
	def setLatitude(self, latitude: float):
		"""
		Sets the latitude.
		
		@param latitude The latitude to set.
		"""
		self.latitude = latitude
	
	def getLongitude(self) -> float:
		"""
		Returns the longitude.
		
		@return The longitude.
		"""
		return self.longitude
	
	def setLongitude(self, longitude: float):
		"""
		Sets the longitude.
		
		@param longitude The longitude to set.
		"""
		self.longitude = longitude
	
	def getElevation(self) -> float:
		"""
		Returns the elevation.
		
		@return The elevation.
		"""
		return self.elevation
	
	def setElevation(self, elevation: float):
		"""
		Sets the elevation.
		
		@param elevation The elevation to set.
		"""
		self.elevation = elevation
	
	def updateData(self, data):
		"""
		Updates this instance with data from another BaseIotData instance.
		
		@param data The BaseIotData instance to copy from.
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
			
			self._handleUpdateData(data)
	
	def _handleUpdateData(self, data):
		"""
		Template method for subclasses to implement additional update logic.
		
		@param data The data instance to update from.
		"""
		pass
	
	def __str__(self):
		"""
		Returns a string representation of this data instance.
		
		@return String representation.
		"""
		return f"name={self.name},typeID={self.typeID},timeStamp={self.timeStamp},statusCode={self.statusCode},hasError={self.hasError},locationID={self.locationID},elevation={self.elevation},latitude={self.latitude},longitude={self.longitude}"