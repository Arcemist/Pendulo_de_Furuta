void Brazo_Movimiento() {
  
 if (digitalRead(brazo.B) == HIGH) { // Puede ser optimizado con registros
    brazo.count++;
  } else {
    brazo.count--;
  };

  cambio = 1;
}

void Brazo_Referencia() {
  brazo.count = 0;
}