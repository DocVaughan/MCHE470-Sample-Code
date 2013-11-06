/*------------------------------------------------------------------------------------
MidTerm_Problem2e_Answer.ino

One way to answer problem 2e from the MidTerm

This method goes into an infinite loop after the items are printed the first time.

Created: 11/6/13 - Joshua Vaughan 
                 - joshua.vaughan@louisiana.edu

Modified:
------------------------------------------------------------------------------------*/

void setup(){
  // Set up the Serial communication
  Serial.begin(9600);
}

void loop() {
  
  // We only want this to run once.
  for(int ii = 0;ii<=20;ii=ii+2){
    if (ii<10){
      Serial.println(ii*ii);
    }
    else{
      Serial.println(ii*ii*ii);
    }
  }
  
  // after running once, go into an infinite loop to prevent 2nd run
  while(1){}
}

