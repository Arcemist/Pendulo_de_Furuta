volatile int Lecturas[32];
volatile byte posicion_libre = 0;
int Reduccion;
volatile int Reductor = 1;

inline void Inicializar_telemetria() {
  noInterrupts();

  /* Configuracion del Timer 1:

  Se eligio el modo CTC
  El preescaler en 8
  El valor de comparacion en 199

  Porque esto consigue una frecuencia 
  de reloj de 0.1ms o 10kHz
  
  */
  TCCR1B |= (1 << WGM12);
  TCCR1B |= (1 << CS11);
  OCR1A = 199;
  TIMSK1 |= (1 << OCIE1A);

  // Liga el pin 11 al Timer 1
  // Para probar con un ocsiloscopio
  pinMode(11, OUTPUT);
  TCCR1A |= (1 << COM1A0);
  // Esta parte puede ser eliminada despues de probar

  interrupts();

  // Reduccion por defecto
  switch (Modo_Salida) {
    case RT_BURST:
      Reduccion = 2; // 0.2ms
    break;

    case LEGIBLE:
      Reduccion = Segundos_a_Pulsos(4.0); // 4s
    break;
  }
}

ISR(TIMER1_COMPA_vect) {
  Reductor++;

  if (Reductor == Reduccion) {
    Reductor = 1;

    switch (Modo_Salida) {
      case LEGIBLE:
        Espaciar_salida();

        switch (Modo_Funcionamiento) {
          case PRUEBA_PENDULO:
            Serial.print("Pendulo: ");
            Serial.print(pendulo.count);
            Serial.print("\n");
          break;

          case PRUEBA_MOTOR:
            Serial.print("Brazo: ");
            Serial.print(brazo.count);
            Serial.print("\n");
          break; 
        }
      break;

      case RT_BURST:
        switch (Modo_Funcionamiento) {
          case PRUEBA_PENDULO:
            Lecturas[posicion_libre] = pendulo.count;
          break;

          case PRUEBA_MOTOR:
            Lecturas[posicion_libre] = brazo.count;
          break;

          posicion_libre++; 
          if (posicion_libre == 32) {
            posicion_libre = 0;
            Serial.write((uint8_t*)Lecturas, sizeof(Lecturas)); // Esto seguramente va a ser raro de leer
          }
        }
      break;
    }
  }
}

inline void Ajustar_Reduccion(float segundos) {
  Reduccion = Segundos_a_Pulsos(segundos);
}