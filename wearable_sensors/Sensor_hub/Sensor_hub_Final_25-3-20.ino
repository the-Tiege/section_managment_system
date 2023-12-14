#include <avr/sleep.h>
#include "Bat_level.h"
#include "my_gps.h"
#include "my_heartrate.h"
#include "Coms.h"
#include "ID.h"

my_gps gps;
Bat_level Bat(A3);
my_heartrate pulse;
Coms Com;
ID id;


bool Sensor = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  Com.coms_setup();//Calls set up function for serial communication
 
  id.Setup_rfid();//Calls set up function for RFID Reader
  gps.GPS_Setup();//Calls set up function for GPS
  pulse.Heart_Rate_Setup();//Calls set up function for Heart rate monitor
  Bat.setup_Bat();//Calls set up function for Battery level reader

  pinMode(LED_BUILTIN,OUTPUT);

  digitalWrite(LED_BUILTIN,HIGH);//Indicates arduino is awake.


  delay(500);

  Com.SerialSend("Ident:0");//Identity unconfirmed

  Serial.println("waiting");
  
  while(!id.ID_check())//Wait until card is read
  {
    //Serial.println("waiting");
  }
  

  Com.SerialSend("Ident:1");//Sent when Identity is confirmed

  Going_To_Sleep();//Arduino sleep function.

  

}
void loop() 
{


  Serial.println("Checking");
  delay(15);//When the ESP 32 wakes the Arduino if it holds the logic level on pin 2 LOW for longer than this delay it will return GPS coordinates, 
            //If it is not held for longer than this delay 
            //Then it is sending an esp-now message to translate.
  while(!Com.check_for_message())
  {
    
    if(digitalRead(2)==LOW)
    {
      Com.SerialSend(pulse.detect_heart_rate() + ",Batery:" + String(Bat.read_Bat_level()) + gps.readGPS());//Reads heartrate gps location 
                                                                                                      //and battery level and sends them to the sensor hub.
      break;
     
    }
  }
  
  Going_To_Sleep();//Arduino sleep function. 
}
void Going_To_Sleep()//Sets up arduino to go to sleep.
{
  Serial.println("Going to Sleep");
  digitalWrite(5,HIGH);
  Sensor=false;
  sleep_enable();//enables sleep mode.
  attachInterrupt(0,wakeup,LOW);//Interrupt for when trigger is pulled
  //attachInterrupt(1,wakeup,LOW);//Interrupt for when ESP wakes the arduino to check its battery level.
  set_sleep_mode(SLEEP_MODE_PWR_DOWN);//Sets sleep mode to power down
  digitalWrite(LED_BUILTIN,LOW);//Turns off built in LED to indicate Arduino is asleep
  delay(1000);
  sleep_cpu();//puts arduino to sleep.
  Serial.println("Woke up!");//Indicates arduino is awake.
  digitalWrite(LED_BUILTIN,HIGH);//Indicates arduino is awake.
}
void wakeup()
{
  Serial.println("interrupt fired");//Indicates that the Interrupt was triggered.
  sleep_disable();//Wakes arduino
  detachInterrupt(0);//Disables interrupt
  //detachInterrupt(1);//Disables interrupt
  digitalWrite(5,LOW);
  Sensor=true;
}
