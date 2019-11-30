/* F5 TEST FOR ESP2PY
 * Written by Junicchi
 * https://github.com/KebabLord/esp_to_python
 * It simply increases and returns a variable everytime a python req came */
uint8_t pingPin = D6;  //D4
uint8_t echoPin = D5;  //D3
uint8_t buzzerpin = D7; 
int count=0;
#include "ESP_MICRO.h" //Include the micro library 
int testvariable = 0;
void setup(){
  Serial.begin(9600); // Starting serial port for seeing details
  start("AyushRedmi","12345678");  // EnAIt will connect to your wifi with given details
  pinMode(buzzerpin, OUTPUT);
}
void loop(){
  //waitUntilNewReq();  //Waits until a new request from python come
  /* increases index when a new request came*/
  //testvariable += 1;
 //returnThisInt(testvariable); 
  long duration, inches, cm;
  //Serial.print('c');
  pinMode(pingPin, OUTPUT);
  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(pingPin, LOW);
  pinMode(echoPin, INPUT);
  duration = pulseIn(echoPin, HIGH);
  //Serial.print('b');
  cm = microsecondsToCentimeters(duration);
  Serial.println(cm);
   
  if (cm<60&&cm>2&&count==0)
  {count+=1;
  waitUntilNewReq(); 
     if (count==0){count+=1;}
     else if (count==1){count-=1;}
     returnThisInt(69); //Returns the data to python
     
     delayMicroseconds(6000);
    
    }
   else
   {
     waitUntilNewReq(); 
     returnThisInt(0);
    
    }
      
  // Serial.print('a');   //Using a as a seperator
  
   //delay(50);   //will check
}

long microsecondsToCentimeters(long microseconds) {
   return microseconds / 29 / 2;
}
