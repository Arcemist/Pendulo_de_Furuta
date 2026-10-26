struct Encoder {
  const int A;
  const int B;
  const int Z;
  volatile int count;
};

/* DISCLAIMER:
Al cambiar los pines mencionados a continuacion
se debe tambien cambiar la configuracion de la 
lectura por registros que esta en las interrupciones
externas mas abajo en este archivo.
*/
struct Encoder brazo = {
  .A = 3,
  .B = 2,
  .Z = 5,
  .count = 0
};
struct Encoder pendulo = {
  .A = 19,
  .B = 18,
  .Z = 16,
  .count = 0
};

inline void Inicializar_encoders() {

  switch (Modo_Funcionamiento) {
    case PRUEBA_PENDULO:
      pinMode(pendulo.A, INPUT_PULLUP);
      pinMode(pendulo.B, INPUT_PULLUP);
      pinMode(pendulo.Z, INPUT_PULLUP);

      attachInterrupt(
        digitalPinToInterrupt(pendulo.A),
        Pendulo_A,
        CHANGE
      );
      attachInterrupt(
        digitalPinToInterrupt(pendulo.B),
        Pendulo_B,
        CHANGE
      );
      attachInterrupt(
        digitalPinToInterrupt(pendulo.Z),
        Pendulo_Referencia,
        RISING
      );
    break;

    case PRUEBA_MOTOR:
      pinMode(brazo.A, INPUT_PULLUP);
      pinMode(brazo.B, INPUT_PULLUP);
      pinMode(brazo.Z, INPUT_PULLUP);

      attachInterrupt(
        digitalPinToInterrupt(brazo.A),
        Brazo_A,
        CHANGE
      );
      attachInterrupt(
        digitalPinToInterrupt(brazo.B),
        Brazo_B,
        CHANGE
      );
      attachInterrupt(
        digitalPinToInterrupt(brazo.Z),
        Brazo_Referencia,
        RISING
      );
    break;
  }
}

void Pendulo_A() {
  const bool valor_A = PINE & (1 << PE5); // Pin 3
  const bool valor_B = PINE & (1 << PE4); // Pin 2

  if (valor_A == valor_B) 
    { pendulo.count--; }
  else
    { pendulo.count++; };
}
void Pendulo_B() {
  const bool valor_A = PINE & (1 << PE5); // Pin 3
  const bool valor_B = PINE & (1 << PE4); // Pin 2

  if (valor_A == valor_B) 
    { pendulo.count++; }
  else 
    { pendulo.count--; };
}

void Brazo_A() {
  const bool valor_A = PIND & (1 << PD2); // Pin 19
  const bool valor_B = PIND & (1 << PD3); // Pin 18

  if (valor_A == valor_B) 
    { brazo.count++; }
  else
    { brazo.count--; };
}
void Brazo_B() {
  const bool valor_A = PIND & (1 << PD2); // Pin 19
  const bool valor_B = PIND & (1 << PD3); // Pin 18

  if (valor_A == valor_B) 
    { brazo.count--; }
  else
    { brazo.count++; };
}

void Pendulo_Referencia() { pendulo.count = 0; }
void Brazo_Referencia()   { brazo.count = 0; }