import paho.mqtt.client as mqtt
import sqlite3
from time import time
from azure.iot.device import IoTHubDeviceClient, Message

MQTT_HOST = '192.168.43.220'
MQTT_PORT = 1883
MQTT_USER = 'juanh'
MQTT_PASSWORD = '1234'
TOPIC = 'esp32/+'
 
DATABASE_FILE = 'mqtt.db'
 
CONNECTION_STRING = "HostName=azurerasp.azure-devices.net;DeviceId=rasppi;SharedAccessKey=UrfhiURUcD/E14ce8MHUS+BErVabKXykNojjeDFfXPU="

# Define the JSON message to send to IoT Hub.
From = "Pi"
To = "Azure"
MSG_TXT = '{{"Temperatura": {temp},"Presion": {presion}}}'


contador=0
count=0
 
def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client
    
def iothub_client_telemetry_sample_run():
    global contador
    global cliente
  
    if(contador==0):
        cliente = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        contador=1

    try:
        
        msg_txt_formatted = MSG_TXT.format(temp=ind1,presion=ind2)
        message = Message(msg_txt_formatted)

        # Send the message.
        print( "Sending message: {}".format(message) )
        cliente.send_message(message)
        print ( "Message successfully sent" )

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )    

 
def on_connect(mqtt_client, user_data, flags, conn_result):
    print('resultado del codigo ' + str())
    mqtt_client.subscribe(TOPIC)
 
 
def on_message(mqtt_client, user_data, message):
    global count
    global ind1
    global ind2

    db_conn = user_data['db_conn']
    sql = 'INSERT INTO datos (temperature,Presion) VALUES (?, ?)'
    cursor = db_conn.cursor()


    datos=str(message.payload)
    if 'Temperatura:'in datos:
         Pri=datos.find(':')
         Ult=datos.find('C')
         ind1=datos[Pri+1:Ult]
         print('T:',ind1)
         count=count+1
    elif 'Presion:'in datos:
         Pri=datos.find(':')
         Ult=datos.find('%')
         ind2=datos[Pri+1:Ult]
         print('P:',ind2)
         count=count+1
    if count == 4:
         cursor.execute(sql,(ind1,ind2))
         db_conn.commit()
         cursor.close()
         count=0

         iothub_client_telemetry_sample_run()


def main():
    db_conn = sqlite3.connect(DATABASE_FILE)
    sql = """
    CREATE TABLE IF NOT EXISTS datos (
        temperature TEXT NOT NULL,
        Presion TEXT NOT NULL
    )
    """
    cursor = db_conn.cursor()
    cursor.execute(sql)
    cursor.close()
 
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.user_data_set({'db_conn': db_conn})
 
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
 
    mqtt_client.connect(MQTT_HOST, MQTT_PORT)
    mqtt_client.loop_forever()
 

if __name__ == '__main__':
    print('INICIO')
    print ( "Press Ctrl-C to exit" ) 
    main() 
    