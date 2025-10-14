"""
MqttClientConnector module for handling MQTT pub/sub operations.

This module provides MQTT client connectivity for the Constrained Device Application (CDA),
implementing the IPubSubClient interface using the Paho MQTT client library.

@author: Your Name
"""

import logging
import paho.mqtt.client as mqttClient

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.IPubSubClient import IPubSubClient


class MqttClientConnector(IPubSubClient):
    """
    MQTT client connector implementation using Paho MQTT.
    
    Handles connection, disconnection, publishing, and subscribing to MQTT broker.
    Implements callback mechanisms for message handling and connection events.
    """
    
    def __init__(self, clientID: str = None):
        """
        Constructor for MqttClientConnector.
        
        Initializes MQTT client properties from configuration file and sets up
        the client ID. If no clientID is provided, it will be read from config
        or use a default value.
        
        Args:
            clientID (str): Optional custom client ID for MQTT connection
        """
        self.config = ConfigUtil()
        self.dataMsgListener = None
        
        # Load MQTT broker configuration
        self.host = \
            self.config.getProperty(
                ConfigConst.MQTT_GATEWAY_SERVICE, 
                ConfigConst.HOST_KEY, 
                ConfigConst.DEFAULT_HOST)
        
        self.port = \
            self.config.getInteger(
                ConfigConst.MQTT_GATEWAY_SERVICE, 
                ConfigConst.PORT_KEY, 
                ConfigConst.DEFAULT_MQTT_PORT)
        
        self.keepAlive = \
            self.config.getInteger(
                ConfigConst.MQTT_GATEWAY_SERVICE, 
                ConfigConst.KEEP_ALIVE_KEY, 
                ConfigConst.DEFAULT_KEEP_ALIVE)
        
        self.defaultQos = \
            self.config.getInteger(
                ConfigConst.MQTT_GATEWAY_SERVICE, 
                ConfigConst.DEFAULT_QOS_KEY, 
                ConfigConst.DEFAULT_QOS)
        
        self.mqttClient = None
        
        # IMPORTANT:
        # 
        # You can choose to set clientID in a number of ways:
        #  1 - use the deviceLocationID value in PiotConfig.props as the clientID (see below)
        #  2 - pass a custom clientID into constructor (from DeviceDataManager or your test)
        #  3 - hard code a clientID in this constructor (generally not recommended)
        #  4 - if using Python Paho, set NO client ID and let broker auto-assign
        #      a random value (not recommended if setting clean session flag to False)
        
        # NOTE: There are other ways to implement this logic, esp. if you
        # want to ensure the clientID passed into the constructor always
        # takes precedent. This is only one viable solution.
        
        if not clientID:
            # Use a default client ID - customize this for your implementation
            clientID = 'CDAMqttClientID001'
        
        self.clientID = \
            self.config.getProperty(
                ConfigConst.CONSTRAINED_DEVICE, 
                ConfigConst.DEVICE_LOCATION_ID_KEY, 
                clientID)
        
        # Validate the clientID
        if not self.clientID or len(self.clientID.strip()) == 0:
            raise ValueError("Client ID cannot be null or empty")
        
        logging.info('MqttClientConnector initialized.')
        logging.info('\tMQTT Client ID:   ' + self.clientID)
        logging.info('\tMQTT Broker Host: ' + self.host)
        logging.info('\tMQTT Broker Port: ' + str(self.port))
        logging.info('\tMQTT Keep Alive:  ' + str(self.keepAlive))
    
    
    def connectClient(self) -> bool:
        """
        Connects to the MQTT broker.
        
        Creates an MQTT client instance if not already created, sets up callback
        handlers, and establishes connection to the broker. Starts the network loop
        for handling incoming/outgoing messages.
        
        Returns:
            bool: True if connection initiated, False if already connected
        """
        if not self.mqttClient:
            # Create MQTT client instance
            # TODO: make clean_session configurable
            self.mqttClient = mqttClient.Client(
                client_id=self.clientID, 
                clean_session=True)
            
            # Set up callback handlers
            self.mqttClient.on_connect = self.onConnect
            self.mqttClient.on_disconnect = self.onDisconnect
            self.mqttClient.on_message = self.onMessage
            self.mqttClient.on_publish = self.onPublish
            self.mqttClient.on_subscribe = self.onSubscribe
        
        if not self.mqttClient.is_connected():
            logging.info('MQTT client connecting to broker at host: ' + self.host)
            self.mqttClient.connect(self.host, self.port, self.keepAlive)
            self.mqttClient.loop_start()
            
            return True
        else:
            logging.warning('MQTT client is already connected. Ignoring connect request.')
            
            return False
    
    
    def disconnectClient(self) -> bool:
        """
        Disconnects from the MQTT broker.
        
        Stops the network loop and disconnects from the broker if currently connected.
        
        Returns:
            bool: True if disconnection initiated, False if already disconnected
        """
        if self.mqttClient and self.mqttClient.is_connected():
            logging.info('Disconnecting MQTT client from broker: ' + self.host)
            self.mqttClient.loop_stop()
            self.mqttClient.disconnect()
            
            return True
        else:
            logging.warning('MQTT client already disconnected. Ignoring.')
            
            return False
    
    
    def publishMessage(self, resource: ResourceNameEnum = None, msg: str = None, qos: int = ConfigConst.DEFAULT_QOS) -> bool:
        """
        Publishes a message to the specified topic.
        
        Args:
            resource (ResourceNameEnum): The resource name enum representing the topic
            msg (str): The message payload to publish
            qos (int): Quality of Service level (0, 1, or 2). Defaults to DEFAULT_QOS.
        
        Returns:
            bool: True if message published successfully, False otherwise
        """
        # Check validity of resource (topic)
        if not resource:
            logging.warning('No topic specified. Cannot publish message.')
            return False
        
        # Check validity of message
        if not msg:
            logging.warning('No message specified. Cannot publish message to topic: ' + resource.value)
            return False
        
        # Check validity of QoS - set to default if necessary
        if qos < 0 or qos > 2:
            qos = ConfigConst.DEFAULT_QOS
        
        # Publish message, and wait for publish to complete before returning
        msgInfo = self.mqttClient.publish(topic=resource.value, payload=msg, qos=qos)
        msgInfo.wait_for_publish()
        
        return True
    
    
    def subscribeToTopic(self, resource: ResourceNameEnum = None, callback = None, qos: int = ConfigConst.DEFAULT_QOS) -> bool:
        """
        Subscribes to the specified topic.
        
        Args:
            resource (ResourceNameEnum): The resource name enum representing the topic
            callback: Optional callback function (not currently used)
            qos (int): Quality of Service level (0, 1, or 2). Defaults to DEFAULT_QOS.
        
        Returns:
            bool: True if subscription initiated successfully, False otherwise
        """
        # Check validity of resource (topic)
        if not resource:
            logging.warning('No topic specified. Cannot subscribe.')
            return False
        
        # Check validity of QoS - set to default if necessary
        if qos < 0 or qos > 2:
            qos = ConfigConst.DEFAULT_QOS
        
        # Subscribe to topic
        logging.info('Subscribing to topic %s', resource.value)
        self.mqttClient.subscribe(resource.value, qos)
        
        return True
    
    
    def unsubscribeFromTopic(self, resource: ResourceNameEnum = None) -> bool:
        """
        Unsubscribes from the specified topic.
        
        Args:
            resource (ResourceNameEnum): The resource name enum representing the topic
        
        Returns:
            bool: True if unsubscription initiated successfully, False otherwise
        """
        # Check validity of resource (topic)
        if not resource:
            logging.warning('No topic specified. Cannot unsubscribe.')
            return False
        
        logging.info('Unsubscribing to topic %s', resource.value)
        self.mqttClient.unsubscribe(resource.value)
        
        return True
    
    
    def setDataMessageListener(self, listener: IDataMessageListener = None):
        """
        Sets the data message listener for handling incoming messages.
        
        Args:
            listener (IDataMessageListener): The listener to receive message callbacks
        """
        if listener:
            self.dataMsgListener = listener
            logging.info('Data message listener set.')
        else:
            logging.warning('No data message listener provided.')
    
    
    # =========================================================================
    # Callback methods
    # =========================================================================
    
    def onConnect(self, client, userdata, flags, rc):
        """
        Callback for when the client receives a CONNACK response from the broker.
        
        Args:
            client: The client instance for this callback
            userdata: The private user data as set in Client() or userdata_set()
            flags: Response flags sent by the broker
            rc: The connection result code
        """
        if rc == 0:
            logging.info('MQTT client connected successfully to broker: ' + self.host)
        else:
            logging.error('MQTT client connection failed with result code: ' + str(rc))
            
            # Result codes:
            # 0: Connection successful
            # 1: Connection refused - incorrect protocol version
            # 2: Connection refused - invalid client identifier
            # 3: Connection refused - server unavailable
            # 4: Connection refused - bad username or password
            # 5: Connection refused - not authorized
    
    
    def onDisconnect(self, client, userdata, rc):
        """
        Callback for when the client disconnects from the broker.
        
        Args:
            client: The client instance for this callback
            userdata: The private user data as set in Client() or userdata_set()
            rc: The disconnection result code
        """
        if rc == 0:
            logging.info('MQTT client disconnected gracefully from broker.')
        else:
            logging.warning('MQTT client disconnected unexpectedly. Result code: ' + str(rc))
    
    
    def onMessage(self, client, userdata, message):
        """
        Callback for when a PUBLISH message is received from the broker.
        
        NOTE: You may need to delegate this callback functionality to a separate
        thread depending on your anticipated future use case. This will be discussed
        further in Lab Module 10.
        
        Args:
            client: The client instance for this callback
            userdata: The private user data as set in Client() or userdata_set()
            message: An instance of MQTTMessage with properties: topic, payload, qos, retain
        """
        try:
            topic = message.topic
            payload = message.payload.decode('utf-8')
            qos = message.qos
            
            logging.info('MQTT message received with payload: ' + str(payload))
            logging.debug('Topic: ' + topic)
            logging.debug('QoS: ' + str(qos))
            
            # Delegate to data message listener if set
            if self.dataMsgListener:
                try:
                    # Try to find matching ResourceNameEnum by comparing topic values
                    resourceEnum = None
                    for resource in ResourceNameEnum:
                        if resource.value == topic:
                            resourceEnum = resource
                            break
                    
                    if resourceEnum:
                        self.dataMsgListener.handleIncomingMessage(resourceEnum, payload)
                    else:
                        logging.warning('Unknown topic received: ' + topic)
                except Exception as e:
                    logging.error('Error delegating message to listener: ' + str(e))
            else:
                logging.debug('No data message listener set. Message not delegated.')
                
        except Exception as e:
            logging.error('Error processing incoming message: ' + str(e))
    
    
    def onPublish(self, client, userdata, mid):
        """
        Callback for when a message has been sent to the broker.
        
        Args:
            client: The client instance for this callback
            userdata: The private user data as set in Client() or userdata_set()
            mid: The message ID of the published message
        """
        logging.debug('Message published with ID: ' + str(mid))
    
    
    def onSubscribe(self, client, userdata, mid, granted_qos):
        """
        Callback for when the broker responds to a subscribe request.
        
        Args:
            client: The client instance for this callback
            userdata: The private user data as set in Client() or userdata_set()
            mid: The message ID of the subscribe request
            granted_qos: A list of integers giving the QoS level the broker granted
        """
        logging.debug('Subscription confirmed with message ID: ' + str(mid))
        logging.debug('Granted QoS: ' + str(granted_qos))