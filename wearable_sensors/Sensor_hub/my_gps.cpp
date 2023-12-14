#include "Arduino.h"
#include <Adafruit_GPS.h>
#include "my_gps.h"

#define GPSSerial Serial1
Adafruit_GPS GPS(&GPSSerial);



my_gps::my_gps()
{
  
}
void my_gps::GPS_Setup()
{
   GPS.begin(9600);

  GPS.sendCommand("$PGCND,30,0*6D");//turn off antenna data.
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_10HZ);//Set speed to 10HZ
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);//Request RMC and GGA Data only
  delay(1000);
}
String my_gps::readGPS()
{
  char c;
  String NMEA1; //Variable for first NMEA sentence
  String NMEA2; //Variable for second NMEA sentence
  String message = " ";

  //Serial.println("GPS Begin);
  
  clearGPS();

  while(!GPS.newNMEAreceived())
  {
    c=GPS.read();
  }

  GPS.parse(GPS.lastNMEA());
  NMEA1=GPS.lastNMEA();
  

  while(!GPS.newNMEAreceived())
  {
    c=GPS.read();
  }

  GPS.parse(GPS.lastNMEA());
  NMEA2=GPS.lastNMEA();

  if(GPS.fix==1)
  {

    message = ConvertLatLong();
    
  }
  else
  {
    Serial.println("No Fix");
    message = "F";
  }

  
  //Serial.println("GPS End);

  return message;
  
}
void my_gps::clearGPS()
{
    
    char c;
   
  while(!GPS.newNMEAreceived())
  {
    c=GPS.read();
  }
  GPS.parse(GPS.lastNMEA());
  
  while(!GPS.newNMEAreceived())
  {
    c=GPS.read();
  }
  GPS.parse(GPS.lastNMEA());

  while(!GPS.newNMEAreceived())
  {
    c=GPS.read();
  }
  GPS.parse(GPS.lastNMEA());

  while(!GPS.newNMEAreceived())
  {
    c=GPS.read();
  }
  GPS.parse(GPS.lastNMEA());

  
}
String my_gps::ConvertLatLong()
{
  float Long = 0, Lat = 0, degWhole = 0, degDec =0;
  String message = " ";
  
  degWhole=float(int(GPS.longitude/100)); //gives me the whole degree part of Longitude
  degDec = (GPS.longitude - degWhole*100)/60; //give me fractional part of longitude
  Long = degWhole + degDec; //Gives complete correct decimal form of Longitude degrees
  if (GPS.lon=='W') {  //If you are in Western Hemisphere, longitude degrees should be negative
    Long= (-1)*Long;
  }
  
  degWhole=float(int(GPS.latitude/100)); //gives me the whole degree part of Longitude
  degDec = (GPS.latitude - degWhole*100)/60; //give me fractional part of longitude
  Lat = degWhole + degDec; //Gives complete correct decimal form of Longitude degrees
  if (GPS.lon=='S') {  //If you are in Western Hemisphere, longitude degrees should be negative
    Lat= (-1)*Lat;
  }

  message = ",long:" + String(Long,5) + "," + "lat:" + String(Lat,5);

  return message;

}
String my_gps::TIME()
{
  return ",TIME:" + String(GPS.hour) + "." +String(GPS.minute) + "." +String(GPS.seconds);
}
