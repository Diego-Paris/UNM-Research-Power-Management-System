
// 51 Hz
// minimum Pulse Width of 1.28ms



#include <PWM.h>

const int pwm = 9 ;    //  naming pin 3 as PWM
const int adc = A0 ;   //  naming pin A0 of analog input for ADC 0 - 1023


int32_t frequency = 51; //  sets the PWM pins frequency


void setup() 
{
      // put your setup code here, to run once:
      
      Serial.begin(9600);
      
      pinMode(pwm,OUTPUT) ;  //  setting the PWN pin as output
      
      InitTimersSafe();     //   this makes all the Timers except Timer 0 available for setting at different Frequencies 

      bool success = SetPinFrequencySafe(pwm, frequency);   //   this sets PWN pin to the Value stated for frequency
      
      if (success)    //   pin 13 Lights Up if the SetPinFrequecySafe function was successful    *** OPTIONAL ***
      {
        pinMode(13, OUTPUT);
        digitalWrite(13, HIGH);
      }

}


void loop()
{
      // put your main code here, to run repeatedly:
      
      int adc  = analogRead(A0) ;       //  reading analog voltage and storing it in an integer in the variable 'adc'
      
      adc = map(adc, 0, 1023, 0, 255);  //  scales the output of adc, which is 10 bit and gives values 0 to 1023
                                        //  to the values of the PWM, which is 0 to 255
                                        //  analogWrite funtion can only receives values of this range, o to 255
      
      Serial.println(adc);
      
//      analogWrite(pwm,adc) ;          //   not used when using the PWM library and its functions 
      
      pwmWrite(pwm, adc);               //   PWM function sending

}
