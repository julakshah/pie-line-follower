#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); // Initialize motorshield
Adafruit_DCMotor *leftMotor = AFMS.getMotor(4); // Left motor attached to M4
Adafruit_DCMotor *rightMotor = AFMS.getMotor(2); // Right motor attached to M3 // right motor flipped

const uint8_t sensorPinLeft = A1; // Left IR sensor
const uint8_t sensorPinRight  = A0; // Right IR sensor

int sensorValLeft;
int sensorValRight;
int motorSLeft;
int motorSRight;

//const int leftOnLower = 75;
const int leftOnUpper = 200; // Upper bound value for left sensor when on track
//leftOn range -- 75 - 300 (Calibration)

//const int rightOnLower = 200;
const int rightOnUpper = 200; // Upper bound value for right sensor when on track
//RightOn range -- 200 - 420 (Calibration)

int baseSpeed = 30; // Default speed -- motor moving forward
int turnSpeed = 10; // Speed of a motor when turning

bool rightHigh = false;
bool leftHigh = false;

void setup() {
  Serial.begin(9600); // Start serial monitor

  // Debugging
  if (!AFMS.begin()) {         
    Serial.println("Could not find Motor Shield. Check wiring.");
    while (1);
  }
  Serial.println("Motor Shield found.");
  
  // Set starting speed and direction of motors
  leftMotor->setSpeed(baseSpeed-5); 
  rightMotor->setSpeed(baseSpeed);
  leftMotor->run(FORWARD);
  rightMotor->run(FORWARD);
}

void loop() {

  // Measure and store sensor values
  sensorValLeft = analogRead(sensorPinLeft); 
  sensorValRight = analogRead(sensorPinRight); 

  // Boolean determining if sensor detects the track based on calibration values
  bool leftOff = (sensorValLeft < leftOnUpper); 
  bool rightOff = (sensorValRight < rightOnUpper);
  
  if (rightOff && leftOff) {
    motorSLeft = 25;
    motorSRight = 25;
    leftMotor->setSpeed(motorSLeft);
    rightMotor->setSpeed(motorSRight);
    if(rightHigh) {
      motorSRight = 30;
      rightMotor->setSpeed(motorSRight);
    } else if (leftHigh) {
      motorSLeft = 30;
      leftMotor->setSpeed(motorSLeft);
    }
    leftMotor->run(FORWARD);
    rightMotor->run(FORWARD);
  } else if (!leftOff && rightOff) {
    // Both left and right sensor on track -- move straight
    motorSLeft = 30;
    motorSRight = 25;
    leftMotor->setSpeed(motorSLeft);
    rightMotor->setSpeed(motorSRight);
    leftMotor->run(FORWARD);
    rightMotor->run(BACKWARD);
    rightHigh = false;
    leftHigh = true;
  } 
  else if (leftOff && !rightOff) {
    // Left on track, right off track -- turn right
    motorSLeft = 25;
    motorSRight = 30;
    leftMotor->setSpeed(motorSLeft);
    rightMotor->setSpeed(motorSRight);
    leftMotor->run(BACKWARD);
    rightMotor->run(FORWARD);
    rightHigh = true;
    leftHigh = false;
  } else {
    motorSLeft = 25;
    motorSRight = 25;
    leftMotor->setSpeed(motorSLeft);
    rightMotor->setSpeed(motorSRight);
    leftMotor->run(FORWARD);
    rightMotor->run(FORWARD);
    rightHigh = false;
    leftHigh = false;
  }
delay(200);

  // Print values
  Serial.print(sensorValLeft);
  Serial.print(" ");
  Serial.print(sensorValRight);
  Serial.print(" ");
  Serial.print(motorSLeft);
  Serial.print(" ");
  Serial.println(motorSRight);
}
