#include "Arduino.h"
#include "Coms.h"
#include "my_gps.h"

my_gps gps1;


Coms::Coms()
{
  
  
}
void Coms::coms_setup()//Sets up pins and serial used to communicate with ESP 32
{
    Serial2.begin(9600);//Using Serial2

    pinMode(5,OUTPUT);//Pin 5 used as an output. Held LOW by arduino to alert ESP 32 that it has a message to send.
    digitalWrite(5,LOW);//Written LOW initally, as long as arduino is awake pin 5 is held LOW. Written HIGH before entering Sleep

    pinMode(2,INPUT_PULLUP);//Interrupt pin used to wake arduino. Input pullup to prevent undefined logic levels.
    
}
bool Coms::check_for_message()
{
       
    String message = "";//String to contain message to be sent
    
    
      if(Serial2.read()=='H')//When the Header 'H' is read from the serial integer values after header parsed into variables.
      {
        sensor = Serial2.parseInt();
        battery = Serial2.parseInt();
        info = Serial2.parseInt();
                                
        Serial2.flush();
                
        //if the sensor information read from the serial is greater than 0 it means that a round has been fired or an impact has been detected on the body armour
        //in this case a gps location will also need to be sent. If it is zero then it is just sending a battery report and it does not need a GPS location.
        if(info>0)
        {
          message = translate(sensor,battery,info)+ gps1.readGPS();
        }
        else
        {
          message = translate(sensor,battery,info);
        }
        
        delay(500);
        SerialSend(message);
        

        return true;
      }
      else
      {
        return false;
      }

  
   
}
void Coms::SerialSend(String message)
{
  
  Serial.println("waiting");
  while(Serial2.available()==0)
  {
    

  }
  Serial2.flush();
  
  Serial2.println(message + "F");
  Serial.println(message + "F");

  
  
  
}/*
In this function the values sent from the ESP 32 to the Arduino mega are entered into a switch case statement. 
Which case is used is controlled by the int value sensor. 
A value of one means it is sensor 1 and it is the ammunition tracker, it is then translated into a comma and colon separated string.

*/
String Coms::translate(int sensor,int battery, int info )
{
    String message = " ";
  
    switch(sensor)
    {
      case 1 :  message = "RifleBat:" + String(battery)+ "," + "Rndsfired:" + String(info);
                break;

      case 2 :  message = "ArmourBat:" + String(battery) + "," + "State:" + String(info);
                break;

      default : Serial.println("Something Went Wrong");
                break;
  
  }

  return message;
}
