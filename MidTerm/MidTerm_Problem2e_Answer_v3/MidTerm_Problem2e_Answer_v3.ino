/*------------------------------------------------------------------------------------
MidTerm_Problem2e_Answer.ino

One way to answer problem 2e from the MidTerm

This method using a counter and if..else check to limit to one run

Created: 11/6/13 - Joshua Vaughan 
                 - joshua.vaughan@louisiana.edu

Modified:
------------------------------------------------------------------------------------*/

int count = 0;    // Counter for number of times the loop has run

void setup(){
  // Set up the Serial communication
  Serial.begin(9600);
}

void loop() {
  
  // If count is 1 or greater don't print to the Serial Monitor
  if(count < 1){
    for(int ii = 0;ii<=20;ii=ii+2){
      if (ii<10){
        Serial.println(ii*ii);
      }
      else{
        Serial.println(ii*ii*ii);
      }
    }
    
    // incremement counter by 1
    count++;       // This is shorthand for count = count + 1;
  }
}

