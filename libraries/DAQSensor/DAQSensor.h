#ifndef DAQSENSOR_H
#define DAQSENSOR_H

#include <Arduino.h>

#define SENSOR_PROTO 0
#define SENSOR_ANALOG 1
#define SENSOR_I2C 2
#define SENSOR_DIGITAL 3
#define SENSOR_PULSE 4
#define SENSOR_PWM 5

extern char sensorTypeNames[];

class Sensor{
	public:	

		//uint8_t value;
		double value;


	
		Sensor(uint8_t pin, uint8_t idx){
			id = idx;
			arduinoPin = pin;
		}
		
		uint8_t init(){
			name = sensorTypeNames+((type)*8);
			
			isInitialized = 1;
		}
		
		void summary(){
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
		}
		
		uint8_t deliver(){
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
		
	protected:
		uint8_t id;
		uint8_t type;
		
		
		
		uint8_t yield;
		
		//uint8_t pullup;
		uint8_t isInitialized;
		uint8_t arduinoPin;
		char * name;
};

class AnalogSensor:public Sensor{
	public:
		AnalogSensor(uint8_t pin, uint8_t id) : Sensor(pin, id){
			type = SENSOR_ANALOG;
			pinMode(arduinoPin, INPUT);
		}
		
		uint8_t read(){
			yield = 0;
			if(!isInitialized){	//Refuse to read if not initialized
				Serial.println("ERROR analog sensor not initialized");
				return 1;
			}
			
			double reading = analogRead(arduinoPin);	//arduinoPin may be incorrect but there's no good way to detect
			//value = map(reading, 0.0, 1023.0, 10.0, 25.0);
			value = (reading/1024.0)*(25.0-10.0)+10.0;
			yield = 1;
			
			return 0;
		}
};

class I2CSensor:public Sensor{
};

class DigitalSensor:public Sensor{
	public:
		DigitalSensor(uint8_t pin, uint8_t id, uint8_t pullup) : Sensor(pin, id){
			type = SENSOR_DIGITAL;
			pinMode(arduinoPin, INPUT);
			digitalWrite(arduinoPin, pullup);
		}
		
		uint8_t read(){
			yield = 0;
			if(!isInitialized){	//Refuse to read if not initialized
				Serial.println("ERROR digital sensor not initialized");
				return 1;
			}
			
			value = digitalRead(arduinoPin);	//arduinoPin may be incorrect but there's no good way to detect
			yield = 1;
			
			return 0;
		}
};

class PulseSensor:public Sensor{
};

class PWMSensor:public Sensor{
};

#endif
