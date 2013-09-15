
/*------------------------------------------------------------------------------------
arduino_miniProject_Problem4.ino

Reads the position of a pontentiometer and aligns a servo to the same angle

Created: 9/13/13 - Joshua Vaughan - joshua.vaughan@louisiana.edu

Modified:
  * 
------------------------------------------------------------------------------------*/

// include the servo libary
#include <Servo.h> 

// create servo object to control a servo
Servo myServo;   

// Pin declarations
int potentiometer = 5;      // pin A5 has the potentiometer attached to it. 

                              
// This is always run once when the sketch starts
void setup() {
  // initialize serial communication at 9600 bits per second - for debugging
  Serial.begin(9600);
  
  // Enable control of a servo on pin 3:
  myServo.attach(3);
}

// the loop routine runs over and over again forever:
void loop() {
  int servoAngle;    // The desired angle of the servo
  
  // read the input on analog pin 5:
  int potValue = analogRead(potentiometer);
  
  // Map the potentiomoter output range to the servo angle range
  // The relatively cheap potentiometer in the kit acts strange near 0
  //   the servo will too as a result
  servoAngle= map(potValue, 0, 1023, 0, 180);
  
  // nsure the position is within an acceptable range
  servoAngle = constrain(servoAngle, 0, 180);
  
  // Move the servo to the desired angle
  myServo.write(servoAngle);
  
  // Uncomment for debugging 
  Serial.print("Potentiometer Value: ");   
  Serial.print(potValue);              // print the value of the pot
  Serial.print("  \t");                // prints a tab, for pretty, readable output
  Serial.print("Desired Servo Angle: "); 
  Serial.println(servoAngle);          // print the desired servo angle
}
