#include <avr/sleep.h>
#include <SoftwareSerial.h>
#include "Bat_level.h" //Includes Battery reading object.

const int rxPin = 10, txPin = 11;//Defines pins used for software serial.

SoftwareSerial mySerial(rxPin,txPin);//creates software serial object.
Bat_level bat(A4);//Creates battery reading object


const int Xpin = A5, Ypin = A6, Zpin = A7, n = 500, triggerPin = 2,  ESP_wakes_arduino= 3, wake_ESP = 7;//Defines pins used.
int Xcount=0;//Counts rounds fired

////////////Timer Variables/////////////////////////////////
/*
 * Timer for keeping arduino awake once trigger is pulled. As long as trigger is pulled the arduino will remain awake. 
 * Once the trigger is released the arduino stays awake for 3 seconds, then sends its information to the esp and goes to sleep.
 */
unsigned long startTime;
unsigned long currentTime;
unsigned long period = 3000;
///////////////////////////////////////////////////////////
/*
 * Function Prototypes
 */
int MAX(int,int);
int MIN(int,int);

void Going_To_Sleep();
void wakeup();



void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);//Serial for debugging
  mySerial.begin(9600);//Software serial used to communicate with ESP
  
  //External reference for analogue read 3.3v. Used for both Accelerometer and battery reading.
  analogReference(EXTERNAL);

  //Inturrupt pin for trigger pull
  pinMode(triggerPin,INPUT_PULLUP);

  //Inturrupt pin for when ESP wakes arduino to check its battery level.
  pinMode(ESP_wakes_arduino,INPUT_PULLUP);
  
  pinMode(LED_BUILTIN,OUTPUT);//Built in LED used to indicate when arduino is awake for debugging.
  digitalWrite(LED_BUILTIN,HIGH);//When builtin led is turned on the arduino is awake.

  pinMode(12,OUTPUT);//Used to light led when a round is fired for debugging purpose.
  digitalWrite(12,LOW);
 
  pinMode(wake_ESP,OUTPUT);//Sets up pin that is used to wake the ESP when a message is to be sent.
  digitalWrite(wake_ESP,LOW);//Ensures wake pin is LOW until ESP is needed.

  startTime = millis();//Sets start time for timer.

  

}

void loop() {
  /*
   * Variables used to read values from Accelerometer
   * x,y,z : Used to read analogue value from Accelerometer.
   * minx, miny, minz : gets the minimum value read from the accelerometer.
   * maxx, maxy, maxz : gets the maximum value read from the accelerometer.
   * Diffx, Diffy, Diffz : gets the difference between the max and min points, 
   * in this way the absolute value of which axis moved the most can be determined,
   * exessive movement on the y and z axis can be ignored and only when the movement is mainly
   * on the x axis will a round be counted.
   */
  int x=0,y=0,z=0,minx=0,miny=0,minz=0,maxx=0,maxy=0,maxz=0,Diffx=0,Diffy=0,Diffz=0;

  currentTime = millis();

  if(digitalRead(triggerPin)==LOW)
  {

  //////////////////////////////////////////////////////////////
  /*
   * Initial reading to use as base line for min-max value functions.
   */
  x=analogRead(Xpin);
  x=map(x,0,1023,-300,+300);
  minx=x;
  maxx=x;
  //delay(1);
  
  y=analogRead(Ypin);
  y=map(y,0,1023,-300,+300);
  miny=y;
  maxy=y;
  //delay(1);
  
  z=analogRead(Zpin);
  z=map(z,0,1023,-300,+300);
  minz=z;
  maxz=z;
  //delay(1);
 /////////////////////////////////////////////////////////////
 /* 
  *  for loop takes 500 over the course of 500 ms and gets the min and max values on each axis.
  */
for(int i=0; i<n;i++)
{
  x=analogRead(Xpin);
  x=map(x,0,1023,-300,+300);
  maxx=MAX(x,maxx);
  minx=MIN(x,minx);
  //delay(1);
  
  y=analogRead(Ypin);
  y=map(y,0,1023,-300,+300);
  maxy=MAX(y,maxy);
  miny=MIN(y,miny);
  //delay(1);
  
  z=analogRead(Zpin);
  z=map(z,0,1023,-300,+300);
  maxz=MAX(z,maxz);
  minz=MIN(z,minz);
  delay(1);
  
}
//////////////////////////////////////////////////////////
/*
 * The differenc between the max and min reading on each axis is obtained to see on which axis there was the most movement.
 */
Diffx=maxx-minx;
Diffy=maxy-miny;
Diffz=maxz-minz;
/////////////////////////////////////////////////////////
//Prints values to serial monitor which can be viewed on Serial plotter for debugging.
/*Serial.print("DiffX :\t ");Serial.print(Diffx);Serial.print("\t");
Serial.print("DiffY :\t ");Serial.print(Diffy);Serial.print("\t");
Serial.print("DiffZ :\t ");Serial.print(Diffz);Serial.print("\t");
Serial.println();*/
 }


if((Diffx>20)&&(Diffy<50)&&(Diffz<50) && (digitalRead(triggerPin)==LOW))
{
  /*
   * if the trigger is pulled detects and the movement on the x axis is above a certain treshold
   * and if movement on the y and z axis is below a certain treshold then a round has been fired.
   */
  Xcount++;
  Serial.print("X :");
  Serial.println(Xcount);
  digitalWrite(12,HIGH);//lights led to indicate round has been fired.
  delay(50);
  digitalWrite(12,LOW);
}



if(digitalRead(triggerPin)==LOW)//If the trigger remains pulled resets start time to keep arduino awake. only when trigger is released will arduino sleep.
  {
    startTime=currentTime;
  }


  if((currentTime-startTime) >= period)
  {
    /*
     * Once the trigger has been released the timer ends after 3 seconds and the Arduino sends information to ESP then goes to sleep.
     */

    digitalWrite(wake_ESP,HIGH);//Sends a logic HIGH to the esp to wake it.
    delay(100);
    digitalWrite(wake_ESP,LOW);
    
    delay(180);//This delay allows the ESP time to wake. If this delay is below 170 milliseconds 
                //the ESP will not recieve the information sent by the arduino and becomes stuck in a loop.
    
    mySerial.println("H,"+String(bat.read_Bat_level())+","+String(Xcount));//Sends information to ESP over Serial monitor.

    Serial.println("H,"+String(bat.read_Bat_level())+","+String(Xcount));//Echos information sent to the ESP for debugging.

    

    
    Going_To_Sleep();//Arduino sleep function.
    startTime=currentTime;//When Arduino wakes up resets the timer.
    Xcount = 0;//Resets rounds counted to 0.

    
  
  }





  

  

}
int MAX(int Reading,int MAX)//Function to compare two values and return the larger value.
{

  
    if(Reading>MAX)
    {
      MAX=Reading;
    }
    else
    {
      MAX=MAX;
    }
    

  return MAX;
}
int MIN(int Reading, int MIN)//Function to compare two values and return the lower value.
{

    if(Reading>MIN)
    {
      MIN=MIN;
    }
    else
    {
      MIN=Reading;
    }

  

  return MIN;
}
void Going_To_Sleep()//Sets up arduino to go to sleep.
{
  sleep_enable();//enables sleep mode.
  attachInterrupt(0,wakeup,LOW);//Interrupt for when trigger is pulled
  attachInterrupt(1,wakeup,LOW);//Interrupt for when ESP wakes the arduino to check its battery level.
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
  detachInterrupt(1);//Disables interrupt
}
