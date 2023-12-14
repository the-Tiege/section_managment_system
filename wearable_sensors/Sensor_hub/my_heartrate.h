#ifndef my_heartrate_h
#define my_heartrate_h

#include "Arduino.h"
#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"





class my_heartrate
{
  public:
  my_heartrate();//Constructor
  void Heart_Rate_Setup();//Set up hearth rate monitor
  String detect_heart_rate();

  
  
  private:
  
  
  const byte RATE_SIZE = 4; //Increase this for more averaging. 4 is good.

};



#endif
