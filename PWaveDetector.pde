/*
 State Spammer for P-Wave Detector
 Copyright 2011, Casey Halverson
 MIT License (see README)

 This very simple code monitors the level of a digital line and dumps it over the serial.
 This will let us detect very minute make-and-break events on the host and figure out
 what it means there.

 */

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT);
  digitalWrite(2, HIGH); // pullup
}

void loop() {
  delayMicroseconds(1000);
  int sensorValue = digitalRead(2);
  Serial.print(sensorValue, DEC);
}


