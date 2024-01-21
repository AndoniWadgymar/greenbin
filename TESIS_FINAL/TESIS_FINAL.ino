// FINAL ARDUINO IDE CODE FOR TESIS

// Libraries used to connect to Wifi and get HTTP RESPONSE 
#include <WiFi.h>
#include <HTTPClient.h>
// Librarie to get JSON answer
#include <Arduino_JSON.h>
// LCI2C
#include <LiquidCrystal_I2C.h>  //https://github.com/fdebrabander/Arduino-LiquidCrystal-I2C-library
// Timer library
#include "Countimer.h" //https://github.com/inflop/Countimer
#include <EEPROM.h>
// Tempeture and Humidity Sensors
#include <DHT.h>
#include <DHT_U.h>
// EEPROM SIZE
#define EEPROM_SIZE 12  
// DIMER LIBRARY
#include <RBDdimmer.h>//
#include <dimmable_light.h>

//Define LiquidCrystal  
LiquidCrystal_I2C lcd(0x27, 16, 2);  // LCD HEX address 0x3F -- change according to yours
// Define timer
Countimer tdown;

// const char* ssid = "INFINITUMF9D1";
// const char* password = "QvS5Z22NSi";
const char* ssid = "Domain Expansion";
const char* password = "SaturoGojo97!";

//Your Domain name with URL path or IP address with path
const char* serverName = "http://54.89.24.238/trash/process/active/json";

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastTime = 0;
unsigned long timerDelay = 5000;

String sensorReadings;

// Values from JSON response
int JSONID;
int JSONTime;
const char* JSONSize;


// LED SETUP
uint8_t LEDred = 23;
// NO SE PUEDE EL PUERTO 1 
// uint8_t LEDyellow = 1;
uint8_t LEDyellow = 16;
uint8_t LEDgreen = 3;
      
//Sensores Humedad
int SENSOR1 = 13;
// int SENSOR2 = 14;   

int TEMPERATURA1;
int HUMEDAD1;
// int TEMPERATURA2;
// int HUMEDAD2;

DHT dht1(SENSOR1, DHT22);  
// DHT dht2(SENSOR2, DHT22);

// Buttons set up
#define bt_set 19
#define bt_up 18
#define bt_down 5
#define bt_start 17

// Timer Setup   
int time_s = 0;
int time_m = 0;
int time_h = 0;

// Flags Setup
int set = 0;
int flag1=0, flag2=0, flag3=0;

int buzzer = 4;

// DIMMER SETUP MOTOR
// #define outputPin  33 
// #define zerocross 36
// dimmerLamp dimmer_motor(outputPin, zerocross); //initialase port for dimmer for ESP8266, ESP32, Arduino due boards
// int motorVal = 20;

// // DIMMER SETUP LIGHT
// #define outputPin  32 
// #define zerocross 39
// dimmerLamp dimmer(outputPin, zerocross); //initialase port for dimmer for ESP8266, ESP32, Arduino due boards
// int lightVal = 20;

// DIMMER SETUP LIGHT & MOTOR 
const int syncPin = 27;
#define outputPinL  33
#define outputPinM  32

DimmableLight lightL(outputPinL);
DimmableLight lightM(outputPinM);

// MOTOR TURN TIME
int turntimemin = 1;
int firstStop;
int hourStop;
int secondsjson;

// // MOTOR
// // Motor A
// int motor1Pin1 = 26; 
// int motor1Pin2 = 27; 
// int enable1Pin = 14; 

// // Setting PWM properties
// const int freq = 30000;
// const int pwmChannel = 0;
// const int resolution = 8;
// int dutyCycle = 200;

// TIMER SETUP

void setup() {

  Serial.begin(115200);

  // Buttons set up
  pinMode(bt_set, INPUT_PULLUP);
  pinMode(bt_up, INPUT_PULLUP);
  pinMode(bt_down, INPUT_PULLUP);
  pinMode(bt_start, INPUT_PULLUP);

  // LEDS setup
  pinMode(LEDred, OUTPUT);
  pinMode(LEDyellow, OUTPUT);
  pinMode(LEDgreen, OUTPUT);

  // Buzzer set up
  pinMode(buzzer, OUTPUT);

  // Start DHT
  dht1.begin();
  // dht2.begin();  

  // START DIMMER MOTOR
  // dimmer_motor.begin(NORMAL_MODE, ON); //dimmer initialisation: name.begin(MODE, STATE) 
  // dimmer_motor.setPower(motorVal); // setPower(0-100%);

  //   // START DIMMER
  // dimmer.begin(NORMAL_MODE, ON); //dimmer initialisation: name.begin(MODE, STATE) 
  // dimmer.setPower(lightVal); // setPower(0-100%);

  DimmableLight::setSyncPin(syncPin);
  DimmableLight::begin();

  //Init EEPROM
  EEPROM.begin(EEPROM_SIZE);

  // Motor TIMERS
  int turntimesec = 60 * turntimemin;

  //PINS MOTOR:
  // pinMode(motor1Pin1, OUTPUT);
  // pinMode(motor1Pin2, OUTPUT);
  // pinMode(enable1Pin, OUTPUT);
  
  // // configure LED PWM functionalitites
  // ledcSetup(pwmChannel, freq, resolution);
  
  // // attach the channel to the GPIO to be controlled
  // ledcAttachPin(enable1Pin, pwmChannel);

  // Inicialize LCD
  lcd.init();
  
  //TURN ON BACKLIGHT
  lcd.backlight();

  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("  Bienvenido a  ");
  lcd.setCursor(0,1);
  lcd.print("    Greenbin    ");
  tdown.setInterval(print_time, 925);
  eeprom_read();
  eeprom_write();
  delay(10000);

  start_leds();
  sound_buzzer();
  lcd.clear();

  // Connect to wifi with password and ssid
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    lcd.setCursor(0,0);
    lcd.print("   Conectando  ");
    lcd.setCursor(0,1);
    lcd.print("      Wifi      ");
  }
  lcd.clear();
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");
}

void print_time(){
  time_s = time_s-1;
  if(time_s<0){
    time_s=59; 
    time_m = time_m-1;
    }
  if(time_m<0){
    time_m=59; 
    time_h = time_h-1;
    }
  secondsjson = secondsjson - 1; 
}

void loop() {
  // Timer start
  tdown.run();

  Serial.println(secondsjson);

  // dimmer_motor.setPower(motorVal); // setPower(0-100%);

  if(flag2==1){
    print_th();
  }

  if(digitalRead (bt_set) == 0){
    if(flag1==0 && flag2==0){flag1=1;
    set = set+1;
    if(set>3){set=0;}
    delay(100); 
  }
  }else{flag1=0;}

  if(digitalRead (bt_up) == 0){
  if(set==0){
    tdown.start();
    process_on_leds();
    start_dimmer_light();
    flag2=1;}
  if(set==1){time_s++;}
  if(set==2){time_m++;}
  if(set==3){time_h++;}
  if(time_s>59){time_s=0;}
  if(time_m>59){time_m=0;}
  if(time_h>99){time_h=0;}
  if(set>0){
    eeprom_write();
    eeprom_print();
    }
  delay(200); 
  }

  if(digitalRead (bt_down) == 0){
  if(set==0){
    tdown.stop();
    process_off_leds();
    stop_dimmer_light();
    stop_dimmer_motor();
    flag2=0;}
  if(set==1){time_s--;}
  if(set==2){time_m--;}
  if(set==3){time_h--;}
  if(time_s<0){time_s=59;}
  if(time_m<0){time_m=59;}
  if(time_h<0){time_h=99;}
  if(set>0){
    eeprom_write();
    eeprom_print();
  }
  delay(200); 
  }

  if(digitalRead (bt_start) == 0){ 
    flag2=1; 
    eeprom_read(); 
    tdown.restart(); 
    tdown.start();
    process_on_leds();
    start_dimmer_light();
    start_dimmer_motor();
    secondsjson = (time_h*3600) + (time_m*60) + (time_s);
    firstStop = secondsjson - 30;
  }
  
  if(flag2 == 0){
    lcd.setCursor(0,0);
    if(set==0){lcd.print("      Timer     ");}
    if(set==1){lcd.print("  Ing Timer SS  ");}
    if(set==2){lcd.print("  Ing Timer MM  ");}
    if(set==3){lcd.print("  Ing Timer HH  ");}
  }
  
  lcd.setCursor(4,1);
  if(time_h<=9){lcd.print("0");}
  lcd.print(time_h);
  lcd.print(":");
  if(time_m<=9){lcd.print("0");}
  lcd.print(time_m);
  lcd.print(":");
  if(time_s<=9){lcd.print("0");}
  lcd.print(time_s);
  lcd.print("   ");

  if(time_s==0 && time_m==0 && time_h==0 && flag2==1){
    flag2=0;
    flag3=0;
    tdown.stop();
    sound_buzzer();
    process_off_leds();
    stop_dimmer_light();
    stop_dimmer_motor();
    process_cooldown_leds();

  }
  
  if(firstStop == secondsjson){
    stop_dimmer_motor();
  }

  if(time_s==0 && time_m==0 && time_h!=0 && flag2==1){
    start_dimmer_motor();
    hourStop = secondsjson - 10;
  }

  if(hourStop == secondsjson){
    stop_dimmer_motor();
  }

  //Send an HTTP POST request every 10 minutes
  if ((millis() - lastTime) > timerDelay && flag3!=1) {

    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      
      Serial.println(WiFi.status());
      sensorReadings = httpGETRequest(serverName);
      Serial.println(sensorReadings);
      JSONVar myObject = JSON.parse(sensorReadings);
  
      // JSON.typeof(jsonVar) can be used to get the type of the var
      if (JSON.typeof(myObject) == "undefined") {
        Serial.println("Parsing input failed!");
        return;
      }
    
      Serial.print("JSON object = ");
      Serial.println(myObject);
    
      // myObject.keys() can be used to get an array of all the keys in the object
      JSONVar keys = myObject.keys();
    
      for (int i = 0; i < 3; i++) {
        JSONVar value = myObject[keys[i]];
        Serial.print(keys[i]);
        Serial.print(" = ");
        Serial.println(value);
        if(i == 0 ){
          JSONID = value;
        }
        if(i == 1 ){
          JSONTime = value;
        }
        if(i == 2 ){
          JSONSize = value;
        }
      }
      Serial.print("1 = ");
      Serial.println(JSONID);
      Serial.print("2 = ");
      Serial.println(JSONTime);
      Serial.print("3 = ");
      Serial.println(JSONSize);
      
      if(JSONID){
        Serial.println("PROCESS_ON");
        if(flag3 == 0){
          secondsjson = JSONTime;
          time_h = secondsjson/3600;
          time_m = (secondsjson % 3600) / 60;
          time_s = (secondsjson % 60);

          flag3 = 1;
          flag2=1;

          firstStop = secondsjson - (turntimemin*30);
          Serial.println(secondsjson);
          Serial.println(firstStop);
          eeprom_write();
          eeprom_read(); 
          tdown.restart(); 
          tdown.start();
          process_on_leds();
          start_dimmer_light();
          start_dimmer_motor();
          // motor_on();
        } 
      }
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}

// Function to request HTTP payload
String httpGETRequest(const char* serverName) {
  WiFiClient client;
  HTTPClient http;
    
  // Your Domain name with URL path or IP address with path
  http.begin(client, serverName);
  
  // If you need Node-RED/server authentication, insert user and password below
  //http.setAuthorization("REPLACE_WITH_SERVER_USERNAME", "REPLACE_WITH_SERVER_PASSWORD");
  
  // Send HTTP POST request
  int httpResponseCode = http.GET();
  
  String payload = "{}"; 
  
  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return payload;
}

// Function to save values in ESP32 MEMORY
void eeprom_write(){
  EEPROM.write(1, time_s);  
  EEPROM.write(2, time_m);  
  EEPROM.write(3, time_h); 
  EEPROM.commit(); 
}

// Function to read values from ESP32 MEMORY
void eeprom_read(){
  time_s =  EEPROM.read(1);
  time_m =  EEPROM.read(2);
  time_h =  EEPROM.read(3);
}

void eeprom_print(){
  int aux1 =  EEPROM.read(1);
  Serial.println(aux1);
  int aux2 =  EEPROM.read(2);
  Serial.println(aux2);
  int aux3 =  EEPROM.read(3);
  Serial.println(aux3);
}

void start_leds(){
  digitalWrite(LEDred, HIGH);
  delay(500);
  digitalWrite(LEDred, LOW);
  delay(500);
  digitalWrite(LEDyellow, HIGH);
  delay(500);
  digitalWrite(LEDyellow, LOW);
  delay(500);
  digitalWrite(LEDgreen, HIGH);
  delay(500);
  digitalWrite(LEDgreen, LOW);
  delay(500);
  digitalWrite(LEDred, HIGH);
  digitalWrite(LEDyellow, HIGH);
  digitalWrite(LEDgreen, HIGH);
  delay(2000);
  digitalWrite(LEDred, HIGH);
  digitalWrite(LEDyellow, LOW);
  digitalWrite(LEDgreen, LOW);
}

// Function to indicate process starting LEDS
void process_on_leds(){
  digitalWrite(LEDred, LOW);
  delay(500);
  digitalWrite(LEDyellow, HIGH);
  delay(500);
  digitalWrite(LEDyellow, LOW);
  delay(500);
  digitalWrite(LEDyellow, HIGH);
  delay(500);
  digitalWrite(LEDyellow, LOW);
  delay(500);
  digitalWrite(LEDyellow, HIGH);
  delay(500);
  digitalWrite(LEDyellow, LOW);
  delay(500);
  digitalWrite(LEDgreen, HIGH);
}

// Function to indicate process STOPING LEDS
void process_cooldown_leds(){
  digitalWrite(LEDyellow, HIGH);
  delay(10000);
  digitalWrite(LEDyellow, LOW);
}
// Function to indicate process STOPING LEDS
void process_off_leds(){
  digitalWrite(LEDgreen, LOW);
  delay(500);
  digitalWrite(LEDyellow, HIGH);
  delay(500);
  digitalWrite(LEDyellow, LOW);
  delay(500);
  digitalWrite(LEDyellow, HIGH);
  delay(500);
  digitalWrite(LEDyellow, LOW);
  delay(500);
  digitalWrite(LEDyellow, HIGH);
  delay(500);
  digitalWrite(LEDyellow, LOW);
  delay(500);
  digitalWrite(LEDred, HIGH);
}

void sound_buzzer(){
  digitalWrite(buzzer, HIGH);
  delay(300);
  digitalWrite(buzzer, LOW);
  delay(200);
  digitalWrite(buzzer, HIGH);
  delay(300);
  digitalWrite(buzzer, LOW);
  delay(200);
  digitalWrite(buzzer, HIGH);
  delay(300);
  digitalWrite(buzzer, LOW);
}

void print_th(){
  float h1 = dht1.readHumidity(); //Read Humidity
  float t1 = dht1.readTemperature(); //Read Temp
  // float h2 = dht1.readHumidity(); //Read Humidity
  // float t2 = dht1.readTemperature(); //Read Temp
  float hf = h1;
  float tf = t1;
  lcd.setCursor(0,0);
  lcd.print("T:");
  lcd.setCursor(2,0);
  lcd.print(tf);
  lcd.setCursor(7,0);
  lcd.print("  ");
  lcd.setCursor(9,0);
  lcd.print("H:");
  lcd.setCursor(11,0);
  lcd.print(hf);
}

void start_dimmer_light(){
  lightL.setBrightness(255);
}

void stop_dimmer_light(){
  lightL.setBrightness(0);
  }

void start_dimmer_motor(){
  lightM.setBrightness(255);
}

void stop_dimmer_motor(){
  lightM.setBrightness(0);
}

// void motor_on(){
//   // digitalWrite(motor1Pin1, HIGH);
//   // digitalWrite(motor1Pin2, LOW);
//   // while (dutyCycle <= 255){
//   //   ledcWrite(pwmChannel, dutyCycle);   
//   //   Serial.print("Forward with duty cycle: ");
//   //   Serial.println(dutyCycle);
//   //   dutyCycle = dutyCycle + 5;
//   //   delay(500);
//   // }
//   // dutyCycle = 200;
//   Serial.println("Motor started");
//   lightM.setBrightness(255);
// }

// void motor_off(){
//   // Stop the DC motor
//   // digitalWrite(motor1Pin1, LOW);
//   // digitalWrite(motor1Pin2, LOW);
//   // delay(1000);
//   Serial.println("Motor stopped");
//   lightM.setBrightness(0);
// }