#include <ESP8266WiFi.h>
#include <Servo.h>

Servo myservo;
int thres = 800;

void move(int pos, int del)
{
  myservo.write(pos);
  delay(del);
}

void setup() {
  // put your setup code here, to run once:
 Serial.begin(115200);
  myservo.attach(D4);
}

void loop() 
{
   double reading = analogRead(A0);
   Serial.println(reading);
   if( reading < thres)
   {
     move(110,400);
     move(70,400);
   }
}
