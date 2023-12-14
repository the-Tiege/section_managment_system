#include <Arduino.h>
#include <esp_now.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include <HTTPClient.h>
#define USE_SERIAL Serial

WiFiMulti wifiMulti;

typedef struct send_struct {
  int sensor = 0;
  int Battery = 0;
  int info=0;
  
} send_struct;//Structure to send seperate pieces of data seperately

uint8_t Sensor1_MAC[] = {0xA4, 0xCF, 0x12, 0x81, 0xE1, 0xA0};//A4:CF:12:81:E1:A0. Mac address of Ammunition tracker

uint8_t Sensor2_MAC[] = {0xA4, 0xCF, 0x12, 0x32, 0xF1, 0x10};//A4:CF:12:32:F1:10.  Mac address of Body armour sensor

const long long unsigned int Micro = 1000000;// Sleep tomer is in micro seconds, This is to convert seconds to micro seconds.
const int Sleep_time = (30*1); //length of time to sleep in seconds. (5*60) is 5 minutes, when the ESP wakes by sleep timer 
                                //it is to check battery level, once every 5 minutes is enough for this.

void OnDataRecv(const uint8_t * mac, const uint8_t *data, int len);//Function called when ESP now data is recieved
void wifiSend();//Function to send data to server
void print_wakeup_reason();//Prints reason why ESP woke up, Used for Debugging.
void OnDataSent(const uint8_t *mac, esp_now_send_status_t status);//Function called when ESP now Data is sent.

///////Variables for timer////////////////////////////////////////////////////
/*
 *Variables used for timer to keep Arduino awake to recieve ESP now messages
 */
unsigned long startTime;
unsigned long currentTime;
unsigned long period = 30000;//"period" sets duration of the timer.
/////////////////////////////////////////////////////////////////////////////
void setup() {

    USE_SERIAL.begin(115200);//Serial used for debugging
    Serial2.begin(9600);//Serial 2 used to send data to the Arduino mega
    print_wakeup_reason();//Prints reason why ESP woke from sleep

    WiFi.mode(WIFI_STA);//Set wifi mode to station

    pinMode(26,OUTPUT);//Output to wake Arduino 
    digitalWrite(26,HIGH);//Logic HIGH means do nothing. Logic LOW wakes Arduino

    pinMode(33,INPUT_PULLUP);//Indicates message from arduino when pulled LOW
    
    esp_sleep_wakeup_cause_t wakeup_reason;//Creates variable of type "esp_sleep_wakeup_cause_t" to store wake up reason.

    wakeup_reason = esp_sleep_get_wakeup_cause();//Gets wake up reason from "esp_sleep_get_wakeup_cause()".

    Serial.println("I'm awake");//Debugging.

    //If the wake up reason was the Sleep timer, the ESP wakes up the arduino by sending a 
    //logic LOW to digital pin 3 of the arduino. This triggers an inturrupt and wakes the arduino.
    if(wakeup_reason == ESP_SLEEP_WAKEUP_TIMER)
    {
      digitalWrite(26,LOW);//Wakes Arduino.

      delay(200);

      digitalWrite(26,HIGH);

      wifiSend();
    }

    
    if(digitalRead(33)==LOW)
    {
      wifiSend();
    }

    Serial.println("Past wifiSend()\n");

    
  if (esp_now_init() != ESP_OK)//Starts listening for ESP-NOW messages.
    {
      Serial.println("Error initializing ESP-NOW");
      return;
    }

    esp_now_peer_info_t Sensor_1;//sensor 1 peer information.
    memcpy(Sensor_1.peer_addr, Sensor1_MAC, 6);
    Sensor_1.channel = 0;  
    Sensor_1.encrypt = false;
  
    // Add Sensor 1 peer        
    if (esp_now_add_peer(&Sensor_1) != ESP_OK){
      Serial.println("Failed to add peer");
      ESP.restart();
    }

    esp_now_peer_info_t Sensor_2;//sensor 1 peer information.
    memcpy(Sensor_2.peer_addr, Sensor2_MAC, 6);
    Sensor_2.channel = 1;  
    Sensor_2.encrypt = false;
  
    // Add Sensor 2 peer        
    if (esp_now_add_peer(&Sensor_2) != ESP_OK){
      Serial.println("Failed to add peer");
      ESP.restart();
    }
     
     esp_now_register_send_cb(OnDataSent);//Set callback on data sent using ESP now
     esp_now_register_recv_cb(OnDataRecv);//When ESP-now message recieved jump to "OnDataRecv()"

     esp_sleep_enable_timer_wakeup(Sleep_time * Micro);//sleep timer in micro seconds

     startTime=millis();//30 second timer starts.
}

void loop() {

  currentTime = millis();

  if((currentTime-startTime) >= period)
  {
    Serial.println((currentTime-startTime));
    Serial.println("Going to sleep now");
    esp_deep_sleep_start();// puts esp into deep sleep
    
  }
  else if(digitalRead(33)==LOW)
  {
    ESP.restart();//in case esp32 wakes before arduino on power up restarts to catch message.
  }

}
void wifiSend()
{

  String http_message = "http://10.0.0.1:5000/input/id:862097";//Address of server and Id of soldier
  String SensorInfo = " ";
  bool recieved = false;

  USE_SERIAL.println("[SETUP] WAIT %..." );

  for(uint8_t t = 4; t > 0; t--) {
        
        USE_SERIAL.flush();
        delay(10);
    }
    
     wifiMulti.addAP("fruit-gums", "fruitgums");//"SSID" and "PASSWORD"

    // wait for WiFi connection
    
    if((wifiMulti.run() == WL_CONNECTED))
    {
        do//Arduino waits untill ESP32 is ready to recieve message when ready ESP 32 sends "X" then arduino sends message.
        {
         Serial2.println("X");
            
         while(Serial2.available()>0)
         {
              
             SensorInfo = Serial2.readStringUntil('F');//Reads String until "F" which is the terminating character in the string
             recieved = true;
               
             Serial2.flush();
                
         }
         }while(recieved == false);
            
         
          Serial.println(http_message + "," + SensorInfo);//Prints recieved information to serial for debugging.

          HTTPClient http;

          USE_SERIAL.print("[HTTP] begin...\n");
          // configure traged server and url
  
          http.begin(http_message + "," + SensorInfo); //HTTP

          // start connection and send HTTP header
          int httpCode = http.GET();

          // httpCode will be negative on error
          if(httpCode > 0) 
          {

            // file found at server
            if(httpCode == HTTP_CODE_OK)
            {
                String payload = http.getString();
                USE_SERIAL.println(payload);
            }
          
          }
          else 
          {
            USE_SERIAL.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());

          http.end();
          }
      
    }
    else
    {
      Serial.println("did not connect.");

          do
          {
            Serial2.println("X");
            
            while(Serial2.available()>0)
            {
              
                SensorInfo = Serial2.readStringUntil('F');
                recieved = true;
               
                Serial2.flush();
                
            }
            }while(recieved == false);
           
      Serial.println(http_message + "," + SensorInfo);

    }
    
    ESP.restart();//After message recieved restarts ESP 32
}


void OnDataRecv(const uint8_t * mac, const uint8_t *data, int len)
{
   
  send_struct* test =(send_struct*) data;//copies recieved data into structure

  esp_err_t result;// variable to check for error sending messages

  bool Sending = true;
  if(test->sensor==1)//If message recieved from sensor 1 ack sensor 1
  {
    Serial.println("sending");
    result = esp_now_send(Sensor1_MAC, (uint8_t *) &Sending, sizeof(Sending));
  }
  else if(test->sensor==2)//If message recieved from sensor 2 ack sensor 2
  {
    result = esp_now_send(Sensor2_MAC, (uint8_t *) &Sending, sizeof(Sending));
  }
  if (result == ESP_OK) {
    Serial.println("Sent with success");
  }
  else {
    Serial.println("Error sending the data");
  }

  digitalWrite(26,LOW);//Wakes Arduino.
  delay(5);//Short time held low identifies that it is sending an ESP now message to arduino to be translated;
  digitalWrite(26,HIGH);

  delay(200);
  
  Serial2.println("H,"+String(test->sensor)+","+String(test->Battery)+","+String(test->info));//information sent using serial 2
  Serial.println("H,"+String(test->sensor)+","+String(test->Battery)+","+String(test->info));
  
  Serial.println("Restarting");
  
 // ESP.restart();
 
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
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) //Sends status for auto ack from reciever.
{
  
    Serial.println(status);
    if (status == 0)
    {
      Serial.println("ESPNOW: ACK_OK");
      ESP.restart();
    }
    else
    {
      Serial.println("ESPNOW: SEND_FAILED");

      //retry = true;
    }
    Serial.println("[SUCCESS]");

}
