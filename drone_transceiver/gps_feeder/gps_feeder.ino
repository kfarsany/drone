#include <TinyGPS++.h>
#include <SoftwareSerial.h>
/*
   This sample sketch demonstrates the normal use of a TinyGPS++ (TinyGPSPlus) object.
   It requires the use of SoftwareSerial, and assumes that you have a
   4800-baud serial GPS device hooked up on pins 4(rx) and 3(tx).
*/

static const int RXPin = 5, TXPin = 6;

static const uint32_t GPSBaud = 9600;

float coord[2];

// The TinyGPS++ object
TinyGPSPlus gps;

// The serial connection to the GPS device
SoftwareSerial ss(RXPin, TXPin);

void setup()
{
  Serial.begin(115200);
  ss.begin(GPSBaud);
  delay(2000);

  Serial.println("Ready");
}

void loop(){
  while (ss.available() > 0){
    if (gps.encode(ss.read())){
      feedInfo();
      Serial.println(String(coord[0],6)+", "+String(coord[1],6)+",");
      delay(1100);
    }
  }
  if (millis() > 5000 && gps.charsProcessed() < 10){
    Serial.println(F("No GPS detected: check wiring."));
    while(true);
  }
}

void feedInfo()
{
  if (gps.location.isValid())
  {
    coord[0] = gps.location.lat();
    coord[1] = gps.location.lng();
  }
  else
  {
    coord[0] = -999;
    coord[1] = -999;
  }
}
