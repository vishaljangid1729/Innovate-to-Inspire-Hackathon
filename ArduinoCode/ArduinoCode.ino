int Vpin1 = A5;
int Vpin2 = A4;
int Vpin3 = A3;
int count = 0;
float voltage1, voltage2, voltage3;
float volts1, volts2, volts3;
void setup() {
  Serial.begin(9600);
}
void loop() {
  count = 0;
  voltage1 = analogRead(Vpin1);
  volts1 = voltage1 / 1023 * 5.0;
  Serial.print("Street Light 1:");
  Serial.println(volts1);
  voltage2 = analogRead(Vpin2);
  volts2 = voltage2 / 1023 * 5.0;
  Serial.print("Street Light 2:");
  Serial.println(volts2);
  voltage3 = analogRead(Vpin3);
  volts3 = voltage3 / 1023 * 5.0;
  Serial.print("Street Light 3:");
  Serial.println(volts3);
  if (volts1 > 2.5) {
    Serial.println("Street Light one is faulty");
    count += 1;
  }
  if (volts2 > 2.5) {
    Serial.println("Street Light two is faulty");
    count += 1;
  }
  if (volts3 > 2.5) {
    Serial.println("Street Light three is faulty");
    count += 1;
  }
  else if(volts1 < 2.5 && volts2 < 2.5 && volts3 < 2.5)  {k
    Serial.println("");
    count = 0;
  }
  Serial.print("No. of Faults = ");
  Serial.println(count);
}
