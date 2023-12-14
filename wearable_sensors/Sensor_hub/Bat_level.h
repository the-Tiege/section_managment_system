#ifndef Bat_level_h
#define Bat_level_h

#include "Arduino.h"






class Bat_level
{
  public:

  Bat_level(int);//constructor, takes analogue pin as an argument
  void setup_Bat();//Sets up battery read
  int read_Bat_level();//Reads battery level
  
 
  private:

  float Battery = 0; 
  int readPin; 

};

#endif
