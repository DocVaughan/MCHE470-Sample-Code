
/*------------------------------------------------------------------------------------
arduino_miniProject_Problem2.ino

Reads the status of flex sensor every 500ms (0.5s),
and prints the value to the Serial Monitor

Created: 9/13/13 - Joshua Vaughan - joshua.vaughan@louisiana.edu

Modified:
  * 
------------------------------------------------------------------------------------*/

// Pin declarations
int flexSensor = 5;      // The flex sensor is attached to A5

                             
// This is always run once when the sketch starts
void setup() {
  // initialize serial communication at 9600 bits per second - for debugging
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  int flexReading;               // The A/D value of the flex sensor
  
  // Take a reading from the flex sensor
  flexReading = analogRead(flexSensor);
  
  // Print that reading 
  Serial.print("Flex Sensor Value: ");
  Serial.println(flexReading);
  
  // Delay for 500ms (0.5s)
  delay(500);
  
}
