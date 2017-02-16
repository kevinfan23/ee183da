#include <ESP8266WiFi.h>
#include <Servo.h>

WiFiServer server(80); //Initialize the server on Port 80
Servo myservo;

void move(int pos, int del)
{
  myservo.write(pos);
  delay(del);
}

void setup() {
  // put your setup code here, to run once:
  WiFi.mode(WIFI_AP); //Our ESP8266-12E is an AccessPoint 
  WiFi.softAP("Brick_Break", "12345678"); // Provide the (SSID, password); . 
  server.begin(); // Start the HTTP Server

  Serial.begin(115200); //Start communication between the ESP8266-12E and the monitor window
  IPAddress HTTPS_ServerIP= WiFi.softAPIP(); // Obtain the IP of the Server 
  Serial.print("Server IP is: "); // Print the IP to the monitor window 
  Serial.println(HTTPS_ServerIP);

  myservo.attach(D4);
}

void loop() 
{
   WiFiClient client = server.available();
   if (!client) 
   { 
     return; 
   } 
   Serial.println("Somebody has connected :)");  
   String request = client.readStringUntil('\r');
   Serial.println(request); 

   if (request.indexOf("/ONE") != -1)
   {
      move(110,400);
      move(70,400);
   }

   
  // Prepare the HTML document to respond and add buttons:
  String s = "HTTP/1.1 200 OK\r\n";
  s += "Content-Type: text/html\r\n\r\n";
  s += "<!DOCTYPE HTML>\r\n<html>\r\n";
  s += "<br><input type=\"button\" name=\"b1\" value=\"Solo\"";
  s += " onclick=\"location.href='/ONE'\">";
  s += "<br><br><br>";
  s += "<br><input type=\"button\" name=\"b1\" value=\"Harmony\"";
  s += " onclick=\"location.href='/TWO'\">";
  s += "</html>\n";
  
  //Serve the HTML document to the browser.
  client.flush(); //clear previous info in the stream
  client.print(s); // Send the response to the client
  delay(1);
  Serial.println("Client disonnected"); //Looking under the hood   
}
