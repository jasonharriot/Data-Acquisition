#ifndef I2CSLAVE_H
#define I2CSLAVE_H
#include <arduino.h>

class I2CSlave{
	public:
	I2CSlave(uint8_t);
	
	uint8_t init();
	
	private:
	uint8_t address;
};

#endif