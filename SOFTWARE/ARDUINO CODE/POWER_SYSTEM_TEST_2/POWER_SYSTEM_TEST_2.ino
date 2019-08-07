/* THIS SKETCH CONSISTS OF TESTING AND DEVELOPING
 * THE UART COMMUNICATION IN PROCCESSING AND THE 
 * SPI COMMUNICATION TO THE ARDUINO
 */

#include <SPI.h>

int swi = 0;
 
int solarPin = 0;     //  analog pin 0

int windPin = 1;      //  analog pin 1

int batteryPin = 2;   //  analog pin 2

//  Initializes the safety minimum
int minVolt = 2;

//  Initializes the cases
int case1 = 1;   //  WIND ON,     REST OFF
int case2 = 2;   //  SOLAR ON,    REST OFF
int case3 = 3;   //  ETHANOL ON,  REST OFF
int case4 = 4;   //  ALL OFF
int currentCase = 0;  //case selector



void setup ()
{
  Serial.begin(9600);  

  digitalWrite(SS, HIGH); // set SS high  
  // initialize the SPI for Master Mode
  
  SPI.begin();  
  // Slow down the Master a bit
  SPI.setClockDivider(SPI_CLOCK_DIV8);
}



void loop()
{
  //  READS THE VALUE OF solarPin AND SENDS IT THROUGH THE SERIAL PORT
  float solarVal = mapfloat(analogRead(solarPin), 0, 1023, 0, 12); // maps the value read of 1023 to 12
  //delay(10);
    
  //  READS THE VALUE OF windPin AND STORES IT
  float windVal = mapfloat(analogRead(windPin), 0, 1023, 0, 12); 
  //delay(10);

  //  READS THE VALUE OF batteryPin and stores it
  float batteryVal = 74;      // KEPT CONSTANT FOR TESTING PURPOSES
  //delay(10);
  


  //  ANALYZES THE CURRENT VOLTAGE ON THE SOURCES AND DETERMINES A CASE
  if(  (windVal > solarVal) && (windVal > minVolt)  )         // Selects Wind
  {
    currentCase = case1;    
  } 
  else if (  (solarVal > windVal) && (solarVal > minVolt)  )  // Selects Solar
  {
    currentCase = case2;
  }  
  else if (  (windVal < minVolt) && (solarVal < minVolt)  )   // Selects Ethanol
  {
    currentCase = case3;
  }
  else                                                        // Shuts off power feed
  {
    currentCase = case4;
  }

  Serial.print(solarVal);
  Serial.print(" , ");
  Serial.println(windVal);
  
  
  
  //Serial.println(batteryVal);
  //Serial.println(currentCase);
  
  SPIconnection();
  delay(1000); // DEBUGGING
  
  
}


float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
 return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}



void SPIconnection()
{
    //  START SPI MASTER CONNECTION
  char c;

  // enable Slave Select
  digitalWrite(SS, LOW);

  //send alternate strings
  if(currentCase == case1)
  {
    for (const char * p = "A\n" ; c = *p; p++)
    SPI.transfer (c);  
  }
  else if (currentCase == case2)
  {
    for(const char * p = "B\n"; c = *p; p++)
    SPI.transfer (c);
  }
  else if (currentCase == case3)
  {
    for(const char * p = "C\n"; c = *p; p++)
    SPI.transfer (c);
  }
  else
  {
    for(const char * p = "D\n"; c = *p; p++)
    SPI.transfer (c);  
  }


  //disable Slave Select
  digitalWrite(SS, HIGH);
//  swi = 1-swi;

  //delay(50);    // 1 second delay
  //  END SPI MASTER CONNECTION
}
