#include <ESP8266WiFi.h>
#include <Servo.h>

Servo myservo;

void move(int pos, int del)
{
  myservo.write(pos);
  delay(del);
}

void setup() {
  // put your setup code here, to run once:
  myservo.attach(D4);
}

void loop() 
{
   double reading = analogRead(D7);
   if( reading > 0)
   {
     move(120,400);
     move(60,400);
     move(90,200);
   }
}
