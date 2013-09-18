
/*------------------------------------------------------------------------------------
arduino_miniProject_Problem3.ino

Reads the status of a switchs attached to pins 2 and 4 
The states of a multi-color LED are set according to:
  * Green if no buttons pressed 
  * Yellow is a single button is pressed
  * Red if both buttons are pressed 

Created: 9/13/13 - Joshua Vaughan - joshua.vaughan@louisiana.edu

Modified:
  * 
------------------------------------------------------------------------------------*/

// Pin declarations
int pushButton1 = 2;      // pin 2 has a pushbutton attached to it. 
int pushButton2 = 4;      // pin 4 has a pushbutton attached to it. 
int blueLEDpin = 8;       // The blue lead of the LED is attached to pin 8
int greenLEDpin = 9;      // The green lead of the LED is attached to pin 9
int redLEDpin = 10;       // The red lead of the LED is attached to pin 10

// Global variables
int blueLEDstate = LOW;             // current state of the blue LED, off initially
int greenLEDstate = HIGH;           // current state of the green LED, on initially
int redLEDstate = LOW;              // current state of the red LED, off initially
                              

// This is always run once when the sketch starts
void setup() {
  // initialize serial communication at 9600 bits per second - for debugging
  Serial.begin(9600);
  
  // Remember that the digital pins can be in or out, so... 
  pinMode(pushButton1, INPUT);       // define the button1 digital pin as an INPUT
  pinMode(pushButton2, INPUT);       // define the button2 digital pin as an INPUT  
  pinMode(blueLEDpin, OUTPUT);       // define blue LED pin as OUTPUT
  pinMode(greenLEDpin, OUTPUT);      // define green LED pin as OUTPUT
  pinMode(redLEDpin, OUTPUT);        // define red LED pin as OUTPUT
}

// the loop routine runs over and over again forever:
void loop() {
  
  // read the value of the two pushbuttons
  int currStateButton1 = digitalRead(pushButton1);
  int currStateButton2 = digitalRead(pushButton2);
  
  
  if (currStateButton1 && currStateButton2){
    
    digitalWrite(redLEDpin,HIGH);       // Turn on the red LED
    digitalWrite(greenLEDpin,LOW);      // Turn off the green LED
    digitalWrite(blueLEDpin,LOW);       // Turn off the blue LED
    
    // Uncomment for debugging
    // Serial.println("Both Buttons Pressed");
   } 
   else if (currStateButton1 || currStateButton2){
      
     // Set the Red & Green LED Ons - Their combo makes yellow
     digitalWrite(redLEDpin,HIGH);     // Turn on the red LED
     digitalWrite(greenLEDpin,HIGH);   // Turn on the green LED
    
     // Uncomment for debugging
     // Serial.println("One Button Pressed");
   }
   else{
     digitalWrite(greenLEDpin,HIGH);     // Turn on the green LED
     digitalWrite(blueLEDpin,LOW);       // Turn off the blue LED
     digitalWrite(redLEDpin,LOW);        // Turn off the red LED
     
     // Uncomment for debugging
     // Serial.println("No Buttons Pressed");
   }
}
