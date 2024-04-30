#include <Wire.h>
#include "I2CSlave.h"
#include "DAQSensor.h"

I2CSlave::I2CSlave(){
	init();
}

uint8_t I2CSlave::init(){
	pinMode(pump1PWMPin, OUTPUT);
	pinMode(pump2RelayPin, OUTPUT);
	return 1;
}

uint8_t I2CSlave::add(Sensor* x){
	sensors[getSensorCount()] = x;
	x->init();
	Serial.println("Added and initialized sensor.");
	Serial.print(getSensorCount());
	Serial.println(" sensors.");
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
	for(uint8_t i=0; i<getSensorCount(); i++){
		//Serial.print("Finding sensor ");
		//Serial.print(s);
		//Serial.print(": ");
		if(sensors[i]->getID()==s){
			return sensors[i];
		}
	}
	
	//return sensors[s];
	return (Sensor*) 0;
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
			if(!sensor) break;
			
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
	
	memset(v_data, 0, BUFSIZE);
	for(uint8_t i=0; Wire.available(); i++){
		uint8_t x = Wire.read();
		v_data[i] = x;
	}
	
	v_dataFlag = 1;
	
	switch(v_command){	//Blind commands (no response)
		case 3:
			//Set actuator state
			setActuator(v_data[0], v_data[1]);
			break;
	}
}


void I2CSlave::setActuator(uint8_t actuatorID, uint8_t actuatorValue){
	//Hardcoded actuators. Can't bother to be dynamic.
	
	//Serial.print("Actuator: ");
	//Serial.println(actuatorID);
	//Serial.print("Value: ");
	//Serial.println(actuatorValue);
	
	switch(actuatorID){
		case 0:
			analogWrite(pump1PWMPin, actuatorValue);
			break;
			
		default:
			break;
	}
}

void I2CSlave::update(){
	//Serial.print("Updating ");
	//Serial.print(getSensorCount());
	//Serial.println(" sensors...");
	for(uint8_t i=0; i<getSensorCount(); i++){
		Sensor* sens = sensors[i];
		if(!sens) continue;
		//Serial.print("Reading sensor ");
		//Serial.println(sens->getID());
		sens->read();
	}
	
	if(v_dataFlag){
		//Serial.print("Command Recv'd (");
		//Serial.print(v_command);
		//Serial.print("): ");
		for(uint8_t i=0; i<BUFSIZE; i++){
			//Serial.print(v_data[i]);
			//Serial.print(' ');
		}
		//Serial.println();
		
		v_dataFlag = 0;
		
		
		
		
	}
}