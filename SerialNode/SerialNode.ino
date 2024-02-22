//EDAC Labs 2024
//This firmware handles analog/digital/i2c to serial.

#include <Wire.h>
#include "DAQActuator.h"
#include "Timer.h"

#define NUMSENSORS 16
#define NUMFIELDS 4

Timer queryTimer(100);

Timer pumpTestTimer(1000);
uint8_t pumpTestState = 0;

uint16_t potVal;

#define SERIALBUFLEN 32
char serialBuf [SERIALBUFLEN] = {0};

void querySensor(uint8_t nodeID, uint8_t sensorID){
	Wire.beginTransmission(nodeID);
	Wire.write(2);	//Get Sensor output
	Wire.write(sensorID);	//Get this sensor
	Wire.endTransmission();

	//Get ID, type, and value from one sensor.
	Wire.requestFrom(nodeID, NUMFIELDS);
	uint8_t id = Wire.read();
	uint8_t type = Wire.read();
	uint8_t valueHigh = Wire.read();
	uint8_t valueLow = Wire.read();

	uint16_t value = ((uint16_t)valueHigh<<8) + valueLow;
	
	if(id < 255 && type < 255 && value < 1024){
		Serial.print(value);
	} else{
		Serial.print("err");
	}
	Serial.print(',');
}

void printHeader(uint8_t numSensors, uint8_t numFields){
	Serial.print("HEADER,");
	for(uint8_t i=0; i<numSensors; i++){
		//for(uint8_t j=0; j<numFields; j++){
			/*Serial.print("Sensor ID ");
			Serial.print(i);
			Serial.print(" field ");
			Serial.print(j);
			Serial.print(",");*/
			//Serial.print(i);
			//Serial.print(":");
			//Serial.print(j);
			//Serial.print(",");
		//}


		Serial.print(i);
		Serial.print(":3,");	//Only print data field

	}
	Serial.println();
}

uint8_t sendActuatorCommand(char * buf){
	uint8_t nodeID = 0;
	uint8_t actuatorID = 0;
	uint8_t actuatorValue = 0;

	uint8_t i=0;
	char * buf2 = 0;

	nodeID = (uint8_t)(atoi(buf));
	
	buf2 = strchr(buf, ',')+1;
	if(buf2 != 0) actuatorID = (uint8_t)(atoi(buf2));
	
	buf2 = strchr(buf2, ',')+1;
	if(buf2 != 0) actuatorValue = (uint8_t)(atoi(buf2));

	Serial.print("Node ID ");
	Serial.println(nodeID);

	Serial.print("Actuator ID ");
	Serial.println(actuatorID);

	Serial.print("Actuator Value ");
	Serial.println(actuatorValue);

	Wire.beginTransmission(nodeID);
	Wire.write(3);
	Wire.write(actuatorID);
	Wire.write(actuatorValue);
	Wire.endTransmission();
	
	return 0;
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
			//delay(10);
		}

		Serial.println();
	}

	/*if(pumpTestTimer.check()){
		if(pumpTestState){
			sendActuatorCommand("1,0,255");
		} else{
			sendActuatorCommand("1,0,0");
		}

		pumpTestState = !pumpTestState;
	}*/

	if(Serial.available() > 0){
		int received = Serial.read();

		if(received == -1){
			//No data to read
		}

		char ch = (char)(received);
		if(received == '\n'){
			Serial.print("Serial recv: ");
			Serial.println(serialBuf);

			sendActuatorCommand(serialBuf);
			
			memset(serialBuf, 0, SERIALBUFLEN);
		} else if(strlen(serialBuf) < SERIALBUFLEN-1){
			serialBuf[strlen(serialBuf)] = ch;
		}
	}

	
}
