import paho.mqtt.client as mqtt
import sqlite3
from time import time

MQTT_HOST = '192.168.43.220'
MQTT_PORT = 1883
MQTT_USER = 'juanh'
MQTT_PASSWORD = '1234'
TOPIC = 'esp32/+'
 
DATABASE_FILE = 'mqtt.db'
 
count=0
 
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
