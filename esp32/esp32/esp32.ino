#include "config.h"
#include <BlynkSimpleEsp32.h>
#include <WiFi.h>
#include <WebServer.h>
#include <DHT.h>
#include <InfluxDbClient.h>

DHT dht(DHT_PIN, DHT11);
unsigned long startTime;

InfluxDBClient client(INFLUXDB_URL, INFLUXDB_ORG, INFLUXDB_BUCKET, INFLUXDB_TOKEN);
Point sensor("jetson_iot");

WebServer server(WebServerPort);

unsigned long previousMillis = 0;
const long interval = 10000;

void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  Blynk.begin(BLYNK_AUTH_TOKEN, WIFI_SSID, WIFI_PASSWORD);
  pinMode(LED_PIN, OUTPUT);

  sensor.addTag("device", "ESP32");
  if (client.validateConnection()) {
      Serial.println("Connected to InfluxDB");
  } else {
      Serial.print("InfluxDB connection failed: ");
      Serial.println(client.getLastErrorMessage());
  }

  server.on("/getdata", getData);
  server.on("/ledon", ledOn);
  server.on("/ledoff", ledOff);
  server.on("/buzzeron", buzzerOn);
  server.on("/buzzeroff", buzzerOff);
  server.begin();

}

void loop() {
  Blynk.run();

  server.handleClient();
    
  unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
      previousMillis = currentMillis;

    Serial.print("ESP32 IP Address: ");
    Serial.println(WiFi.localIP());
    
    Blynk.virtualWrite(VirtElapsedTime, getElapsedTime());
    Blynk.virtualWrite(VirtTemp, getTemperature());
    Blynk.virtualWrite(VirtHum, getHumidity());
    int ledState = getLedState();
    Serial.print("LED state: ");
    Serial.println(ledState);

    Serial.print("Temp: ");
    Serial.println(getTemperature());
    Serial.print("Hum: ");
    Serial.println(getHumidity());
    Serial.print("Time: ");
    Serial.println(getElapsedTime());

    Serial.println("Data written to Blynk");

    sensor.clearFields();
    sensor.addField("temperature", getTemperature());
    sensor.addField("humidity", getHumidity());
    sensor.addField("elapsed_time", getElapsedTime());

    if (!client.writePoint(sensor)) {
      Serial.print("InfluxDB write failed: ");
      Serial.println(client.getLastErrorMessage());
    } else {
      Serial.println("Data written to InfluxDB");
    }
  }
}

float getTemperature() {
    float temp = dht.readTemperature();
    if (isnan(temp)) {
        Serial.println("Failed to read temperature!");
    }
    return temp;
}

float getHumidity() {
    float hum = dht.readHumidity();
    if (isnan(hum)) {
        Serial.println("Failed to read humidity!");
    }
    return hum;
}

float getElapsedTime() {
    return (millis() - startTime) / 3600000.0;
}

int getLedState() {
    return digitalRead(LED_PIN);
}

int getBuzzerState() {
    return digitalRead(BUZZER_PIN);
}

BLYNK_WRITE(VirtLed) {
    int ledState = param.asInt();
    digitalWrite(LED_PIN, ledState);
    Serial.print("LED state changed to: ");
    Serial.println(ledState);
}

BLYNK_WRITE(VirtBuzz) {
    int buzzerState = param.asInt();
    digitalWrite(BUZZER_PIN, buzzerState);
    Serial.print("Buzzer state changed to: ");
    Serial.println(buzzerState);
}

void getData() {
    String message = "ESP32 Sensor Data:\n";
    message += "Temperature: " + String(getTemperature()) + "°C\n";
    message += "Humidity: " + String(getHumidity()) + "%\n";
    message += "Elapsed Time: " + String(getElapsedTime()) + " hrs\n";
    message += "LED State: " + String(getLedState()) + "\n";
    message += "LED State: " + String(getBuzzerState()) + "\n";
    server.send(200, "text/plain; charset=utf-8", message);
}

void ledOn() {
    digitalWrite(LED_PIN, HIGH);
    server.send(200, "text/plain", "LED is ON");
}

void ledOff() {
    digitalWrite(LED_PIN, LOW);
    server.send(200, "text/plain", "LED is OFF");
}

void buzzerOn() {
    digitalWrite(BUZZER_PIN, HIGH);
    server.send(200, "text/plain", "Buzzer is ON");
}

void buzzerOff() {
    digitalWrite(BUZZER_PIN, Low);
    server.send(200, "text/plain", "Buzzer is OFF");
}