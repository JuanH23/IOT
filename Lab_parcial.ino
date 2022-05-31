
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include "time.h"
#include <Adafruit_BMP280.h>   //libreria para el bmp280

//-----------------------------BMP280 SET---------------
#define BMP280_I2C_ADDRESS  0x76
//------------------------------------------------------

Adafruit_BMP280  bmp280;
float pressure=0;
float temperature=0;

long lastMsg=0;
char msg[50];
int value=0;





/*SSID--PASSWORD SERVIDOR*/

const char* ssid="HUAWEI Y7";
const char* password="Clave2323";
const char* ntpServer = "co.pool.ntp.org";
const long gmtOffset_sec = 3600*-5;
const int daylightOffset_sec = 0;
 /*Direccion MQTT---IP address*/
 const char* mqtt_server="192.168.43.220";
 
const char* mqtt_username = "juanh"; // MQTT username
const char* mqtt_password = "1234"; // MQTT password

const char* clientID = "client_data"; // MQTT client ID

WiFiClient wifiClient;
PubSubClient client(mqtt_server,1883,wifiClient);

void connect_MQTT(){

  if(client.connect(clientID, mqtt_username, mqtt_password)) {
    Serial.println("Connected to MQTT Broker!");
  }else {
    Serial.println("Connection to MQTT Broker failed...");
  }

}



void setup_wifi(){
  delay(10);
  Serial.println();
  Serial.print("Conectando a: ");
  Serial.println(ssid);
  WiFi.begin(ssid,password);
  while(WiFi.status() !=WL_CONNECTED){
    delay(500);
    Serial.print(".");
    }
   Serial.println("");
   Serial.println("Wifi conectado");
   Serial.println("IP address: ");
   Serial.println(WiFi.localIP());
  }

  
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  bmp280.begin(0x76);
  setup_wifi();

}

void loop() {
  // put your main code here, to run repeatedly:
  connect_MQTT();
  long now=millis();


 
  if(now - lastMsg >1000){
  lastMsg=now;
  
  /****Señal de temperatura que se quiere enviar al broker*/
  temperature = bmp280.readTemperature();
  String tem="Temperatura:"+String((float)temperature)+"C ";
  /*Convertir el valor a char array*/
  char tempString[8];
  dtostrf(temperature,1,2,tempString);
  Serial.print("Temperatura: ");
  Serial.println(tempString);
  client.publish("esp32/temperature",tem.c_str());

  /*Señal de humedad que se quiere enviar al broker */

  pressure = bmp280.readPressure()*0.0009870;
  String pre="Presion:"+String((float)pressure)+"% ";
  /*Convertir el valor a char array*/
  char PreString[8];
  dtostrf(pressure,1,2,PreString);
  Serial.print("Presion: ");
  Serial.println(PreString);
  client.publish("esp32/Presion",pre.c_str());
  } 
   client.disconnect(); //FIN MQTT

}
