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

AnalogSensor sensor1(A0, 0);	//TODO: Assign IDs
AnalogSensor sensor2(A1, 1);
AnalogSensor sensor3(A2, 2);
AnalogSensor sensor4(A3, 3);

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
	delay(100);
}
