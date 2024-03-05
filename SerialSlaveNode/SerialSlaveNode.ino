//EDACL Labs 2024
//This sketch is for one (1) arduino board which shall have the address:
#define I2CADDR 0x01
//This board shall be a slave node on the sensor network and respond to the master node with sensor data.

#include "Timer.h"
#include <Wire.h>
//#include "DAQSensor.h"
#include "I2CSlave.h"

//#define PUMPPWMPIN 8
//#define PUMPRELAYPIN 9

#define ALARMPIN 11

I2CSlave slave;

Timer safetyTimer(1000);
uint8_t safe = 0;



//Analog Sensors, RTDs
AnalogSensor sensor1(A0, 0);
AnalogSensor sensor2(A1, 1);
AnalogSensor sensor3(A2, 2);
AnalogSensor sensor4(A3, 3);

//Digital Sensors
DigitalSensor tankLo(12, 4, 0);
DigitalSensor tankHi(13, 5, 0);

//Pressure
AnalogSensor pt1(A10, 11);
AnalogSensor pt2(A11, 10);
AnalogSensor pt3(A12, 9);
AnalogSensor pt4(A13, 8);
AnalogSensor pt5(A14, 7);
AnalogSensor pt6(A15, 6);

//Flow
AnalogSensor fq3(A9, 12);
AnalogSensor fq2(A8, 13);
AnalogSensor fq1(A7, 14);

//Potentiometer
AnalogSensor pot(A6, 15);











void unSafe(){
	safe = 0;
	safetyTimer.reset();
}







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

	pinMode(slave.pumpPWMPin, OUTPUT);
	pinMode(ALARMPIN, OUTPUT);
	Serial.println("Serial slave node ready!");
}

void loop() {
	slave.update();

	if(safetyTimer.check()){	//It is safe only after the timer expires
		safe = 1;
	}


	//Safety checks
	//Pressure check
	double pres1 = pt1.getValue()*.061050-12.45;
	double pres2 = pt2.getValue()*.061050-12.45;
	double pres3 = pt3.getValue()*.061050-12.45;
	double pres4 = pt4.getValue()*.061050-12.45;
	double pres5 = pt5.getValue()*.061050-12.45;
	double pres6 = pt6.getValue()*.061050-12.45;

	double maxPres = 0;
	maxPres = max(pres1, maxPres);	//PSI gauge
	maxPres = max(pres2, maxPres);
	maxPres = max(pres3, maxPres);
	maxPres = max(pres4, maxPres);
	maxPres = max(pres5, maxPres);
	maxPres = max(pres6, maxPres);

	//Serial.print("Highest pressure: ");
	//Serial.println(maxPres);
	
	if(maxPres >= 30){	//2 Bar
		Serial.println("Overpressure!");
		unSafe();
	}

	//Tank low level
	if(!tankLo.getValue()){
		Serial.println("Tank level low!");
		unSafe();
	}

	

	if(safe){	//Safe condition outputs
		digitalWrite(ALARMPIN, 0);
		analogWrite(slave.pumpPWMPin, pot.getValue()/4);
		
	} else{	//Unsafe condition outputs
		//Disable pumps, etc.
		//Sound alarm
		digitalWrite(ALARMPIN, 1);
		analogWrite(slave.pumpPWMPin, 0);
	}
}
