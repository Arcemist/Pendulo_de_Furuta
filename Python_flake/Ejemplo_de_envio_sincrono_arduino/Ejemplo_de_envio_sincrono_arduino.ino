void setup() {
  Serial.begin(9600);

  while (true) {
    if (Serial.available() > 0) {
      char incomingByte = Serial.read();
      if (incomingByte == 'S') {
        break; // Exit the loop and start the main program
      }
    }
  }
}

void loop() {
  Serial.println("epa,hola");
}
