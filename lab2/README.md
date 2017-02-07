# Robot Pianista

Robot Pianista is an Arduino Internet of things (IoT) API for web-controlled piano playing, using servos.  

  - **Demo**  
  - **Hardware Requirements**  
  - **Design**  
  - **Implementation**  
  - **TODO**  
  - **Reference**  
  - **License**  

### Demo
[Demo](https://vimeo.com/202894019)  

### Hardware Requirements  
To use this API, the following hardware requirements have to be met:
* [ESP8266 micro-controller](https://en.wikipedia.org/wiki/ESP8266) - ESP8266 Micro-controller with Internet shield
* [ESP-12E motor shield](https://smartarduino.gitbooks.io/user-mannual-for-esp-12e-motor-shield/content/interface.html) - Motor shield for ESP8266 to drive the servos
* [Micro servo](https://www.adafruit.com/products/169?gclid=Cj0KEQiA_eXEBRDP8fnIlJDXxsIBEiQAAGfyocOxexE9orkD1clvZEldCO0z9T-eg9v4C2jLbUiJisgaAjMX8P8HAQ)
* Mini USB cable

### Design  
This IoT API was designed as a preliminary step to construct a web-controlled orchestra with Arduino and servos. The ESP8266 micro-controller was used as a server for users to interact with the servos wirelessly through WiFi and their local browsers.

### Implementation
Include the ESP8266 WiFi library and Arduino Servo library
```
#include <ESP8266WiFi.h>
#include <Servo.h>
```

Setup the web server confidentials and start the server.
```
WiFi.mode(WIFI_AP); //Our ESP8266-12E is an AccessPoint
WiFi.softAP("kfan_esp", "110"); // Provide the (SSID, password); .
server.begin(); // Start the HTTP Server

//Looking under the hood
Serial.begin(115200); //Start communication between the ESP8266-12E and the monitor window
IPAddress HTTPS_ServerIP= WiFi.softAPIP(); // Obtain the IP of the Server
Serial.print("Server IP is: "); // Print the IP to the monitor window
Serial.println(HTTPS_ServerIP);
```

Initialize the servo and calibrate to 0
```
myservo.attach(D2);  // attaches the servo on pin 2 to the servo object
myservo.write(0);
```

Checking connections.
```
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
```

Handle HTTP requests and spin the servo when user press the piano key down in the web interface.
```
if (request.indexOf("/ON") != -1){
  myservo.write(110);
  delay(500);
  myservo.write(0);
}
```

Inject html code and inline style onto the web interface.
```
String s = "HTTP/1.1 200 OK\r\n";
s += "Content-Type: text/html\r\n\r\n";
s += "<!DOCTYPE HTML>\r\n<html>\r\n";
s += "<button style=\"width: 100px; height: 500px; background: #fff; border: 3px solid #000; border-radius: 3px;\"><input value=\"Re\" type=\"button\" onclick=\"location.href='/ON'\"></button>";
s += "</html>\n";
```

Handle HTTP requests and spin the servo when user press the piano key down in the web interface.
```
if (request.indexOf("/ON") != -1){
  myservo.write(110);
  delay(500);
  myservo.write(0);
}
```

Flush the stream and reset the client info
```
client.flush(); //clear previous info in the stream
client.print(s); // Send the response to the client
delay(1);
Serial.println("Client disonnected"); //Looking under the hood
```

### TODO
 - Implement Arduino SD library to read html, css and javascript files into the board.  
 - 3D printing wrist and hand for the Robot Pianista.  
 - Multiple servos to simulate human hand.    

### Reference  
 * [Online virtual piano](http://piano-player.info)  
 * [ESP8266 motor shield diagram](http://amazingrobots.net/resources/motor_shield_diagram/)  
 * [ESP8266 board pin mappings](http://amazingrobots.net/resources/nodemcu_pinout/)  
 * [ESP8266-12E quick guide](http://ucla.mehtank.com/teaching/2016-17--02--ee183da/esp8266-12e-quick.pdf)  
 * [ESP8266 programming tutorial](http://www.instructables.com/id/Programming-the-ESP8266-12E-using-Arduino-software/)  

### License  
**MIT**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [@thomasfuchs]: <http://twitter.com/thomasfuchs>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [keymaster.js]: <https://github.com/madrobby/keymaster>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]:  <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
