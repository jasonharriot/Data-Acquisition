//EDAC Labs 2024
//This firmware handles analog/digital/i2c to serial.

#include <Wire.h>
#include "DAQSensor.h"

Sensor sensor0(9, 0);
AnalogSensor sensor1(A0, 1);
DigitalSensor sensor2(12, 2, true);

void setup() {
  Serial.begin(115200);
  Serial.println("Copyright EDAC Labs 2024");
  Serial.println("Data Acquisition Serial Node");

  sensor0.init();
  sensor1.init();
  sensor2.init();


  sensor1.summary();
  sensor2.summary();
}

void loop() {
  
  
  sensor1.read();
  //sensor1.deliver();

  sensor2.read();
  //sensor2.deliver();
  sensor2.summary();

  delay(1000);
}
