int redLed = 9;
int greenLed = 10;
int blueLed = 11;
int d = 1000;
void setup()
{
  pinMode(blueLed, OUTPUT);
  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);
}

void loop()
{
  delay(10); // Delay a little bit to improve simulation performance
  analogWrite(redLed,255);
  delay(d);
  analogWrite(redLed,255);
  analogWrite(greenLed,165);
  delay(d);
  analogWrite(redLed,255);
  analogWrite(greenLed,255);
  delay(d);
  analogWrite(redLed,0);
  analogWrite(greenLed,255);
  delay(d);
  analogWrite(redLed,0);
  analogWrite(greenLed,0);
  analogWrite(blueLed,255);
  delay(d);
  analogWrite(redLed,0);
  analogWrite(greenLed,0);
  analogWrite(blueLed,0);
}
