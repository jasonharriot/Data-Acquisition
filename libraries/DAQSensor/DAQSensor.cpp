#include "DAQSensor.h"
                        //.        .        .        .        .        .
char sensorTypeNames[] = "PROTO\0  ANALOG\0 I2C\0    DIGITAL\0PULSE\0  PWM\0";

Sensor::Sensor(uint8_t pin, uint8_t idx){
	id = idx;
	arduinoPin = pin;
}
	
uint8_t Sensor::init(){
	name = sensorTypeNames+((type)*8);
	
	isInitialized = 1;
	Serial.print("Initialized sensor with ID ");
	Serial.println(id);
}

uint8_t Sensor::read(){
	Serial.println("Base class read!");
}

void Sensor::summary(){
	Serial.println("======== Sensor Summary ========");
	Serial.print(name);
	Serial.print(" (");
	Serial.print(type);
	Serial.println(")");
	
	Serial.print("ID\t");
	Serial.println(id);
	
	Serial.print("Value\t");
	Serial.println(value);
	
	Serial.print("Yield?\t");
	Serial.println(yield);
	
	//Serial.print("Pullup?\t");
	//Serial.println(pullup);
	
	Serial.print("Initialized?\t");
	Serial.println(isInitialized);
	
	Serial.print("Arduino pin\t");
	Serial.println(arduinoPin);
	
	Serial.print("Last read time\t");
	Serial.println(lastReadTime);
}

uint8_t Sensor::deliver(){
	if(!yield){	//If there is no data to deliver
		Serial.print("ERROR no yield");
		return 1;
	}
	
	//Serial.print("DATA ");
	Serial.print(id);
	Serial.print(',');
	Serial.print(type);
	Serial.print(',');
	Serial.print(value);
	
	Serial.println();
	
	return 0;
}

uint8_t Sensor::getType(){
	return type;
}

uint16_t Sensor::getValue(){
	return value;
}

uint8_t Sensor::getID(){
	return id;
}



AnalogSensor::AnalogSensor(uint8_t pin, uint8_t id) : Sensor(pin, id){
	type = SENSOR_ANALOG;
	pinMode(arduinoPin, INPUT);
}

uint8_t AnalogSensor::read(){
	yield = 0;
	if(!isInitialized){	//Refuse to read if not initialized
		Serial.println("ERROR analog sensor not initialized");
		return 1;
	}
	
	uint16_t reading = analogRead(arduinoPin);	//arduinoPin may be incorrect but there's no good way to detect
	lastReadTime = millis();
	
	
	//Reading-to-celcius conversion. Don't use this unless the value parameter is set up for double.
	//value = map(reading, 0.0, 1023.0, 10.0, 25.0);
	//double minTemp = 10;
	//double maxTemp = 25;
	//value = (reading/1024.0)*(maxtemp-minTemp)+minTemp;
	
	
	value = reading;	//Transmit raw value from ADC.
	yield = 1;
	
	return 0;
}




DigitalSensor::DigitalSensor(uint8_t pin, uint8_t id, uint8_t pullup) : Sensor(pin, id){
	type = SENSOR_DIGITAL;
	pinMode(arduinoPin, INPUT);
	digitalWrite(arduinoPin, pullup);
}

uint8_t DigitalSensor::read(){
	yield = 0;
	if(!isInitialized){	//Refuse to read if not initialized
		Serial.println("ERROR digital sensor not initialized");
		return 1;
	}
	
	value = digitalRead(arduinoPin);	//arduinoPin may be incorrect but there's no good way to detect
	lastReadTime = millis();
	yield = 1;
	
	return 0;
}