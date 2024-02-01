#include <Wire.h>
#include "I2CSlave.h"
#include "DAQSensor.h"


uint8_t I2CSlave::init(){
	return 1;
}

uint8_t I2CSlave::add(Sensor* x){
	uint8_t currentSensorCount = getSensorCount();
	sensors[x->getID()] = x;
	x->init();
	//Serial.println("Added and initialized sensor");
	//Serial.println(currentSensorCount);
	return 1;
}

uint8_t I2CSlave::getSensorCount(){
	for(uint8_t i=0;; i++){
		if(sensors[i] == 0){
			return i;
		}
	}
	return 0;
}

Sensor * I2CSlave::getSensor(uint8_t s){	//Index is taken to be the ID because sensors are added to the list by it.
	return sensors[s];
}

void I2CSlave::onRequest(){
	uint8_t count, sensorIndex, valueHigh, valueLow;
	uint16_t value;
	Sensor * sensor;
	switch(v_command){
		case 1:
			count = getSensorCount();
			Wire.write(count);
			numSensorsLastReported = count;
			break;
		case 2:
			//Report sensor data. Sensor index is first parameter
			sensorIndex = v_data[0];
			sensor = getSensor(sensorIndex);
			
			Wire.write(sensor->getID());
			Wire.write(sensor->getType());
			
			value = sensor->getValue();
			valueHigh = value>>8;
			valueLow = value & 255;
			Wire.write(valueHigh);
			Wire.write(valueLow);
			lastValHigh = valueHigh;
			lastValLow = valueLow;
			break;
		default:
			break;
	}
}

void I2CSlave::onReceive(int nBytes){
	v_command = Wire.read();
	for(uint8_t i=0; Wire.available(); i++){
		uint8_t x = Wire.read();
		v_data[i] = x;
	}
	
	v_dataFlag = 1;
}

void I2CSlave::update(){
	for(uint8_t i=0; i<getSensorCount(); i++){
		getSensor(i)->read();
	}
	
	if(v_dataFlag){
		v_dataFlag = 0;
		for(uint8_t i=0; i<BUFSIZE; i++){
			Serial.print(v_data[i]);
		}
		Serial.println();
		
		Serial.print("Command: ");
		Serial.print(v_command);
		Serial.println();
	}
	
	//Serial.print("Last report: ");
	//Serial.println(numSensorsLastReported);
	
	//uint8_t data = v_data;
	
	/*uint8_t repSize = 0;
	switch(data){
		case 0:
			Serial.println("Preparing report");
			repSize = 1 + getSensorCount();
			Serial.print("Sending report size: ");
			Serial.print(repSize);
			Serial.println();
			Wire.write(repSize);
			for(uint8_t i = 0; i < getSensorCount(); i++){
				Wire.write(getSensor(i)->getType());
			}
			break;
		case 1:
			Serial.println("Preparing readout");
			break;
			
		default:
			Serial.println("Unknown command");
			break;
	}
	
	Serial.println("Done responding.");*/
}