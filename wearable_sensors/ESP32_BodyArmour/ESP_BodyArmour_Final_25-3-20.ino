#include <esp_now.h>
#include <WiFi.h>

#define BUTTON_PIN_BITMASK 0x200000000 // 2^33 in hex this defines the pin used to wake the esp from Deep Sleep
const long long unsigned int Micro = 1000000;// Sleep tomer is in micro seconds, This is to convert seconds to micro seconds.
const int Sleep_time = (5*60); //length of time to sleep in seconds. (5*60) is 5 minutes, when the ESP wakes by sleep timer it is to check battery level, once every 5 minutes is enough for this.


uint8_t Macaddress[] = {0xA4, 0xCF, 0x12, 0x32, 0xF0, 0x84};//A4:CF:12:32:F0:84 reciever mac address, Used as address to send ESP-Now message.


bool retry=false;//bool value to use in auto callback to resend message if fails



typedef struct send_struct {
  int sensor = 2;//identifies Which sensor it is. 1 means rifle sensor 2 means body armour sensor
  int Battery = 0;//Sends battery level of sensor
  int info=0;//Sends sensor payload. Rounds fired for rifle. Impact for body armour.
  
} send_struct;//Structure to send sensor data

void print_wakeup_reason();//Prints reason why ESP woke up, Used for Debugging.
void espNowSend(send_struct test);//ESPNOW function prototype
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status);//Auto ack function prototype
void OnDataRecv(const uint8_t * mac, const uint8_t *data, int len);

///////Variables for timer////////////////////////////////////////////////////
/*
 *If the esp-now message fails to send the timer is used to resend the message after a specified ammount of time.
 *A timer is used rather than a delay so that if the Arduino sends more information that it will be recieved by the esp.
 */
unsigned long startTime;
unsigned long currentTime;
unsigned long period = 0;//"period" sets duration of the timer, it is set to 0 here so that the first time the ESP sends a message there is no timer. this is updated to 5 seconds if the message fails to send.
/////////////////////////////////////////////////////////////////////////////

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial2.begin(9600);//Same baud rate as arduino for communication.

  WiFi.mode(WIFI_STA);//wife mode station

  pinMode(33,INPUT_PULLDOWN);



  print_wakeup_reason();//Prints reason why ESP woke from sleep

  //////////////////////////////////////////////////////////////////////////////
  esp_sleep_wakeup_cause_t wakeup_reason;//Creates variable of type "esp_sleep_wakeup_cause_t" to store wake up reason.

  wakeup_reason = esp_sleep_get_wakeup_cause();//Gets wake up reason from "esp_sleep_get_wakeup_cause()".

  Serial.println("I'm awake");//Debugging.

  if(wakeup_reason != ESP_SLEEP_WAKEUP_EXT0)//If the wake up reason was the Sleep timer, the ESP wakes up the arduino by sending a logic LOW to digital pin 3 of the arduino. This triggers an inturrupt and wakes the arduino.
  {
    Serial.println("Woke by timer");
    pinMode(26,OUTPUT);

    digitalWrite(26,LOW);
    delay(10);
    digitalWrite(26,HIGH);
  }

  /////////Set up for serial comms////////////////////////////////////////////////////////////////////

  send_struct test;//Structure declaration

  Serial.println("waiting");//Debugging
  
  while(Serial2.available()==0)//Waits for arduino to send information via the serial.
   {
      
   }

   if(Serial2.read()== 'H')//When it reads the string starting with "H" it stores the information in the structure to be sent.
    {
    
      test.Battery=Serial2.parseInt();
      test.info=Serial2.parseInt();
      

      Serial2.flush();
    }

  

    Serial.println("BATT :" + String(test.Battery) + " State : " + String(test.info));//Prints information for debugging.
  
  ////////Init ESP_NOW///////////////////////////////////////////////////////////////////

  //For some reason this section of the code breakes if it is put in a function outside of setup and called in setup.
  
  if (esp_now_init() != ESP_OK) //if esp_now is not initalised correctly resets loop
   {
      Serial.println("Error initializing ESP-NOW");
      return;
    }

  // register peer
  esp_now_peer_info_t peerInfo;//structure of type peer info declared to sotre peer information.

  memcpy(peerInfo.peer_addr, Macaddress, 6);//copies the mac address stored on array Macaddress to the location of peerInfo.peer_addr
  peerInfo.channel = 0; //sets channel 0
  peerInfo.encrypt = false;//no encryption
          
  if (esp_now_add_peer(&peerInfo) != ESP_OK)//if peer is not registered resets loop.
  {
    Serial.println("Failed to add peer");
    return;
  }

 ///////////////////////////////////////////////////////////////////////////////////////////// 

esp_now_register_send_cb(OnDataSent);//sets up auto callback to carry out function OnDataSent when message is sent.
esp_now_register_recv_cb(OnDataRecv);

  

  
  while(!retry)//if auto ack is not recieved send message again
  {

    if(Serial2.read()== 'H')//If new information is sent from the Sensor while trying to send a message. The information is updated.
    {
    
      test.Battery = Serial2.parseInt();
      test.info = Serial2.parseInt();
      

      Serial2.flush();

      Serial.println("BATT :" + String(test.Battery) + " State : " +String(test.info));
      
      
    }

    currentTime = millis();
    if((currentTime-startTime) >= period)//Timer so that in the event of a message not being recieved the ESP will only retry every 5 seconds.
    {
      
      espNowSend(test);//function to send message.
      
      startTime=currentTime;
      period = 5000;
      
    }
      
      
  }

////////////////Set sleep mode////////////////////////////////////////////////////////////////////////////////////////////////////

  
  esp_sleep_enable_timer_wakeup(Sleep_time * Micro);//leep timer in micro seconds
  esp_sleep_enable_ext0_wakeup(GPIO_NUM_33,1); //1 = High, 0 = Low, enables external wake up from deep sleep when logic high is applied to pin 33

  

  Serial.println("Going to sleep now");
  esp_deep_sleep_start();// puts esp into deep sleep
}

void loop() {
  // put your main code here, to run repeatedly:


}
void print_wakeup_reason()//Prints reason why esp woke up for debugging
{
  esp_sleep_wakeup_cause_t wakeup_reason;

  wakeup_reason = esp_sleep_get_wakeup_cause();

  switch(wakeup_reason)
  {
    case ESP_SLEEP_WAKEUP_EXT0 : Serial.println("Wakeup caused by external signal using RTC_IO"); 
                                 break;
    
    case ESP_SLEEP_WAKEUP_TIMER : Serial.println("Wakeup caused by timer");
                                  break;
    default : Serial.printf("Wakeup was not caused by deep sleep: %d\n",wakeup_reason); 
              break;
  }
}
void espNowSend(send_struct test)//Sends esp now message with error message if fails to send
{
   esp_err_t result = esp_now_send(Macaddress, (uint8_t *) &test, sizeof(send_struct));// sends structure returns resultn 1 if send success
   
  if (result == ESP_OK)
  {
    Serial.println("Sent with success");
  }
  else 
  {
    Serial.println("Error sending the data");
  }

  
}
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) //Sends status for auto ack from reciever.
{
  
    Serial.println(status);
    if (status == 0)
    {
      Serial.println("ESPNOW: ACK_OK");
      //retry = false;
    }
    else
    {
      Serial.println("ESPNOW: SEND_FAILED");

      //retry = true;
    }
    Serial.println("[SUCCESS]");


}
void OnDataRecv(const uint8_t * mac, const uint8_t *data, int len) {
  //memcpy(&incomingReadings, incomingData, sizeof(incomingReadings));
  
  Serial.print("Received: ");
  //Serial.println(len);
  Serial.println(*data);
  retry = (bool*)*data;

  
   
}
