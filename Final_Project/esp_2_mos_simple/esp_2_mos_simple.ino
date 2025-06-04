#include "EmonLib.h"
#include <EEPROM.h>

// Calibration constants
const float vCalibration = 41.5;
const float currCalibration = 0.15;

// EnergyMonitor instance
EnergyMonitor emon;

// Energy tracking
float kWh = 0.0;
unsigned long lastMillis = millis();

// EEPROM address for kWh storage
const int addrKWh = 12;

void setup()
{
  Serial.begin(115200);

  // Initialize EEPROM
  EEPROM.begin(32);

  // Restore stored energy value
  readEnergyDataFromEEPROM();

  // Configure voltage and current input pins
  emon.voltage(35, vCalibration, 1.7); // Voltage: pin 
  emon.current(38, currCalibration);   // Current: pin 

  delay(1000); // Wait for stabilization
}

void loop()
{
  emon.calcVI(20, 2000); // Sample 20 cycles

  // Update energy usage
  unsigned long currentMillis = millis();
  kWh += emon.apparentPower * (currentMillis - lastMillis) / 3600000000.0;
  lastMillis = currentMillis;

  // Print to Serial Monitor
  Serial.printf("Vrms: %.2f V\tIrms: %.4f A\tPower: %.4f W\tEnergy: %.5f kWh\n",
                emon.Vrms, emon.Irms, emon.apparentPower, kWh);

  // Save latest kWh to EEPROM
  saveEnergyDataToEEPROM();

  delay(5000); // 5-second interval
}

void readEnergyDataFromEEPROM()
{
  EEPROM.get(addrKWh, kWh);
  if (isnan(kWh))
  {
    kWh = 0.0;
    saveEnergyDataToEEPROM();
  }
}

void saveEnergyDataToEEPROM()
{
  EEPROM.put(addrKWh, kWh);
  EEPROM.commit();
}
