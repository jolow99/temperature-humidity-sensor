#include <Arduino.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include "Firebase_Arduino_WiFiNINA.h"
#include "secrets.h"

char DATABASE_URL[] = SECRET_DATABASE_URL;
char DATABASE_SECRET[] = SECRET_DATABASE_SECRET;
char WIFI_SSID[] = SECRET_SSID;        
char WIFI_PASSWORD[] = SECRET_PASS;   

#define RELAYPIN 6 // Pin to control the relay
#define DHTPIN 2     // Digital pin connected to the DHT sensor 
#define DHTTYPE DHT11     // DHT 11

// Define firebase and dht objects
FirebaseData fbdo;
DHT_Unified dht(DHTPIN, DHTTYPE);

// Initialise values and define firebase path
String data = "/data";
String power_value = "0";
String temperature_value = "0.00";
String humidity_value = "0.00";
int timestamp;

void printWifi() {
  Serial.println("----------------------------------------");
  Serial.println("Board Information:");
  // print your board's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  Serial.println();
  Serial.println("Network Information:");
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.println(rssi);

  byte encryption = WiFi.encryptionType();
  Serial.print("Encryption Type:");
  Serial.println(encryption, HEX);
  Serial.println();
  Serial.println("----------------------------------------");
}

void printTemperature(sensor_t sensor) { 
  Serial.println(F("Temperature Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("°C"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("°C"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("°C"));
  Serial.println(F("------------------------------------"));
}


void printHumidity(sensor_t sensor) {
  Serial.println(F("Humidity Sensor"));
  Serial.print  (F("Sensor Type: ")); Serial.println(sensor.name);
  Serial.print  (F("Driver Ver:  ")); Serial.println(sensor.version);
  Serial.print  (F("Unique ID:   ")); Serial.println(sensor.sensor_id);
  Serial.print  (F("Max Value:   ")); Serial.print(sensor.max_value); Serial.println(F("%"));
  Serial.print  (F("Min Value:   ")); Serial.print(sensor.min_value); Serial.println(F("%"));
  Serial.print  (F("Resolution:  ")); Serial.print(sensor.resolution); Serial.println(F("%"));
  Serial.println(F("------------------------------------"));
}

void setup()
{
  // Serial Setup and wait for serial
  Serial.begin(9600);
  // while (!Serial); // Waits for serial for debugging purposes. Cannot be used in PROD

  // Initialise Relay
  pinMode(RELAYPIN, OUTPUT);

  // Initialise sensors
  dht.begin();
  sensor_t sensor;

  // Temperature 
  dht.temperature().getSensor(&sensor);
  printTemperature(sensor);

  // Humidity
  dht.humidity().getSensor(&sensor);
  printHumidity(sensor);

  // WiFi setup
  int status = WL_IDLE_STATUS;
  while (status != WL_CONNECTED) {
    Serial.print("Connecting to Wi-Fi: ");
    Serial.println(WIFI_SSID);
    status = WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    delay(10000);
  }
  printWifi();

  // Firebase setup
  Firebase.begin(DATABASE_URL, DATABASE_SECRET, WIFI_SSID, WIFI_PASSWORD);
  Firebase.reconnectWiFi(true);

}

void loop() 
{
  delay(10000);
  
  // Get Power value
  Firebase.getString(fbdo, "/power");
  power_value = fbdo.stringData();
  Serial.print("Current Power Value: ");
  Serial.println(power_value);
  
  if (power_value == "1") {
    sensors_event_t event;
    
    // Get time
    timestamp = WiFi.getTime();
    Serial.print("Time: ");
    Serial.println(timestamp);

    // Get temperature 
    dht.temperature().getEvent(&event);
    if (isnan(event.temperature)) {
      Serial.println(F("Error reading temperature!"));
    }
    else {
      Serial.print(F("Temperature: "));
      Serial.print(event.temperature);
      Serial.println(F("°C"));
      temperature_value = String(event.temperature);
      Firebase.setString(fbdo, data + "/" + String(timestamp) + "/Temperature", temperature_value);
    }
    // Get humidity 
    dht.humidity().getEvent(&event);
    if (isnan(event.relative_humidity)) {
      Serial.println(F("Error reading humidity!"));
    }
    else {
      Serial.print(F("Humidity: "));
      Serial.print(event.relative_humidity);
      Serial.println(F("%"));
      humidity_value = String(event.relative_humidity);
      Firebase.setString(fbdo, data + "/" + String(timestamp) + "/Humidity", humidity_value);
    }

    // Turn on humidifier if humidity < 50%
    if (event.relative_humidity < 50) {
      digitalWrite(6, HIGH);
    }
    else {
      digitalWrite(6, LOW);
    }

  } else {
    Serial.println("Power Value is off");
    digitalWrite(6, LOW);
  }
}