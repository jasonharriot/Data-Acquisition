#ifndef I2CSLAVE_H
#define I2CSLAVE_H

#include <arduino.h>
#include "DAQSensor.h"

#define NUMSENSORS 256
#define BUFSIZE 16

class I2CSlave{
	public:
		I2CSlave();
		uint8_t init();
		uint8_t add(Sensor*);
		uint8_t getSensorCount();
		Sensor* getSensor(uint8_t);
		void onRequest();
		void onReceive(int);
		
		void update();
		
		void setActuator(uint8_t, uint8_t);
		
		int pump1PWMPin = 8;
		int pump2RelayPin = 10;
		
		
	private:
		//volatile uint8_t v_command;
		volatile uint8_t v_command;
		volatile uint8_t v_data [BUFSIZE] = {0};
		volatile uint8_t v_dataFlag;
		volatile uint8_t numSensorsLastReported;
		volatile uint8_t lastValHigh;
		volatile uint8_t lastValLow;
		uint8_t address;
		Sensor* sensors[NUMSENSORS] = {(Sensor*)0};
};

#endif