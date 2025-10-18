int leftSensorPin = A1;
int rightSensorPin = A0;

void setup() {
  Serial.begin(9600);
  pinMode(leftSensorPin, INPUT);
  pinMode(rightSensorPin, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  int leftVal = analogRead(leftSensorPin);
  int rightVal = analogRead(rightSensorPin);
  Serial.print(leftVal);
  Serial.print(" ");
  Serial.println(rightVal);
  delay(10);
}
