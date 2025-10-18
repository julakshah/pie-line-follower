int leftSensorPin = A1; //left input pin
int rightSensorPin = A0; //right input pin

void setup() {
  Serial.begin(9600);
  pinMode(leftSensorPin, INPUT);
  pinMode(rightSensorPin, INPUT);
}

void loop() {
  //send formatted sensor values
  int leftVal = analogRead(leftSensorPin);
  int rightVal = analogRead(rightSensorPin);
  Serial.print(leftVal);
  Serial.print(" ");
  Serial.println(rightVal);
  delay(10);
}
