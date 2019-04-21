/*
 * Arduino Microwave Radar Motion Sensor Interface
 * https://Circuits4you.com
 * Oct 2018
 */

#include <ESP8266WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"


/************************* WiFi Access Point *********************************/

#define WLAN_SSID       "vivo 1718"
#define WLAN_PASS       "satusamhu"

/************************* Information to Connect to Adafruit IO *********************************/
/*  You will need and account - Its FREE  */

#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883                   // use 8883 for SSL
#define AIO_USERNAME    "kaushalya"
#define AIO_KEY         "0707ccd5345744edb15999c21cb5db27"

/************ Setting up your WiFi Client and MQTT Client ******************/

// Create an ESP8266 WiFiClient class to connect to the MQTT server.

WiFiClient client;

// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);

/****************************** Set Up a Feed to Publish To ***************************************/

// Setup a feed called 'photocell' for publishing.
// Notice MQTT paths for AIO follow the form: <username>/feeds/<feedname>

Adafruit_MQTT_Publish isMotionDetected = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/motiondetector");

/********************* Values ******************************/
// Need a changing value to send.  We will increment this value
// in the getVal function.  
//we start at zero and when it gets to 10 we start over.



/*************************** Sketch Code ***********************************************************/

// Bug workaround for Arduino 1.6.6, it seems to need a function declaration
// for some reason (only affects ESP8266, likely an arduino-builder bug).
void MQTT_connect();





int Sensor = D5;   //Input Pin
int LED = D6;     // Led pin for Indication

int flg = 0;  //Change detection flag
void setup() {
  Serial.begin(9600);
  Serial.println("Waiting for motion");
  pinMode (Sensor, INPUT);  //Define Pin as input
  pinMode (LED, OUTPUT);    //Led as OUTPUT


    Serial.println(F("Adafruit MQTT demo"));

  // Connect to WiFi access point.
  Serial.println(); Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WLAN_SSID);

  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.println("WiFi connected");
  Serial.println("IP address: "); Serial.println(WiFi.localIP());

  
}

void loop() {

  MQTT_connect();
     int val = digitalRead(Sensor); //Read Pin as input
     Serial.println(val);
     if((val > 0) && (flg==0))
     {
        digitalWrite(LED, HIGH);
        Serial.println("Motion Detected");
        flg = 1;

        isMotionDetected.publish(flg);
     }

     if(val == 0)
     {
        digitalWrite(LED, LOW);
         Serial.println("Motion not Detected");
        flg = 0;
     }  
     delay(4000);
}


void MQTT_connect() {
  int8_t ret;

  // Stop if already connected.
  if (mqtt.connected()) {
    return;
  }

  Serial.print("Connecting to MQTT... ");

  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) { // connect will return 0 for connected
       Serial.println(mqtt.connectErrorString(ret));
       Serial.println("Retrying MQTT connection in 5 seconds...");
       mqtt.disconnect();
       delay(5000);  // wait 5 seconds
       retries--;
       if (retries == 0) {
         // basically die and wait for WDT to reset me
         while (1);
       }
  }
  Serial.println("MQTT Connected!");
}
