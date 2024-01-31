//EDACL Labs 2024
//This sketch is for one (1) arduino board which shall have the address:
#define I2CADDR 0x01
//This board shall be a slave node on the sensor network and respond to the master node with sensor data.

#include "Timer.h"
#include <Wire.h>
//#include "DAQSensor.h"
#include "I2CSlave.h"

I2CSlave slave;

//Sensor testSensor(13, 99);

AnalogSensor sensor1(A0, 1);
DigitalSensor sensor2(12, 2, true);
DigitalSensor sensor3(10, 3, true);
DigitalSensor sensor4(10, 4, true);

void onRequest(){
	slave.onRequest();
}

void onReceive(int nBytes){
	slave.onReceive(nBytes);
}

void setup() {
	Serial.begin(115200);
	Wire.begin(I2CADDR);

	slave.add(&sensor1);
	slave.add(&sensor2);
	slave.add(&sensor3);
	slave.add(&sensor4);

	Wire.onRequest(onRequest);
	Wire.onReceive(onReceive);

	Serial.println("Serial slave node ready!");
}

void loop() {
	slave.update();
	/*Sensor * sensor = slave.getSensor(0);

	Serial.print("Sensor with index 0 stuff: ");
			
	Serial.println(sensor->getID());
	Serial.println(sensor->getType());
	
	uint16_t value = sensor->getValue();
	uint8_t valueHigh = value>>8;
	uint8_t valueLow = value & 255;

	Serial.println(value);
	Serial.println(valueHigh);
	Serial.println(valueLow);*/
	delay(100);
}
