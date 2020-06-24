#include "Controller.h"

PPM_Signal Drone;
MyData data;

struct GPS_Data {
  long x = 0;
  long y = 0;
};

GPS_Data GPS;

int LED1 = 4;
//Put LED in Pin 4

RF24 radio(CE_PIN, CSN_PIN);

void resetData() 
{   
  data.throttle = 0;
  data.yaw = 127;
  data.pitch = 127;
  data.roll = 127;
  data.AUX1 = 0;
  data.AUX2 = 0;
}

void TransmitterSetup()
{
  radio.begin();
  //radio.setAutoAck(false);
  radio.setDataRate(RF24_250KBPS);
  radio.enableAckPayload();
  radio.setRetries(2,5); // delay, count
  //radio.openWritingPipe(pipeOut);
  radio.openWritingPipe(slaveAddress);
  resetData();
}

void setup() {

//  pinMode(LED1, OUTPUT);

  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  //pinMode(LED_BUILTIN, OUTPUT);

  TransmitterSetup();
}

//================

/*void updateMessage() {
        // so you can see that new data is being sent
    txNum += 1;
    if (txNum > '9') {
        txNum = '0';
    }
    dataToSend[8] = txNum;
} removed */


//================= 

void showData() {
    if (newData == true) {
        Serial.print("GPS Recieved: Lat: ");
        Serial.print(GPS.x); //Leo
        Serial.print(", Lng: ");
        Serial.println(GPS.y); //Leo
        Serial.println();
        newData = false;
    }
} // added/changed

//================

void send() {

    bool rslt;
    rslt = radio.write(&data, sizeof(MyData));
        // Always use sizeof() as it gives the size as the number of bytes.
        // For example if dataToSend was an int sizeof() would correctly return 2

    Serial.print("Data Sent ");
    //Serial.print(dataToSend);
    if (rslt) {
        if ( radio.isAckPayloadAvailable() ) {
            radio.read(&GPS, sizeof(GPS)); // added/change
            newData = true;
        }
        else {
            Serial.println("  Acknowledge but no data ");
        }
        //updateMessage(); removed
    }
    else {
        Serial.println("  Tx failed");
    }

    prevMillis = millis();
 }

void loop() {

  EEPROM.get(1, data);

  currentMillis = millis();
  if (currentMillis - prevMillis >= txIntervalMillis) {
  send();
  }
  showData();
    
  //radio.write(&data, sizeof(MyData));
  
  if (Serial.available() > 0) {
    // read the oldest byte in the serial buffer:
    incomingByte = Serial.read();
    Serial.println(incomingByte);
    switch(Option) {
      case 0:
        // if it's a capital H (ASCII 72), turn on the LED:
        if (incomingByte == 'H') {
          digitalWrite(LED1, HIGH);
        }
        // if it's an L (ASCII 76) turn off the LED:
        else if (incomingByte == 'L') {
          digitalWrite(LED1, LOW);
        }
        else if (incomingByte == '1') {
          //This is for the throttle option
          Option = 1;
        }
        else if (incomingByte == '2') {
          //This is for the yaw option
          Option = 2;
        }
        else if (incomingByte == '3') {
          //This is for the pitch option
          Option = 3;
        }
        else if (incomingByte == '4') {
          //This is for the roll option
          Option = 4;
        }
        else if (incomingByte == '5') {
          //This is for the AUX1 option
          Option = 5;
        }
        else if (incomingByte == '6') {
          //This is for the AUX2 option
          Option = 6;
        }
        else if (incomingByte == '7') {
          //This is for the Calibration option
          Option = 7;
        }
        else if (incomingByte == '8') {
          //This is for the ESC's
          Option = 8;
        }
        else if (incomingByte == '9') {
          /*This is to read from the EEPROM
            using the serial monitor*/
          EEPROM_Read customVar; //Variable to store custom object read from EEPROM.
          EEPROM.get(1, customVar);

          //Serial.println("Read custom object from EEPROM: ");
          Serial.print("Throttle: ");
          Serial.println(customVar.field1);
          Serial.print("Yaw: ");
          Serial.println(customVar.field2);
          Serial.print("Pitch: ");
          Serial.println(customVar.field3);
          Serial.print("Roll: ");
          Serial.println(customVar.field4);
          Serial.print("AUX1: ");
          Serial.println(customVar.field5);
          Serial.print("AUX2: ");
          Serial.println(customVar.field6);
          Serial.print("Calibration: ");
          Serial.println(customVar.field7);
          Serial.print("ESC's On/Off: ");
          Serial.println(customVar.field8);
  
          Option = 0;          
        }
        break;
      case 1: //Throttle
        Drone.Throttle = incomingByte;
        EEPROM.put(1, Drone);
        Option = 0;
        break;
      case 2: //Yaw
        Drone.Yaw = incomingByte;
        EEPROM.put(1, Drone);
        Option = 0;
        break;
      case 3: //Pitch
        Drone.Pitch = incomingByte;
        EEPROM.put(1, Drone);
        Option = 0;
        break; 
      case 4: //Roll
        Drone.Roll = incomingByte;
        EEPROM.put(1, Drone);
        Option = 0;
        break;
      case 5: //AUX1
        Drone.AUX1 = incomingByte;
        EEPROM.put(1, Drone);
        Option = 0;
        break;
      case 6: //AUX2
        Drone.AUX2 = incomingByte;
        EEPROM.put(1, Drone);
        Option = 0;
        break;
      case 7: //Calibration
        Drone.Cal = incomingByte;
        EEPROM.put(1, Drone);
        Option = 0;
        break;
      case 8: //ESC Turn On
        if (incomingByte == 48) {
          Drone.ESC = 0;
        }
        else if (incomingByte == 49) {
          Drone.ESC = 1;
        }
        else {
          Drone.ESC = incomingByte;
        }
        EEPROM.put(1, Drone);
        Option = 0;
        break;
    }
  }
}
