#include <ESP8266WiFi.h>
#include <Servo.h>

WiFiServer server(80); //Initialize the server on Port 80
Servo myservo;  // create servo object to control a servo 

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
      myservo.write(110); 
      delay(500);
      myservo.write(0);
    }

    // Prepare the HTML document to respond and add buttons:
    String s = "HTTP/1.1 200 OK\r\n";
    s += "Content-Type: text/html\r\n\r\n";
    s += "<!DOCTYPE HTML>\r\n<html>\r\n";
    s += "<button style=\"width: 100px; height: 500px; background: #fff; border: 3px solid #000; border-radius: 3px;\"><input value=\"Re\" type=\"button\" onclick=\"location.href='/ON'\"></button>";
    s += "</html>\n";
    
    //Serve the HTML document to the browser.
    client.flush(); //clear previous info in the stream 
    client.print(s); // Send the response to the client 
    delay(1); 
    Serial.println("Client disonnected"); //Looking under the hood
}
