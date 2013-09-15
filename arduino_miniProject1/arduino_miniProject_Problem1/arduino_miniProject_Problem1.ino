
/*------------------------------------------------------------------------------------
arduino_miniProject_Problem1.ino

Reads the status of a switch attached to pin 2, 
and toggles onboard LED with each press

Created: 9/11/13 - Joshua Vaughan - joshua.vaughan@louisiana.edu

Modified:
  * 
------------------------------------------------------------------------------------*/

// Pin declarations
int pushButton = 2;      // pin 2 has a pushbutton attached to it. 
int LEDpin = 13;         // The onboard LED is attached to pin 13

// Global variables
int LEDstate = LOW;           // the current state of the LED, off initially
                              

// This is always run once when the sketch starts
void setup() {
  // initialize serial communication at 9600 bits per second - for debugging
  Serial.begin(9600);
  
  // Remember that the digital pins can be in or out, so... 
  pinMode(pushButton, INPUT);    // define the button digital pin as an INPUT
  pinMode(LEDpin, OUTPUT);       // define LED pin as OUTPUT
}

// the loop routine runs over and over again forever:
void loop() {
  
  // read the value of the pin
  int currButtonState = digitalRead(pushButton);
  
  if (currButtonState){
    
    // Toggle the LEDstate
    LEDstate = !LEDstate;
    
    // Uncomment for debugging
    Serial.println("Button Pressed");  // print state change to Serial Monitor
    Serial.println(LEDstate);
    digitalWrite(LEDpin,LEDstate);     // Toggle  the LED
    delay(250);                        // delay 100ms to debounce switch readings

     }
}
