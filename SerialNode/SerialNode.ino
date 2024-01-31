//EDAC Labs 2024
//This firmware handles analog/digital/i2c to serial.

#include <Wire.h>
#include "DAQActuator.h"

#define PUMPRELAYPIN 2
#define PUMPPWMPIN 9

void querySensor(uint8_t nodeID, uint8_t sensorID){
	Wire.beginTransmission(nodeID);
	Wire.write(2);	//Get Sensor output
	Wire.write(sensorID);	//Get this sensor
	Wire.endTransmission();

	//Get ID, type, and value from one sensor. Last byte is if more sensors available
	Wire.requestFrom(nodeID, 4);
	uint8_t id = Wire.read();
	uint8_t type = Wire.read();
	uint8_t valueHigh = Wire.read();
	uint8_t valueLow = Wire.read();

	uint16_t value = ((uint16_t)valueHigh<<8) + valueLow;

	Serial.print("DATA\t");
	Serial.print(nodeID);
	Serial.print('\t');
	Serial.print(id);
	Serial.print('\t');
	Serial.print(type);
	Serial.print('\t');
	Serial.println(value);
}

void setup() {
	Serial.begin(115200);
	Serial.println("Copyright EDAC Labs 2024");
	Serial.println("Data Acquisition Serial Node");

	Wire.begin();


	//Temporary controls for pump
	pinMode(PUMPRELAYPIN, OUTPUT);
	pinMode(PUMPPWMPIN, OUTPUT);
	//analogWrite(PUMPPWMPIN, 127);
	digitalWrite(PUMPPWMPIN, 0);
	digitalWrite(PUMPRELAYPIN, 1);


}

void loop() {
	querySensor(1, 0);
	delay(1000);
}
