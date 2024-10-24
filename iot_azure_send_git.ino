//Azure IoT Hub + DHT11 + NodeMCU ESP8266 Experiment Done By Prasenjit Saha
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>
#include <Adafruit_AHTX0.h>                               // Подключаем библиотеку Adafruit_AHTX0
Adafruit_AHTX0 aht;       


// WiFi settings
const char* ssid = "WiFi SSID";
const char* password = "Password";



//Azure IoT Hub
const String AzureIoTHubURI="https://myioteventhub.azure-devices.net/devices/devicename/messages/events?api-version=2020-03-13"; 
const String AzureIoTHubFingerPrint="FingerPrint"; 
const String AzureIoTHubAuth="SAS Token";

WiFiClientSecure client;

void setup() {
  
   pinMode( A0, INPUT );
  Serial.begin(115200);
  Serial.println(F("DHTxx test!"));

  Serial.println("ESP8266 starting in normal mode");
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  
  // Print the IP address
  Serial.println(WiFi.localIP());
  if (!aht.begin())                                       // Инициализация датчика
  {                                    
    Serial.println("Could not find AHT? Check wiring");   // Отправка сообщения
    while (1) delay(10);                                  // Зацикливаем программу             
  } 
}

void loop() {

  delay(2000);
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);
  float h = humidity.relative_humidity;
  // Read temperature as Celsius (the default)
  float t = temp.temperature;
  float b = analogRead(A0);


  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));


  String PostData = "{ \"DeviceId\":\"wemos\",\"Temperature\":" + String(t) + ",\"Humidity\":" + String(h) + ",\"Brightness\":" + String(b) +"}";
  Serial.println(PostData);
  
  // Send data to cloud
  int returnCode = RestPostData(AzureIoTHubURI, AzureIoTHubFingerPrint, AzureIoTHubAuth, PostData);
  Serial.println(returnCode);
}

int RestPostData(String URI, String fingerPrint, String Authorization, String PostData)
{
    WiFiClientSecure client;
    client.setFingerprint(fingerPrint.c_str());  // Set the SSL fingerprint

    HTTPClient http;
    if (!http.begin(client, URI)) {  // Pass the secure client and URI to the HTTPClient
        Serial.println("Unable to connect");
        return -1;
    }

    http.addHeader("Authorization", Authorization);
    http.addHeader("Content-Type", "application/json");

    int returnCode = http.POST(PostData);
    if (returnCode < 0) {
        Serial.println("RestPostData: Error sending data: " + String(http.errorToString(returnCode).c_str()));
    }

    http.end();
    return returnCode;
}

