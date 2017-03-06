# Robot Orchestra

Robot Orchestra is an Arduino Internet of things (IoT) API for web-controlled music playing, using servos. Multiple servos can collaborate with each other using sensors and each servo's behavior depends on the previous one's robotic state.

  - **Demo**  
  - **Hardware Requirements**  
  - **Design**  
  - **Installation**  
  - **TODO**  
  - **Reference**  
  - **License**  

### Demo
[Demo](https://www.youtube.com/watch?v=IjqijyLrOXg&feature=youtu.be)  

### Hardware Requirements  
To use this API, the following hardware requirements have to be met:
* [ESP8266 micro-controller](https://en.wikipedia.org/wiki/ESP8266) - ESP8266 Micro-controller with Internet shield
* [ESP-12E motor shield](https://smartarduino.gitbooks.io/user-mannual-for-esp-12e-motor-shield/content/interface.html) - Motor shield for ESP8266 to drive the servos
* [Micro servo](https://www.adafruit.com/products/169?gclid=Cj0KEQiA_eXEBRDP8fnIlJDXxsIBEiQAAGfyocOxexE9orkD1clvZEldCO0z9T-eg9v4C2jLbUiJisgaAjMX8P8HAQ)
* Mini USB cable


### Design
#### Overview
For this implementation, we have three standard servos, a limit switch sensor and a photoresistor. First servo is triggered by https web server, and the servo arm close the limit switch sensor to trigger the second servo. The third servo is triggered by the arm of second servo blocking the photoresistor.

<img width="472" alt="screen shot 2017-02-15 at 17 07 40" src="https://cloud.githubusercontent.com/assets/9398437/23008939/dd76982e-f3c7-11e6-9b15-16e51c203714.png">


#### Photoresistor
The resistance of the photoresistor will change according to light intensity. We design a voltage divider circuit to measure the voltage across the photoresistor in order to determine the light intensity around the photoresistor.
<img width="489" alt="screen shot 2017-02-15 at 18 54 37" src="https://cloud.githubusercontent.com/assets/9398437/23008753/b172019c-f3c6-11e6-8869-859cac9b3a71.png">

We use AnalogRead() function to read the voltage across the photoresistor, typical value under indoor lighting is above 800. The reading will decrease to around 700 after blocking the light using a servo arm.
The code for moving servo based on threshold.
```
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
```
#### Limit Switch
We use the limit switch model 10t85. There are three pins in the switch: C, NC(Normally Closed) and NO(Normally Open). When the switch is open, pin C is connected to NO, and when the switch is closed, pin C is connected to NC. The switch is open in default state, so we connect NC to 3.3V, NO to GND, and C to an GPIO pin of the microcontroller. Therefore, when the servo presses down and closes the switch, pin C will have high voltage. We can use either digitalRead() or analogRead() function to read the voltage and process the signal.

![image](https://cloud.githubusercontent.com/assets/18479261/23009283/ebc5d6d6-f3c9-11e6-9b02-d7d4bdff34da.png)

### Installation
#### Bill of Materials
* ESP 8266 MCU * 3
* Standard Servo * 3
* 20k Ohms Photoresistor
* Limit switch sensor
* Breadboard
* micro-USB Cable
* Jumper Wires
* 10k Ohms Resistor

#### Hardware
* Servos can use any digital pins (D1-D9) on the motor sheild.
* We can only use A0 for analogRead() since it's the only analog pin on the motor shield 
* 10k Ohms resistor is used for voltage divider circuit

#### Server
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

#### File Upload
In order to make the API more scalable, we decided to utilize the SPIFFS file system on the ESP8266 board. The board itself has 4MB flash memory, which is beyond sufficient for the purpose of simple web markup files. We referred to the official ESP8266 SPIFFS library to accomplish the files upload.  

First, download the SPIFFS file upload tools from this Github repository [link](https://github.com/esp8266/arduino-esp8266fs-plugin/releases/download/0.2.0/ESP8266FS-0.2.0.zip). Make a “tools” folder under your Arduino master directory. Place the downloaded “ESP8266FS” folder into this newly created “tools” folder.  

Then place the data files you wish to upload into a folder called “data” inside your Arduino sketch folder. In this repository, we already have the "data" folder under current directory.  

To set up the file I/O, include the following code inside the server.ino Arduino code

Beginning the server and check if the upload file exists  
```
bool file_start = SPIFFS.begin();
 if (file_start) {
   Serial.println("beginning SPIFFS file system");
   bool exist = SPIFFS.exists("/index.html");

   if (exist) {
     Serial.println("upload file detected!");
```

Beginning the server and check if the upload file exists
```
bool file_start = SPIFFS.begin();
if (file_start) {
  Serial.println("beginning SPIFFS file system");
  bool exist = SPIFFS.exists("/index.html");
```

If file exists, start opening the file and store data into a single string  
```
if (exist) {
  Serial.println("upload file detected!");

  File f = SPIFFS.open("/index.html", "r");
  if (!f) {
    Serial.println("file upload FAILED");
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
  Serial.println("cannot find upload file");
}
```
After you include the ESP8266FS "tool" folder into to the Arduino tools, you will be able to see the option of "ESP8266 Sketch Data Upload" under the Arduino dropdown menu. Keep the serial monitor closed first and then click on the "ESP8266 Sketch Data Upload". The file uploading process may take a long time, so please be patient. After the uploading process completes, open the serial monitor and start the regular Arduino sketch upload. After you've done all of this, you should be able to see the serial console output of Arduino and ESP8266 WiFi on your computer.

Connect to the WiFi of the username you set up and input the password. Then open any browser on your computer with the IP address displayed in your serial monitor and you will be able to see the key button appearing in your browser window. The default EPS8266 IP address is http://192.168.4.1.


### Future Works
 - 3D printing wrist and hand for the Robot Orchestra.  

### Reference  
 * [ESP8266 motor shield diagram](http://amazingrobots.net/resources/motor_shield_diagram/)  
 * [ESP8266 board pin mappings](http://amazingrobots.net/resources/nodemcu_pinout/)  
 * [ESP8266-12E quick guide](http://ucla.mehtank.com/teaching/2016-17--02--ee183da/esp8266-12e-quick.pdf)  
 * [ESP8266 programming tutorial](http://www.instructables.com/id/Programming-the-ESP8266-12E-using-Arduino-software/)  
 * [ESP8266 SPIFFS file system](https://github.com/esp8266/Arduino/blob/master/doc/filesystem.md)  

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
