#ifndef I2CSLAVE_H
#define I2CSLAVE_H

#include <arduino.h>
#include "DAQSensor.h"

#define NUMSENSORS 256
#define BUFSIZE 8

class I2CSlave{
	public:
		uint8_t init();
		uint8_t add(Sensor*);
		uint8_t getSensorCount();
		Sensor* getSensor(uint8_t);
		void onRequest();
		void onReceive(int);
		
		void update();
		
		
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