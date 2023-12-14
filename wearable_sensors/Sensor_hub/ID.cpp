#include "Arduino.h"
#include "ID.h"

#include <SPI.h>              //include libraries
#include <MFRC522.h>


#define SS_PIN 53            //define pins
#define RST_PIN 49

 
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class

MFRC522::MIFARE_Key key; 

ID::ID()
{
  
}
void ID::Setup_rfid()
{
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522 

}
bool ID::ID_check()
{
  String inputNum = "";
  bool ID = false;

  Serial.println("Checking ID");

  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! rfid.PICC_IsNewCardPresent())
    return;

  // Verify if the NUID has been read
  if ( ! rfid.PICC_ReadCardSerial())
    return;

    // Store NUID into nuidPICC array
    for (byte i = 0; i < 4; i++)
    {
      nuidPICC[i] = rfid.uid.uidByte[i];//uid number read from card in bytes
      inputNum = inputNum + String(nuidPICC[i]);//uid number changed to a string for ease of verification.
      
    }
    
    Serial.println(inputNum);

    if(inputNum == access)
    {
      ID = true;
      rfid.PCD_SoftPowerDown();
    }
    else
    {
      ID = false;
    }

    return ID;
  
}
