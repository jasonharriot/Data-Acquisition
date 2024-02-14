//EDAC Labs 2024
//This firmware handles analog/digital/i2c to serial.

#include <Wire.h>
#include "DAQActuator.h"
#include "Timer.h"

#define PUMPRELAYPIN 2
#define PUMPPWMPIN 9
#define POTPIN A0

Timer queryTimer(1000);

uint16_t potVal;

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
	pinMode(POTPIN, INPUT);
	analogWrite(PUMPPWMPIN, 0);
	digitalWrite(PUMPRELAYPIN, 1);	//Turn on/off the pump
}

void loop() {
	if(queryTimer.check()){
		/*querySensor(1, 0);
		querySensor(1, 1);
		querySensor(1, 2);
		querySensor(1, 3);

		
		querySensor(1, 6);
		querySensor(1, 7);
		querySensor(1, 8);
		querySensor(1, 9);
		querySensor(1, 10);
		querySensor(1, 11);

		querySensor(1, 12);
		querySensor(1, 13);*/

		for(uint8_t i=0; i<=14; i++){
			querySensor(1, i);
		}

		Serial.print("DATA\t0\t0\t0\t");	//Special data line for the control
		Serial.print(potVal);
		Serial.println();
	}

	potVal = analogRead(POTPIN);
	analogWrite(PUMPPWMPIN, potVal/4);
}
