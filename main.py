import time
import json
from pymodbus.client.sync import ModbusSerialClient
import paho.mqtt.client as mqtt
from loguru import logger

# Read configuration from JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Modbus RTU device configuration
modbus_port = config.get('modbus_server_port')  # The serial port (e.g., 'COM1' on Windows or '/dev/ttyUSB0' on Linux)
modbus_slave_address = config.get('modbus_slave_address')
modbus_register_address = config.get('modbus_register_address')
modbus_register_count = config.get('modbus_register_count')
modbus_baudrate = config.get('modbus_baudrate')
modbus_parity = config.get('modbus_parity')
modbus_bytesize = config.get('modbus_bytesize')
modbus_stopbits = config.get('modbus_stopbits')

# MQTT broker configuration
client_id = config.get('client_id')
mqtt_broker_address = config.get('mqtt_broker_address')
username = config.get('username')
password = config.get('password')
mqtt_topic = config.get('mqtt_topic')

# Initialize Modbus RTU client
modbus_client = ModbusSerialClient(method='rtu', port=modbus_port, stopbits=modbus_stopbits, bytesize=modbus_bytesize,
                                   parity=modbus_parity, baudrate=modbus_baudrate)
logger.debug(f"Modbus RTU Client connected successfully")


def on_connect(client, userdata, flags, rc, properties=None):
    logger.debug(f'Connected to MQTT broker with result code {rc}')


# Initialize MQTT client
mqtt_client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv5)
mqtt_client.username_pw_set(username=username, password=password)
mqtt_client.on_connect = on_connect
logger.debug(f"MQTT Client connected successfully")


def read_energy_data(register_type):
    try:
        if register_type == "holding":
            data = modbus_client.read_holding_registers(
                address=modbus_register_address,
                count=modbus_register_count,
                unit=modbus_slave_address
            )
        elif register_type == "input":
            data = modbus_client.read_input_registers(
                address=modbus_register_address,
                count=modbus_register_count,
                unit=modbus_slave_address
            )
        elif register_type == "discrete_input":
            data = modbus_client.read_discrete_inputs(
                address=modbus_register_address,
                count=modbus_register_count,
                unit=modbus_slave_address
            )
        elif register_type == "coil":
            data = modbus_client.read_coils(
                address=modbus_register_address,
                count=modbus_register_count,
                unit=modbus_slave_address
            )
        else:
            logger.error("Invalid Modbus register type.")
            return None

        if data:
            return data.registers
        else:
            return None
    except Exception as e:
        logger.error(f"Error reading Modbus {register_type}: {e}")
        return None


def publish_to_mqtt(data):
    try:
        mqtt_client.connect(mqtt_broker_address, 1883, 60, clean_start=False)
        mqtt_client.publish(mqtt_topic, str(data))
        logger.debug(f"Data pushed successfully...!")
    except Exception as e:
        logger.error(f"Error publishing to MQTT: {e}")


if __name__ == "__main__":
    try:
        while True:
            if modbus_client.connect():
                register_type = config.get('register_type')
                modbus_data = read_energy_data(register_type)
                modbus_client.close()
                if modbus_data:
                    logger.info(f"Energy Data: {modbus_data}")
                    publish_to_mqtt(modbus_data)
            time.sleep(10)  # Read and publish data every 10 seconds (adjust as needed)
    except Exception as e:
        logger.error(f"Error in Main: {e}")
