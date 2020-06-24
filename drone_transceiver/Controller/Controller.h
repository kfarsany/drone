#include <Arduino.h>
#include <EEPROM.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>

#define CE_PIN   9
#define CSN_PIN 10


struct PPM_Signal {
  byte Throttle = 0;
  byte Yaw = 127;
  byte Pitch = 127;
  byte Roll = 127;
  byte AUX1 = 0;
  byte AUX2 = 0;
  byte Cal = 0;
  byte ESC = 0;
};

struct EEPROM_Read {
  byte field1;
  byte field2;
  byte field3;
  byte field4;
  byte field5;
  byte field6;
  byte field7;
  byte field8;
};

const byte slaveAddress[5] = {'R','x','A','A','A'};

struct MyData {
  byte throttle;
  byte yaw;
  byte pitch;
  byte roll;
  byte AUX1;
  byte AUX2;
  byte cal;
  byte esc;
};

struct GPSData 
{
  double lat;
  double lng;
}; // added

const int ledPin = 13; // the pin that the LED is attached to
int incomingByte;      // a variable to read incoming serial data into
int Option = 0;

//char dataToSend[10] = "Message 0";
//char txNum = '0';
//int ackData[2] = {-1, -1}; // to hold the two values coming from the slave
bool newData = false;

unsigned long currentMillis;
unsigned long prevMillis;
unsigned long txIntervalMillis = 1000; // send once per second
