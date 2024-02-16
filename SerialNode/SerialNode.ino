//EDAC Labs 2024
//This firmware handles analog/digital/i2c to serial.

#include <Wire.h>
#include "DAQActuator.h"
#include "Timer.h"

#define NUMSENSORS 16
#define NUMFIELDS 4

Timer queryTimer(100);

uint16_t potVal;

void querySensor(uint8_t nodeID, uint8_t sensorID){
	Wire.beginTransmission(nodeID);
	Wire.write(2);	//Get Sensor output
	Wire.write(sensorID);	//Get this sensor
	Wire.endTransmission();

	//Get ID, type, and value from one sensor. Last byte is if more sensors available
	Wire.requestFrom(nodeID, NUMFIELDS);
	uint8_t id = Wire.read();
	uint8_t type = Wire.read();
	uint8_t valueHigh = Wire.read();
	uint8_t valueLow = Wire.read();

	uint16_t value = ((uint16_t)valueHigh<<8) + valueLow;

	/*Serial.print("DATA\t");
	Serial.print(nodeID);
	Serial.print('\t');
	Serial.print(id);
	Serial.print('\t');
	Serial.print(type);
	Serial.print('\t');
	Serial.println(value);*/
	Serial.print(nodeID);
	Serial.print(',');
	Serial.print(id);
	Serial.print(',');
	Serial.print(type);
	Serial.print(',');
	Serial.print(value);
	Serial.print(',');
}

void printHeader(uint8_t numSensors, uint8_t numFields){
	Serial.print("HEADER,");
	for(uint8_t i=0; i<numSensors; i++){
		for(uint8_t j=0; j<numFields; j++){
			/*Serial.print("Sensor ID ");
			Serial.print(i);
			Serial.print(" field ");
			Serial.print(j);
			Serial.print(",");*/
			Serial.print(i);
			Serial.print(":");
			Serial.print(j);
			Serial.print(",");
		}
	}
	Serial.println();
}

void setup() {
	Serial.begin(115200);
	Serial.println("Copyright EDAC Labs 2024");
	Serial.println("Data Acquisition Serial Node");

	Wire.begin();

	printHeader(NUMSENSORS, NUMFIELDS);
}

void loop() {
	if(queryTimer.check()){
		Serial.print("DATA,");
		for(uint8_t i=0; i<NUMSENSORS; i++){
			querySensor(1, i);
			delay(5);
		}

		Serial.println();
	}
}
