void Pendulo_Movimiento() {
  
  if (digitalRead(pendulo.B) == HIGH) {  // Puede ser optimizado con registros
    pendulo.count++;
  } else {
    pendulo.count--;
  };

  cambio = 1;
}

void Pendulo_Referencia() {
  pendulo.count = 0;
}