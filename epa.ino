struct Encoder {
  int A;
  int B;
  int Z;
  int count;
};

Encoder brazo;
Encoder pendulo;

void setup() {

  brazo.A = 3;
  brazo.B = 5;
  brazo.Z = 2;
  brazo.count = 0;

  pendulo.A = 18;
  pendulo.B = 16;
  pendulo.Z = 19;
  pendulo.count = 0;

  pinMode(brazo.A, INPUT_PULLUP);
  pinMode(brazo.B, INPUT_PULLUP);
  pinMode(brazo.Z, INPUT_PULLUP);

  pinMode(pendulo.A, INPUT_PULLUP);
  pinMode(pendulo.B, INPUT_PULLUP);
  pinMode(pendulo.Z, INPUT_PULLUP);

  Serial.begin(9600);

  attachInterrupt(digitalPinToInterrupt(brazo.A), Brazo_A, RISING);
  attachInterrupt(digitalPinToInterrupt(brazo.Z), Brazo_Z, RISING);

  attachInterrupt(digitalPinToInterrupt(pendulo.A), Pendulo_A, RISING);
  attachInterrupt(digitalPinToInterrupt(pendulo.Z), Pendulo_Z, RISING);
}

void loop() {}

void Brazo_A() {
 if (digitalRead(brazo.B) == LOW) {
    brazo.count++;
  } else {
    brazo.count--;
  }
}

void Brazo_Z() {
  Serial.print("Brazo: ");
  Serial.println(brazo.count);
  brazo.count = 0;
}

void Pendulo_A() {
 if (digitalRead(pendulo.B) == HIGH) {
    pendulo.count++;
  } else {
    pendulo.count--;
  }
}

void Pendulo_Z() {
  Serial.print("Pendulo: ");
  Serial.println(pendulo.count);
  pendulo.count = 0;
}
