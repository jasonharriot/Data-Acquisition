//EDAC Labs 2024
//This firmware handles analog/digital/i2c to serial.

#include <Wire.h>
#include "DAQSensor.h"
#include "DAQActuator.h"

#define PUMPRELAYPIN 2
#define PUMPPWMPIN 9

Sensor sensor0(9, 0);

AnalogSensor sensor1(A0, 1);
DigitalSensor sensor2(12, 2, true);



void setup() {
  Serial.begin(115200);
  //Serial.println("Copyright EDAC Labs 2024");
  //Serial.println("Data Acquisition Serial Node");
  //Serial.println("ID, Type, Value");

  pinMode(PUMPRELAYPIN, OUTPUT);
  pinMode(PUMPPWMPIN, OUTPUT);

  analogWrite(PUMPPWMPIN, 127);

  sensor0.init();
  sensor1.init();
  sensor2.init();


  //sensor1.summary();
  //sensor2.summary();

  digitalWrite(PUMPRELAYPIN, 1);

  
}

void loop() {                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
  sensor1.read();
  //sensor1.deliver();
  Serial.println(sensor1.value);

  sensor2.read();
  //sensor2.deliver();
  //sensor2.summary();

  /*if(sensor2.value){
    digitalWrite(PUMPRELAYPIN, 0);
  } else{
    digitalWrite(PUMPRELAYPIN, 1);
  }*/

  

  delay(100);
}
