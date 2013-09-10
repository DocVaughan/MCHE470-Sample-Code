/*------------------------------------------------------------------------------------
arduino_Ardumoto_Basic.ino

Demonstrating basic use of the SparkFun Arduomoto Shield

Product Page: https://www.sparkfun.com/products/9896
Code adapted from: https://www.sparkfun.com/tutorials/195

Created: 09/10/13 - Joshua Vaughan - joshua.vaughan@louisiana.edu

Modified:
  * mm/dd/yy - Name (email if not same person as above)
    - major change 1
    - major change 2
  * mm/dd/yy - Name (email if not same person as above)
    - major change 1
------------------------------------------------------------------------------------*/

int pwm_a = 3;     // PWM control for motor outputs 1 and 2 is on digital pin 3
int pwm_b = 11;    // PWM control for motor outputs 3 and 4 is on digital pin 11
int dir_a = 12;    // direction control for motor outputs 1 and 2 is on digital pin 12
int dir_b = 13;    // direction control for motor outputs 3 and 4 is on digital pin 13


// This is always run once when the sketch starts
void setup()
{
  pinMode(pwm_a, OUTPUT);  //Set control pins to be outputs
  pinMode(pwm_b, OUTPUT);
  pinMode(dir_a, OUTPUT);
  pinMode(dir_b, OUTPUT);  
}

// This runs immediately after setup, looping indefinitely
void loop()
{
  digitalWrite(dir_a, LOW);  //Set motor direction, 1 low, 2 high
  digitalWrite(dir_b, LOW);  //Set motor direction, 3 high, 4 low
  
  //set both motors to run at 100% duty cycle (fast)
  analogWrite(pwm_a, 255);     
  analogWrite(pwm_b, 255);
  
  // run for 1000ms (1 s)
  delay(1000);
  
  //set both motors OFF
  analogWrite(pwm_a, 0);      
  analogWrite(pwm_b, 0);
  
  // stay off for 1000ms (1s)
  delay(1000);
  
//  // To reverse, un-comment below  
//  // NOTE: Motor that comes with the SIK is NOT reversable
//
//  digitalWrite(dir_a, HIGH);  //Reverse motor direction, 1 high, 2 low
//  digitalWrite(dir_b, HIGH);  //Reverse motor direction, 3 low, 4 high
//  
//  delay(1000);
//
//  analogWrite(pwm_a, 255);
//  //set both motors to run at (100/255 = 39)% duty cycle   
//  analogWrite(pwm_b, 255);
//  
//  delay(1000);
//
//  //set both motors OFF
//  analogWrite(pwm_a, 0);      
//  analogWrite(pwm_b, 0);
//  
//  // delay 2s before looping
//  delay(2000);
}

