#include <ESP8266WiFi.h>
#include <Servo.h>
#include "FS.h"

WiFiServer server(80); //Initialize the server on Port 80
Servo myservo;  // create servo object to control a servo 
String data;

void setup() {
    WiFi.mode(WIFI_AP); //Our ESP8266-12E is an AccessPoint 
    WiFi.softAP("kfan_esp", "110"); // Provide the (SSID, password); . 
    server.begin(); // Start the HTTP Server

    //Looking under the hood
    Serial.begin(115200); //Start communication between the ESP8266-12E and the monitor window
    IPAddress HTTPS_ServerIP= WiFi.softAPIP(); // Obtain the IP of the Server 
    Serial.print("Server IP is: "); // Print the IP to the monitor window 
    Serial.println(HTTPS_ServerIP);
    
    myservo.attach(D2);  // attaches the servo on pin 9 to the servo object 
    myservo.write(0);

    bool ok = SPIFFS.begin();
    if (ok) {
      Serial.println("ok");
      bool exist = SPIFFS.exists("/index.html");
  
      if (exist) {
        Serial.println("The file exists!");
  
        File f = SPIFFS.open("/index.html", "r");
        if (!f) {
          Serial.println("Some thing went wrong trying to open the file...");
        }
        else {
          int s = f.size();
          Serial.printf("Size=%d\r\n", s);
  
  
      // USE THIS DATA VARIABLE
  
          data = f.readString();
          Serial.println(data);
  
          f.close();
        }
      }
      else {
        Serial.println("No such file found.");
      }
    }

}

void loop() { 
    WiFiClient client = server.available();
    if (!client) { 
      return; 
    } 
    //Looking under the hood 
    Serial.println("Somebody has connected :)");

    //Read what the browser has sent into a String class and print the request to the monitor
    String request = client.readStringUntil('\r');
    //Looking under the hood 
    Serial.println(request);
    
    // Handle the Request
    if (request.indexOf("/ON") != -1){ 
      myservo.write(0);
      delay(500);
      myservo.write(45);
    }
    
    //Serve the HTML document to the browser.
    client.flush(); //clear previous info in the stream 
    client.print(data); // Send the response to the client 
    delay(1); 
    Serial.println("Client disonnected"); //Looking under the hood
}

