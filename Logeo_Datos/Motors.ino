/* Informacion:
Este codigo esta tomando en cuenta el uso de
un Puente H dual L298N pero solo se va a utilizar
un motor, ya que nuestra planta solo tiene uno.
*/
struct Motor {
  const int ENA;
  const int IN1;
  const int IN2;
};

/* DISCLAIMER:
Al cambiar los pines mencionados a continuacion
se debe tambien cambiar la configuracion de la 
lectura por registros que esta en las interrupciones
externas mas abajo en este archivo.
*/
struct Motor motor = {
  .ENA = 6,
  .IN1 = 7,
  .IN2 = 8
};

inline void Inicializar_motor() {
  pinMode(motor.ENA, OUTPUT);
  pinMode(motor.IN1, OUTPUT);
  pinMode(motor.IN2, OUTPUT);

  noInterrupts();

  // Supuestamente elige PWM phase correct con TOP ICR
  TCCR4A |= (1 << WGM41);
  TCCR4B |= (1 << WGM43);

  // Poner el preescaler a 1
  TCCR4B |= (1 << CS40);

  /* Seleccionar Frecuencia:
  Frec = (16*10^6) / 2*1*ICR4
  Frec = (8*10^6) / ICR4

  Y por lo tanto con ICR4 en 4000 la frecuencia
  es igual a 2kHz 
  */
  ICR4 = 4000;

  // 50% por defecto
  OCR4A = 2000;

  interrupts();
}

inline void Configurar_Duty_Cycle(float porcentaje) {
  if (porcentaje > 100.0) { porcentaje = 100.0; };
  if (porcentaje < 0.0)   { porcentaje = 0.0; };

  OCR4A = floor ( 4000.0 * (porcentaje / 100.0) );
}

inline void Apagar_Motor() { TCCR4A &= ~(1 << COM4A1); }

inline void Encender_Motor() { TCCR4A |= (1 << COM4A1); } 

// Incheckeado que no esten al revez
inline void Motor_Derecha() {
  PORTH &= (1 << PH5);
  PORTH |= (1 << PH4); 
}

inline void Motor_Izquierda() {
  PORTH &= (1 << PH4);
  PORTH |= (1 << PH5);
}