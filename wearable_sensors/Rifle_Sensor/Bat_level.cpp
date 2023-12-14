#include "Arduino.h"
#include "Bat_level.h"


Bat_level::Bat_level(int pin)
{
  readPin = pin;
}
int Bat_level::read_Bat_level()
{
   
  float Bat = analogRead(readPin);//Read Analogue input of battery voltage level
  delay(10);

  Bat = map(Bat,0,1023,0,6600);//map read value from between 0 and 1023 to between 0 and 6600, when fully charged the battery level is 6.6v.

  Bat = (Bat/1000.0);//The map function only returns integer values. so to get decimal values the voltage is mapped between 0 and 6600 then divided by 1000

  Battery = ((Bat-5)/1.6)*100.0;//Get voltage level as a persentage

  return Battery + 10;//return battery level
}
void Bat_level::setup_Bat()
{
  analogReference(EXTERNAL);//Use external reference of 3.3v
}
