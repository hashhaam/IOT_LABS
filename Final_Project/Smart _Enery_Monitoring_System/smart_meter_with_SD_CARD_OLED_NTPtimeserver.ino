#include <WiFi.h>
#include <PubSubClient.h>
#include "EmonLib.h"

// OLED Libraries
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// --- OLED Configuration ---
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// WiFi Credentials
const char* ssid = "H.";
const char* password = "sarkari0";

// MQTT Broker IP (Laptop IP)
const char* mqtt_server = "192.168.108.41"; // Replace with your laptop IP

WiFiClient espClient;
PubSubClient client(espClient);

EnergyMonitor emon;

#define vCalibration 85.28
#define currCalibration 1.16

unsigned long lastMillis = 0;
float kWh = 0;

// Function to calculate cost (as per Pakistan tariff slabs)
float calculateCost(float energy_kWh) {
  float cost = 0;
  if (energy_kWh <= 50) cost = energy_kWh * 3.95;
  else if (energy_kWh <= 100) cost = 50 * 3.95 + (energy_kWh - 50) * 7.74;
  else if (energy_kWh <= 200) cost = 50 * 3.95 + 50 * 7.74 + (energy_kWh - 100) * 10.06;
  else if (energy_kWh <= 300) cost = 50 * 3.95 + 50 * 7.74 + 100 * 10.06 + (energy_kWh - 200) * 12.15;
  else if (energy_kWh <= 400) cost = 50 * 3.95 + 50 * 7.74 + 100 * 10.06 + 100 * 12.15 + (energy_kWh - 300) * 19.55;
  else if (energy_kWh <= 500) cost = 50 * 3.95 + 50 * 7.74 + 100 * 10.06 + 100 * 12.15 + 100 * 19.55 + (energy_kWh - 400) * 22.65;
  else if (energy_kWh <= 600) cost = 50 * 3.95 + 50 * 7.74 + 100 * 10.06 + 100 * 12.15 + 100 * 19.55 + 100 * 22.65 + (energy_kWh - 500) * 24.15;
  else cost = 50 * 3.95 + 50 * 7.74 + 100 * 10.06 + 100 * 12.15 + 100 * 19.55 + 100 * 22.65 + 100 * 24.15 + (energy_kWh - 600) * 27.65;
  return cost;
}

void setup_wifi() {
  Serial.begin(115200);
  delay(10);
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected.");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("Connected to MQTT Broker.");
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" Retrying in 5 seconds...");
      delay(5000);
    }
  }
}

void setup_oled() {
  Wire.begin(8, 9); // Adjust SDA, SCL as per your board
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    while (true); // halt
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("Smart Meter MQTT");
  display.println("Initializing...");
  display.display();
  delay(1500);
}

void setup() {
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  setup_oled();

  emon.voltage(4, vCalibration, 1.7); // D4 pin, calibration
  emon.current(5, currCalibration);  // D5 pin, calibration

  lastMillis = millis();
}

void loop() {
  if (!client.connected()) reconnect();
  client.loop();

  emon.calcVI(20, 2000);
  float Vrms = emon.Vrms;
  float Irms = emon.Irms;
  float Power = emon.apparentPower;

  float timeDiffHrs = (float)(millis() - lastMillis) / 3600000.0;
  kWh += (Power * timeDiffHrs) / 1000.0;
  lastMillis = millis();

  float cost = calculateCost(kWh);

  // Build payload for MQTT
  String payload = "{\"Vrms\":" + String(Vrms, 2) +
                   ",\"Irms\":" + String(Irms, 3) +
                   ",\"Power\":" + String(Power, 2) +
                   ",\"kWh\":" + String(kWh, 4) +
                   ",\"Cost\":" + String(cost, 2) + "}";

  client.publish("smartmeter/data", payload.c_str());
  Serial.println("Published: " + payload);

  // OLED DISPLAY
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);

  display.setCursor(0, 0);
  display.print("V: "); display.print(Vrms, 2); display.println("V");

  display.setCursor(0, 16);
  display.print("I: "); display.print(Irms, 3); display.println("A");

  display.setCursor(0, 32);
  display.print("P: "); display.print(Power, 2); display.println("W");

  display.setCursor(0, 48);
  display.print("kWh: "); display.print(kWh, 4);

  display.setCursor(80, 48);
  display.print("Rs: "); display.print(cost, 2);

  display.display();

  delay(5000);
}