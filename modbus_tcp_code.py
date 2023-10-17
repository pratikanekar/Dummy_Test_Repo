import time
from pymodbus.client.sync import ModbusTcpClient
import paho.mqtt.client as mqtt
import json
from loguru import logger

# Read configuration from JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Modbus server (energy meter) configuration
modbus_server_ip = config.get('modbus_server_ip')
modbus_server_port = config.get('modbus_server_port')
modbus_slave_address = config.get('modbus_slave_address')
modbus_register_address = config.get('modbus_register_address')
modbus_register_count = config.get('modbus_register_count')

# MQTT broker configuration
client_id = config.get('client_id')
mqtt_broker_address = config.get('mqtt_broker_address')
username = config.get('username')
password = config.get('password')
mqtt_topic = config.get('mqtt_topic')

# Initialize Modbus client
modbus_client = ModbusTcpClient(modbus_server_ip, port=modbus_server_port)
logger.debug(f"Modbus Client connected Successfully")


def on_connect(client, userdata, flags, rc, properties=None):
    logger.debug(f'Connected to MQTT broker with result code {rc}')


# Initialize MQTT client
mqtt_client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv5)
mqtt_client.username_pw_set(username=username, password=password)
mqtt_client.on_connect = on_connect
logger.debug(f"MQTT Client connected Successfully")


def read_energy_data():
    try:
        modbus_data = modbus_client.read_holding_registers(
            address=modbus_register_address,
            count=modbus_register_count,
            unit=modbus_slave_address
        )
        if modbus_data:
            return modbus_data.registers
        else:
            return None
    except Exception as e:
        logger.error(f"Error reading Modbus data: {e}")
        return None


def publish_to_mqtt(data):
    try:
        mqtt_client.connect(mqtt_broker_address, 1883, 60, clean_start=False)
        mqtt_client.publish(mqtt_topic, str(data))
        logger.debug(f"Data Pushed successfully....!")
    except Exception as e:
        logger.error(f"Error publishing to MQTT: {e}")


if __name__ == "__main__":
    while True:
        modbus_data = read_energy_data()
        if modbus_data:
            logger.info(f"Energy Data: {modbus_data}")
            publish_to_mqtt(modbus_data)
        time.sleep(10)  # Read and publish data every 60 seconds






