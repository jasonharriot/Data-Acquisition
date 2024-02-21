//EDACL Labs 2024
//This sketch is for one (1) arduino board which shall have the address:
#define I2CADDR 0x01
//This board shall be a slave node on the sensor network and respond to the master node with sensor data.

#include "Timer.h"
#include <Wire.h>
//#include "DAQSensor.h"
#include "I2CSlave.h"

#define PUMPPWMPIN 8
#define PUMPRELAYPIN 9

I2CSlave slave;

//Sensor testSensor(13, 99);






//Analog Sensors, RTDs
AnalogSensor sensor1(A0, 0);
AnalogSensor sensor2(A1, 1);
AnalogSensor sensor3(A2, 2);
AnalogSensor sensor4(A3, 3);

//Digital Sensors
DigitalSensor tankLo(12, 4, 0);
DigitalSensor tankHi(13, 5, 0);

//Pressure
AnalogSensor pt1(A15, 6);
AnalogSensor pt2(A14, 7);
AnalogSensor pt3(A13, 8);
AnalogSensor pt4(A12, 9);
AnalogSensor pt5(A11, 10);
AnalogSensor pt6(A10, 11);

//Flow
AnalogSensor fq3(A9, 12);
AnalogSensor fq2(A8, 13);
AnalogSensor fq1(A7, 14);

//Potentiometer
AnalogSensor pot(A6, 15);



















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

	slave.add(&tankLo);
	slave.add(&tankHi);

	slave.add(&pt1);
	slave.add(&pt2);
	slave.add(&pt3);
	slave.add(&pt4);
	slave.add(&pt5);
	slave.add(&pt6);

	slave.add(&fq1);
	slave.add(&fq2);
	slave.add(&fq3);

	slave.add(&pot);

	Wire.onRequest(onRequest);
	Wire.onReceive(onReceive);

	pinMode(PUMPPWMPIN, OUTPUT);

	digitalWrite(PUMPRELAYPIN, 1);

	Serial.println("Serial slave node ready!");
}

void loop() {
	slave.update();
	//sensor1.summary();
	//pt1.summary();
	analogWrite(PUMPPWMPIN, pot.getValue()/4);	//Special output for pump
	delay(100);
}
