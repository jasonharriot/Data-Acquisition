#include <Arduino.h>
#include "Timer.h"

Timer::Timer(uint32_t x){
	uint32_t now = millis();
	lastTime = now;
	
	interval = x;
}

void Timer::reset(){
	uint32_t now = millis();
	lastTime = now;
}

uint8_t Timer::check(){
	uint32_t now = millis();
	if(now-lastTime > interval){
		lastTime += interval;
		return 1;
	}
	return 0;
}