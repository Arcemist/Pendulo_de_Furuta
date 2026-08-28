int encoderCount;

void setup() {
  pinMode(3, INPUT_PULLUP);
  pinMode(2, INPUT_PULLUP);
  pinMode(5, INPUT_PULLUP);
  Serial.begin(9600);

  attachInterrupt(digitalPinToInterrupt(3), doEncoderA, RISING);
  attachInterrupt(digitalPinToInterrupt(2), doEncoderZ, RISING);
}

void loop() {
}

void doEncoderA() {
 if (digitalRead(5) == HIGH) {
    encoderCount++; // Clockwise
  } else {
    encoderCount--; // Counter-Clockwise
  }
  
}

void doEncoderZ() {
  Serial.println(encoderCount);
  encoderCount = 0;
  
}