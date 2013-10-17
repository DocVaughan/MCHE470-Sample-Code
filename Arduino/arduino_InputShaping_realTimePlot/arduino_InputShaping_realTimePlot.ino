/*------------------------------------------------------------------------------------
 arduino_InputShaping_realTimePlot.ino
 
 Implementation of input shaping - 
   outputs values to a serial conncetion for realtime plotting 
   with matplotlib or MATLAB
 
 Created: 10/4/13 - Joshua Vaughan - joshua.vaughan@louisiana.edu
 
 Modified:
   * 10/13/13 - JEV - joshua.vaughan@louisiana.edu
     - updated commenting
     - 
 ------------------------------------------------------------------------------------*/
// Variables declared here are global
const float pi = 3.14;         // declare and define pi
double sampleTime = 100;       // the time between samples (ms)
unsigned long lastTime;        // to store the time of the last loop
double shaper[4];              // create an array to store shaper parameters
double shaperBuffer[100];      // create a buffer for the input shaped output
double A1buffer[100];          // create a buffer for the A1 portion of shaped output 
double A2buffer[100];          // create a buffer for the A1 portion of shaped output 
int bufferIndex = 0;           // create a variable to mark the current buffer position

// Pin declarations
int pushButton = 2;          // pin 2 has a pushbutton attached to it. 

// This is always run once when the sketch starts
// Use to initialize variables, pin modes, libraries, communication, etc
void setup()
{
  // initialize serial communication at 9600 bits per second
  Serial.begin(9600);

  // define the button digital pin as an INPUT
  pinMode(pushButton, INPUT);    

  // define the system parameters
  double freq = 0.5;       // system natural frequency (Hz)
  double zeta = 0.0;       // damping ratio

  // fill the buffers with zeros
  //   leaving them empty can result in strange results
  for (int ii=0; ii < 100; ii++)
  {
    shaperBuffer[ii] = 0;
    A1buffer[ii] = 0;
    A2buffer[ii] = 0;
  }

  // call the ZV shaper function
  ZV(freq, zeta, shaper);   

//  // Uncomment for debugging shaper solution
//  Serial.print("|Ai| = |");   
//  Serial.print(shaper[0]);            // print the Amp1
//  Serial.print("  \t");               // prints a tab, for pretty, readable output
//  Serial.print(shaper[1]);            // print the Amp2
//  Serial.println("|");
//  Serial.print("|ti| = |");   
//  Serial.print(shaper[2]);            // print the t1
//  Serial.print("  \t");               // prints a tab, for pretty, readable output
//  Serial.print(shaper[3]);            // print the t2
//  Serial.println("|");
//  Serial.println(" ");
//
//  // Wait for Serial communication to finish
//  Serial.flush();
}


// This runs immediately after setup, looping indefinitely
void loop()
{
  double Amp1, Amp2, t1, t2;  // declare temp variables for ZV solution
  double currentOutput, currentA1, currentA2;       // the current total output
  int currButtonState;

  // Retrieve the shaper values from the array
  Amp1 = shaper[0];
  Amp2 = shaper[1];
  t1 = shaper[2];
  t2 = shaper[3];

  // get the current time
  unsigned long now = millis();

  // calculate the time change since the last loop
  int timeChange = (now - lastTime);

  // if the time elapsed is >= the sampleTime, update the shaped output
  if (timeChange >= sampleTime)
  {
    // read the value of the pin
    currButtonState = digitalRead(pushButton);

    // The A1 buffer for plotting output
    A1buffer[bufferIndex] = Amp1*float(currButtonState);
    
    // The A2 buffer for plotting output
    A2buffer[(bufferIndex + int(round(t2/(sampleTime/1000)))) % 99] = Amp2*float(currButtonState);


    // The total output (add the A1 portion to the saved buffer from A2)
    shaperBuffer[bufferIndex] = shaperBuffer[bufferIndex] + Amp1*float(currButtonState);
    
    // save the A2 porition of the output for later
    shaperBuffer[(bufferIndex + int(round(t2/(sampleTime/1000)))) % 99] = Amp2*float(currButtonState);

    // set the current position of the shaperBuffer as the currentOutput
    currentOutput = shaperBuffer[bufferIndex];
    currentA1 = A1buffer[bufferIndex];
    currentA2 = A2buffer[bufferIndex];

    // clear the current element of the shaperBuffer after it is output
    shaperBuffer[bufferIndex] = 0;
    A1buffer[bufferIndex] = 0;
    A2buffer[bufferIndex] = 0;
    
    Serial.print(float(currButtonState));
    Serial.print(" ");              // prints a tab, to make parsing easier
    Serial.print(currentA1);           
    Serial.print(" ");              // prints a tab, to make parsing easier
    Serial.print(currentA2);      
    Serial.print(" ");              // prints a tab, to make parsing easier
    Serial.print(currentOutput); 
    Serial.print("\n");             // use an explicit newline character
    Serial.flush();                 // wait for serial comm to finish
    
  
    // if the next index is outside the buffer size, loop back to the beginning
    if (bufferIndex + 1 < 99)
    {
      bufferIndex++;
    }
    else
    {
      bufferIndex = 0;
    }

    // Remember some variables for next time
    lastTime = now;
  } 
}


void ZV(double freq, double zeta, double shaper[4])
{
  double Amp1, Amp2, t1, t2;  // declare temp variables for ZV solution
  
  double K = exp(-zeta*pi/(sqrt(1-zeta*zeta)));
  
  // define the damped period of oscillation
  double wd = freq*2*pi*sqrt(1-zeta*zeta);
  double tau = 2*pi/wd;
  
  // solve for the impulse amplitudes
  Amp1 = 1/(1+K);
  Amp2 = K/(1+K);
  
  // solve for the impulse times, t1 always 0
  t1 = 0;
  t2 = tau/2;
  
  // Put the shaper values into the array
  shaper[0] = Amp1;
  shaper[1] = Amp2;
  shaper[2] = t1;
  shaper[3] = t2;
} 


