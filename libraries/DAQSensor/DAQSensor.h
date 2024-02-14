#ifndef DAQSENSOR_H
#define DAQSENSOR_H

#include <arduino.h>

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
		
		Sensor(uint8_t, uint8_t);
		uint8_t init();
		void summary();
		uint8_t deliver();
		uint8_t getType();
		uint16_t getValue();
		uint8_t getID();
		virtual uint8_t read();
		uint32_t lastReadTime;
		void setValue(uint16_t);

	protected:
		uint16_t value;
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
		AnalogSensor(uint8_t, uint8_t);
		uint8_t read();
};

class I2CSensor:public Sensor{
	public:
		uint8_t read();
};

class DigitalSensor:public Sensor{
	public:
		DigitalSensor(uint8_t, uint8_t, uint8_t);
		uint8_t read();
};

class PulseSensor:public Sensor{
	public:
		uint8_t read();
};

class PWMSensor:public Sensor{
	public:
		uint8_t read();
};

#endif
