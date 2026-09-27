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

  // Cosas del Brazo
  pinMode(brazo.A, INPUT_PULLUP);
  pinMode(brazo.B, INPUT_PULLUP);
  pinMode(brazo.Z, INPUT_PULLUP);

  attachInterrupt(
    digitalPinToInterrupt(brazo.A),
    Brazo_Movimiento,
    RISING
  );
  attachInterrupt(
    digitalPinToInterrupt(brazo.Z),
    Brazo_Referencia,
    RISING
  );

  // Cosas del Pendulo
  pinMode(pendulo.A, INPUT_PULLUP);
  pinMode(pendulo.B, INPUT_PULLUP);
  pinMode(pendulo.Z, INPUT_PULLUP);

  attachInterrupt(
    digitalPinToInterrupt(pendulo.A),
    Pendulo_Movimiento,
    RISING
  );
  attachInterrupt(
    digitalPinToInterrupt(pendulo.Z),
    Pendulo_Referencia,
    RISING
  );

  // Esperar la señal de sincronia
  Serial.begin(9600);
  while (true) {
    if (Serial.available() > 0) {
      char incomingByte = Serial.read();
      if (incomingByte == 'S') {
        break;
      }
    }
  };

}

void loop() {
  if (cambio) {
    Enviar_Valores();
    cambio = 0;
  }
}