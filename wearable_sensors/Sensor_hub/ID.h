#ifndef ID_h
#define ID_h

#include "Arduino.h"






class ID
{
  public:

  ID();//constructor
  void Setup_rfid();//Setup for RFID reader
  bool ID_check();//Function to check for RFID card
  
 
  private:

  byte nuidPICC[4];//four byte array to store UID
  const String access = "35236227";//UID of accepted card
  String inputNum = "";

};

#endif
