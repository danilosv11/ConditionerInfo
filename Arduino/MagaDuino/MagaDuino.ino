#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

#define DHT_IN_PIN 4 // Пин, к которому подключен датчик DHT11_IN
#define DHT_OUT_PIN 21 // Пин, к которому подключен датчик DHT11_OUT
#define AnemoPin 34 // Пин, к которому подключён Анемоментр
#define ButtonPin 13 // Пин кнопки включения

#define DHT_IN_TYPE DHT11 // Тип датчика DHT11_IN
#define DHT_OUT_TYPE DHT11 // Тип датчика DHT11_OUT

const char* ssid = "your_SSID"; // Укажите ваш SSID
const char* password = "your_password"; // Укажите ваш пароль
const char* serverName = "http://your_server_address:8080"; // Укажите IP адрес вашего сервера

DHT dht_in(DHT_IN_PIN, DHT_IN_TYPE);
DHT dht_out(DHT_OUT_PIN, DHT_OUT_TYPE);

int countSignals = 0;
bool anemoChange = false;
bool isWindy = false;
uint32_t dataTimer = 0;
int anemoValue = 0;
int time_to_proccess = 2000;
int time_to_work = 1200000;
uint32_t lastWindSpeedPositiveTime = 0;


void setup() {
  Serial.begin(115200);

  // Подключение к WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  dht_in.begin();
  dht_out.begin();

  pinMode(ButtonPin, INPUT_PULLUP);
}

void loop() {
  // Чтение данных с датчиков DHT11
  float humidity_in = dht_in.readHumidity();
  float temperatire_in = dht_in.readTemperature();
  float humidity_out = dht_out.readHumidity();
  float temperatire_out = dht_out.readTemperature();
  anemoValue = analogRead(AnemoPin);
  

  if (anemoValue >= 2200 && !anemoChange){
    countSignals = countSignals + 1;
    anemoChange=true;
  }
  if (anemoValue < 2200 && anemoChange){
    anemoChange=false;
  }

  // Проверка, что данные корректные
  if (isnan(humidity_in) || isnan(temperatire_in)) {
    Serial.println("Failed to read from DHT_IN sensor!");
    return;
  }
  if (isnan(humidity_out) || isnan(temperatire_out)) {
    Serial.println("Failed to read from DHT_OUT sensor!");
    return;
  }

  if (millis() - dataTimer > time_to_proccess){
    float wind_speed=M_PI*countSignals*0.28/(24*2);
    countSignals=0;
  
    // Формирование сообщения для отправки на сервер
    String postData = "Temperature_IN: ";
    postData += String(temperatire_in);
    postData += " C\nHumidity_IN: ";
    postData += String(humidity_in);
    postData += " %\nTemperature_OUT: ";
    postData += String(temperatire_out);
    postData += " C\nHumidity_OUT: ";
    postData += String(humidity_out);
    postData += " %\nWind_speed: ";
    postData += String(wind_speed);
    postData += " m/s";
  
    Serial.println("Sending data: " + postData);
    
    if (wind_speed > 0.5 && !isWindy) {
      lastWindSpeedPositiveTime = millis();
      isWindy = true;
    }

    if (wind_speed < 0.5) {
      isWindy = false;
    }
    
    if (digitalRead(ButtonPin) == 0){
      if ((millis() - lastWindSpeedPositiveTime) >= time_to_work && isWindy) {
        if (WiFi.status() == WL_CONNECTED){
          HTTPClient http;
          http.begin(serverName);
          http.addHeader("Content-Type", "text/plain");

          int httpResponseCode = http.POST(postData);

          if (httpResponseCode > 0) {
            String response = http.getString();
            Serial.println(httpResponseCode);
            Serial.println(response); // Вывод ответа сервера
          } else {
            Serial.print("Error on sending POST: ");
            Serial.println(httpResponseCode);
          }
          http.end();
        } else {
        Serial.println("WiFi Disconnected");
        }
      } else {
      Serial.println("ISNT WINDY ENOUGH");
      } 
    } else {
      Serial.println("SYSTEM IS TURNED OFF");
    }
    dataTimer = millis();
  }
}
