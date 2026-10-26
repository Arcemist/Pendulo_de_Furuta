/* Seleccion de modo de funcionamiento
La siguiente constante determina el modo en el cual
sera compilado el programa.
*/
enum Modos_Funcionamiento { 
  PRUEBA_PENDULO,
  PRUEBA_MOTOR,
};
const Modos_Funcionamiento
  Modo_Funcionamiento = PRUEBA_MOTOR;

enum Modos_Salida {
  LEGIBLE,
  RT_BURST
};
const Modos_Salida Modo_Salida = LEGIBLE;

void setup() {
  Serial.begin(115200); // Maximo estable

  while (true) {
    if (Serial.available() > 0) {
      char incomingByte = Serial.read();
      if (incomingByte == 'S') {
        break;
      }
    }
  };

  Inicializar_encoders();

  Inicializar_motor();

  Inicializar_telemetria();
}

char Commando;
void loop() {
  if (Serial.available() > 0) {
    const String lectura_serial = Serial.readStringUntil('\n');
    
    Commando = 0x00; // placeholder
    if (isascii( lectura_serial[0] )) {
       Commando = toUpperCase( lectura_serial[0] );
    };

    switch (Commando) {
      case 'E':
        Encender_Motor();
      break;
      
      case 'A':
        Apagar_Motor();
      break;

      case 'P':
        float espera = lectura_serial.substring(2).toFloat();
        Encender_Motor();
        delay(espera * 1000.0);
        Apagar_Motor();
      break;

      case 'D':
        Motor_Derecha();
      break;

      case 'I':
        Motor_Izquierda();
      break;

      case 'V':
        float porcentaje = lectura_serial.substring(2).toFloat();
        Configurar_Duty_Cycle(porcentaje);
      break;

      case 'T':
        float segundos = lectura_serial.substring(2).toFloat();
        Ajustar_Reduccion(segundos);
      break;

      default:
        Serial.println("Se ha ingresado un commando invalido");
    }
  }
}