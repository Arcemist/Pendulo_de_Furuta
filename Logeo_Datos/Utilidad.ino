void Enviar_Valores() {
  Serial.print("\n\n\n\n\n\n\n\n\n\n");

  Serial.print("Pendulo: ");
  Serial.println(pendulo.count);
  Serial.print("Brazo: ");
  Serial.println(brazo.count);
}

const char divisor = ',';
void Enviar_Valores_crudo() {
  Serial.print(pendulo.count);
  Serial.print(divisor);
  Serial.println(brazo.count);
}