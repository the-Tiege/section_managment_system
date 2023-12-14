#ifndef Coms_h
#define Coms_h

#include "Arduino.h"






class Coms
{
  public:

  Coms();
  void coms_setup();//Set up for serial communication
  bool check_for_message();//Recieve message sent from ESP 32
  void SerialSend(String);//Send message to ESP 32
  
  
 
  private:

  String translate(int,int,int);//Function to translate information sent using ESP now into a string.

  int sensor = 0, info = 0, battery = 0;
  

    

};

#endif
