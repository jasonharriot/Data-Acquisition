#include "I2CSlave.h"
#include <arduino.h>

I2CSlave::I2CSlave(uint8_t addr){
		address = addr;
}

uint8_t I2CSlave::init(){
	return 1;
}
	