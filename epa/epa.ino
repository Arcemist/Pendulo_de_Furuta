struct Encoder {
  const int A;
  const int B;
  const int Z;
  volatile int count;
};

Encoder brazo = {
  .A = 3,
  .B = 5,
  .Z = 2,
  .count = 0
};

Encoder pendulo = {
  .A = 18,
  .B = 16,
  .Z = 19,
  .count = 0
};

bool cambio = 0;

void setup() {
  Serial.begin(9600);

  //pinMode(brazo.A, INPUT_PULLUP);
  //pinMode(brazo.B, INPUT_PULLUP);
  //pinMode(brazo.Z, INPUT_PULLUP);

  pinMode(pendulo.A, INPUT_PULLUP);
  pinMode(pendulo.B, INPUT_PULLUP);
  pinMode(pendulo.Z, INPUT_PULLUP);

  //attachInterrupt(digitalPinToInterrupt(brazo.A), Brazo_A, RISING);
  //attachInterrupt(digitalPinToInterrupt(brazo.Z), Brazo_Z, RISING);

  attachInterrupt(digitalPinToInterrupt(pendulo.A), Pendulo_A, RISING);
  attachInterrupt(digitalPinToInterrupt(pendulo.Z), Pendulo_Z, RISING);

  // Esperar la sincronia
  //while (true) {
  //  if (Serial.available() > 0) {
  //    char incomingByte = Serial.read();
  //    if (incomingByte == 'S') {
  //      break;
  //    }
  //  }
  //}
}

void loop() {
  if (cambio) {
    //Serial.print("Brazo: ");
    //Serial.println(brazo.count);
    //Serial.print("Pendulo: ");
    //Serial.println(pendulo.count);
    cambio = 0;
  }
}

//void Brazo_A() {
// if (digitalRead(brazo.B) == LOW) { // Puede ser optimizado con registros
//    brazo.count++;
//  } else {
//    brazo.count--;
//  };
//  cambio = 1;
//}

void Pendulo_A() {
  if (digitalRead(pendulo.B) == HIGH) {  // Puede ser optimizado con registros
    pendulo.count++;
  } else {
    pendulo.count--;
  };

  if (pendulo.count > 1024) {
    pendulo.count = 0;
  };

  cambio = 1;
}

void Brazo_Z() {
  brazo.count = 0;
}

void Pendulo_Z() {
  pendulo.count = 0;
  Serial.println("Esta en el 0");
}
