#ifndef TIMER_H
#define TIMER_H

class Timer{
	public:
		Timer(uint32_t);
		
		uint8_t check();
		void reset();
	
	private:
		uint32_t interval;
		uint32_t lastTime;
};

#endif