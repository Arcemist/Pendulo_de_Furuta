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

  while (false) {
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

char Comando;
void loop() {
  if (Serial.available() > 0) {
    String lectura_serial = Serial.readStringUntil('\n');
    
    float argumento = lectura_serial.substring(1).toFloat();

    Comando = lectura_serial[0];

    switch (Comando) {
      case 'E':
        Encender_Motor();
      break;
      
      case 'A':
        Apagar_Motor();
      break;

      case 'P':
        Encender_Motor();
        delay(argumento * 1000.0);
        Apagar_Motor();
      break;

      case 'D':
        Motor_Derecha();
      break;

      case 'I':
        Motor_Izquierda();
      break;

      case 'V':
        Configurar_Duty_Cycle(argumento);
      break;

      case 'T':
        Ajustar_Reduccion(argumento);
      break;

      default:
        Serial.println("Se ha ingresado un commando invalido");
    }
  }
}