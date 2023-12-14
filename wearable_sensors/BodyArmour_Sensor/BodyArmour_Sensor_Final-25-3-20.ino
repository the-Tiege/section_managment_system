#include <avr/sleep.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <Adafruit_MMA8451.h>
#include <Adafruit_Sensor.h>
#include "Bat_level.h"

const int rxPin = 10, txPin = 11;//Software Serial RX and TX pins 10 and 11

SoftwareSerial mySerial(rxPin,txPin);//Set RX and TX pins for software Serial.
Adafruit_MMA8451 mma = Adafruit_MMA8451();//Create MMA8451 Object
Bat_level bat(A1);//Create battery read object


const int Battery_check_pin = 3, wakePin = 6;

bool State = false, Battery = false;
float x =0, y = 0, z = 0;





void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  mySerial.begin(9600);

  bat.setup_Bat();
  

  pinMode(9,OUTPUT);
  digitalWrite(9,LOW);
 
  
  pinMode(wakePin,OUTPUT);//wake
  pinMode(Battery_check_pin,INPUT_PULLUP);//recieve
  
  digitalWrite(wakePin,HIGH);

 if (! mma.begin()) {
    Serial.println("Couldnt start");
    while (1);
  }
  Serial.println("MMA8451 found!");
  
  mma.setRange(MMA8451_RANGE_8_G);

  attachInterrupt(1,Battery_Check,LOW);//Interrupt for when ESP wakes the arduino to check its battery level.
 

}

void loop() {
  // put your main code here, to run repeatedly:

  sensors_event_t event;//Create sensor event variable
  mma.getEvent(&event);//pass event variable into MMA82451 object

  x = sqrt((event.acceleration.x)*(event.acceleration.x));
  y = sqrt((event.acceleration.y)*(event.acceleration.y));
  z = sqrt((event.acceleration.z)*(event.acceleration.z));

  if( x>45 || y>45 || z>45)
  {
    digitalWrite(9,HIGH);
    delay(500);
    digitalWrite(9,LOW);
    State = true;
  }

  /* Display the results (acceleration is measured in m/s^2) 
  Serial.print("X: \t"); Serial.print(x); Serial.print("\t");
  Serial.print("Y: \t"); Serial.print(y); Serial.print("\t");
  Serial.print("Z: \t"); Serial.print(z); Serial.print("\t");
  Serial.println("m/s^2 ");*/
  








  if(x>45 || y>45 || z>45 || Battery)//If Sensor is detected to have been triggered or the battery level needs to be sent to the server
  {

    digitalWrite(wakePin,HIGH);
    delay(100);
    digitalWrite(wakePin,LOW);

    delay(180);//This delay allows the ESP time to wake. If this delay is below 170 milliseconds 
                //the ESP will not recieve the information sent by the arduino and becomes stuck in a loop.

    mySerial.println("H,"+String(bat.read_Bat_level())+","+String(State));

    Serial.println("H,"+String(bat.read_Bat_level())+","+String(State));

    digitalWrite(5,HIGH);

    
    
    Battery = false;
    
    attachInterrupt(1,Battery_Check,LOW);//Interrupt for when ESP wakes the arduino to check its battery level.
 
  
  
  } 

}
void Battery_Check()
{
  Serial.println("interrupt fired");//Indicates that the Interrupt was triggered.
  Battery = true;
  detachInterrupt(1);
  
}
