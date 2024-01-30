//EDACL Labs 2024
//This sketch is for one (1) arduino board which shall have the address:
#define I2CADDR 0x01
//This board shall be a slave node on the sensor network and respond to the master node with sensor data.

#include "I2CSlave.h"
#include "Timer.h"

I2CSlave slave(I2CADDR);

void setup() {
	Serial.begin(115200);
	slave.init();

	Serial.println("Serial slave node ready!");
}

void loop() {
}
