#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_DCMotor *leftmotor = AFMS.getMotor(1);
Adafruit_DCMotor *rightmotor = AFMS.getMotor(2);

/*PID variables*/
unsigned long lastTime;
double Input, Output, Setpoint;
double errSum, lastErr;
double kp, ki, kd;
/*working variables*/
bool runFlag = true; // setting to true for testing purposes
float k_vals[] = {1.0, 1.0, 1.0};
String prev = "";

  

void setup() {
  Serial.begin(9600);
  AFMS.begin();
  
  leftmotor->setSpeed(0);
  leftmotor->run(FORWARD);
}

void loop() {
  // Get python script k vals, otherwise use inbuilt
  String serial_string = Serial.readString();
  serial_string.trim();

  if(runFlag) {  
    //update k vals only when new message comes
    if(serial_string != prev) {  
      prev = serial_string;
      char pid_flag = serial_string.substring(0,1);
      float val = (float)serial_string.subString(2) / 100;
      // Do PID shenanigans
      switch (pid_flag) {
        case "p":
          k_vals[0] = val;
          break;
        case "i":
          k_vals[1] = val;
          break;
        case "d":
          k_vals[2] = val;
          break;
      }
    }
    //compute the PID positions
    Compute();

  } else if (serial_string = "run") {
    runFlag = true;
    delay(200);
  }
}

void Compute()
{
  /*How long since we last calculated*/
  unsigned long now = millis();
  double timeChange = (double)(now - lastTime);

  /*Compute all the working error variables*/
  double error = Setpoint - Input;
  errSum += (error * timeChange);
  double dErr = (error - lastErr) / timeChange;

  /*Compute PID Output*/
  Output = kp * error + ki * errSum + kd * dErr;

  /*Remember some variables for next time*/
  lastErr = error;
  lastTime = now;
}


void SetTunings(double Kp, double Ki, double Kd)
{
  kp = Kp;
  ki = Ki;
  kd = Kd;
}
