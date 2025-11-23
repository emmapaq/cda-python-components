import logging
import ssl
import paho.mqtt.client as mqttClient

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.IPubSubClient import IPubSubClient

from programmingtheiot.data.DataUtil import DataUtil


class MqttClientConnector(IPubSubClient):
    """
    MQTT client connector implementation using Paho MQTT.
    
    Handles connection, disconnection, publishing, and subscribing to MQTT broker.
    Implements callback mechanisms for message handling and connection events.
    Supports TLS/SSL encryption for secure connections.
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
        
        # Encryption properties
        self.enableEncryption = \
            self.config.getBoolean(
                ConfigConst.MQTT_GATEWAY_SERVICE, 
                ConfigConst.ENABLE_CRYPT_KEY)
        
        self.pemFileName = \
            self.config.getProperty(
                ConfigConst.MQTT_GATEWAY_SERVICE, 
                ConfigConst.CERT_FILE_KEY)
        
        self.mqttClient = None
        
        # Set client ID
        if not clientID:
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
        logging.info('\tEncryption:       ' + str(self.enableEncryption))
    
    
    def connectClient(self) -> bool:
        """
        Connects to the MQTT broker.
        
        Creates an MQTT client instance if not already created, sets up callback
        handlers, and establishes connection to the broker. Starts the network loop
        for handling incoming/outgoing messages.
        
        If encryption is enabled, configures TLS/SSL before connecting.
        
        Returns:
            bool: True if connection initiated, False if already connected
        """
        if not self.mqttClient:
            # Create MQTT client instance
            # TODO: make clean_session configurable
            self.mqttClient = mqttClient.Client(
                client_id=self.clientID, 
                clean_session=True)
            
            try:
                if self.enableEncryption:
                    logging.info("Enabling TLS encryption...")
                    
                    # Update port to secure port
                    self.port = \
                        self.config.getInteger(
                            ConfigConst.MQTT_GATEWAY_SERVICE, 
                            ConfigConst.SECURE_PORT_KEY, 
                            ConfigConst.DEFAULT_MQTT_SECURE_PORT)
                    
                    self.mqttClient.tls_set(
                        self.pemFileName, 
                        tls_version=ssl.PROTOCOL_TLS_CLIENT)
                    
                    logging.info("TLS encryption enabled with cert: " + str(self.pemFileName))
                    logging.info("Using secure port: " + str(self.port))
            except Exception as e:
                logging.warning("Failed to enable TLS encryption: " + str(e))
                logging.warning("Using unencrypted connection.")
            
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
        
        NOTE: wait_for_publish() is commented out to prevent blocking/deadlock.
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
        
        # Publish message
        msgInfo = self.mqttClient.publish(topic=resource.value, payload=msg, qos=qos)
        
        # COMMENTED OUT for Lab Module 10 - prevents blocking/deadlock
        # msgInfo.wait_for_publish()
        
        # NOTE: The 'True' return no longer guarantees successful publish,
        # as it will return before the publish may successfully complete
        return True
    
    
    def subscribeToTopic(self, resource: ResourceNameEnum = None, callback = None, qos: int = ConfigConst.DEFAULT_QOS) -> bool:
        """
        Subscribes to the specified topic.
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
        
        Subscribes to actuator command topic upon successful connection.
        """
        if rc == 0:
            logging.info('[Callback] Connected to MQTT broker. Result code: ' + str(rc))
            
            # Subscribe to actuator command topic
            self.mqttClient.subscribe(
                topic=ResourceNameEnum.CDA_ACTUATOR_CMD.value,
                qos=self.defaultQos
            )
            
            # Add topic-specific callback for actuator commands
            self.mqttClient.message_callback_add(
                sub=ResourceNameEnum.CDA_ACTUATOR_CMD.value,
                callback=self.onActuatorCommandMessage
            )
            
            logging.info('Subscribed to actuator command topic: ' + ResourceNameEnum.CDA_ACTUATOR_CMD.value)
        else:
            logging.error('MQTT client connection failed with result code: ' + str(rc))
    
    
    def onDisconnect(self, client, userdata, rc):
        """
        Callback for when the client disconnects from the broker.
        """
        if rc == 0:
            logging.info('MQTT client disconnected gracefully from broker.')
        else:
            logging.warning('MQTT client disconnected unexpectedly. Result code: ' + str(rc))
    
    
    def onActuatorCommandMessage(self, client, userdata, msg):
        """
        Callback for actuator command messages received from GDA.
        
        This is a topic-specific callback that handles ActuatorData commands.
        
        Args:
            client: The MQTT client instance
            userdata: User data
            msg: The MQTT message containing actuator command
        """
        logging.info('[Callback] Actuator command message received. Topic: %s.', msg.topic)
        
        if self.dataMsgListener:
            try:
                # Assumes all data is encoded using UTF-8 (between GDA and CDA)
                actuatorData = DataUtil().jsonToActuatorData(msg.payload.decode('utf-8'))
                
                # Delegate to DeviceDataManager
                self.dataMsgListener.handleActuatorCommandMessage(actuatorData)
            except Exception as e:
                logging.exception("Failed to convert incoming actuation command payload to ActuatorData: ")
        else:
            logging.warning("No data message listener set. Actuator command ignored.")
    
    
    def onMessage(self, client, userdata, message):
        """
        Callback for when a PUBLISH message is received from the broker.
        
        This is the default message handler for topics without specific callbacks.
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
        """
        # PERFORMANCE TESTING: Comment out during performance tests
        # logging.debug('Message published with ID: ' + str(mid))
        pass
    
    
    def onSubscribe(self, client, userdata, mid, granted_qos):
        """
        Callback for when the broker responds to a subscribe request.
        """
        logging.debug('Subscription confirmed with message ID: ' + str(mid))
        logging.debug('Granted QoS: ' + str(granted_qos))