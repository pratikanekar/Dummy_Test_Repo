# Modbus to MQTT Data Bridge

---

This Python script is designed to read data from a Modbus RTU device and publish it to an MQTT broker. It provides a bridge between Modbus and MQTT protocols, allowing you to collect data from Modbus devices and make it available on MQTT for further processing or monitoring.

### Requirements

First Unzip the Folder and Before using this script, you need to have install the following dependencies and configurations present inside requirements.txt file.

1. Python: Ensure that you have Python 3.8 installed on your system.
2. Required Python Packages: Install the necessary Python packages using pip:
   - pymodbus for Modbus communication
   - paho-mqtt for MQTT communication
   - loguru for logging
   - You can install these packages using the following command: ```pip3 install -r requirements.txt```
3. Configuration File: Created a JSON configuration file named config.json with the following parameters:
    ```
   {
    "modbus_server_port": "COM1",  # Serial port for Modbus (e.g., 'COM1' on Windows or '/dev/ttyUSB0' on Linux)
    "modbus_slave_address": 1,  # Modbus slave address
    "modbus_register_address": 0,  # Modbus register address
    "modbus_register_count": 1,  # Number of registers to read
    "modbus_baudrate": 9600,  # Modbus serial baud rate
    "modbus_parity": "N",  # Modbus serial parity ('N' for None, 'E' for Even, 'O' for Odd)
    "modbus_bytesize": 8,  # Modbus serial byte size
    "modbus_stopbits": 1,  # Modbus serial stop bits
    "client_id": "client 1",  # MQTT client ID
    "mqtt_broker_address": "IP_address of MQTT",  # MQTT broker address
    "username": "mqtt_username",  # MQTT username
    "password": "mqtt_password",  # MQTT password
    "mqtt_topic": "modbus/data/topic",  # MQTT topic to publish data
    "register_type": "holding"  # Modbus register type (holding, input, discrete_input, coil)
    }
    ```
   Adjust the parameters to match your specific Modbus and MQTT configuration.

### Usage
1. Ensure that the config.json file is properly configured with your Modbus and MQTT settings.
2. Ensure that the connection is properly configured with Modbus device and its permissions
3. Create virtual Environment using the following command: ```python3 -m venv venv```
4. Activate virtual Environment using the following command: ```source venv/bin/activate```
5. Run the script using the following command: ```python3 main.py```
   - This script will continuously read data from the specified Modbus registers and publish it to the MQTT broker at the specified interval (every 10 seconds by default).

### Logging
The script uses the Loguru library for logging. You can find log files in the logs directory. Logs provide information about the script's operation and any errors encountered.

### Customization
You can modify the script to suit your specific requirements, such as changing the Modbus register type, the data read interval, or adding additional error handling.

-----