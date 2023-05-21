import paho.mqtt.client as mqtt
import time


def connectBroker(brokerAddress, topic):
    mqttBroker = brokerAddress
    client = mqtt.Client(topic)
    try:
        client.connect(mqttBroker)
        print("Connected to MQTT Broker: " + mqttBroker)
        time.sleep(3)
    except:
        print("Connection failed to MQTT Broker: " + mqttBroker)
        time.sleep(3)

    return client
