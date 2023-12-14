#ifndef my_gps_h
#define my_gps_h

#include "Arduino.h"
#include <Adafruit_GPS.h>






class my_gps
{
  public:

  my_gps();//Constructor
  void GPS_Setup();//GPS setup
  String readGPS();//Reads data from GPS
  String TIME();//Reads Time fromGPS
  
 
  private:

  void clearGPS();//Clear junk data from GPS
  String ConvertLatLong();//Convert latitude and longitude to decimal degrees

  

};

#endif
