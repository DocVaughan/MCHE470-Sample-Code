/*------------------------------------------------------------------------------------
MidTerm_Problem2e_Answer.ino

One way to answer problem 2e from the MidTerm

Created: 10/22/13 - Joshua Vaughan 
                  - joshua.vaughan@louisiana.edu

Modified:
------------------------------------------------------------------------------------*/

void setup(){
  // Set up the Serial communication
  Serial.begin(9600);
  
  // We only want this to run once.
  // One way to do that is put it in setup() instead of loop()
  for(int ii = 0;ii<=20;ii=ii+2){
    if (ii<10){
      Serial.println(ii*ii);
    }
    else{
      Serial.println(ii*ii*ii);
    }
  }
}

void loop() {
}

