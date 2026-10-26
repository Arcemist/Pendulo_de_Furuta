inline float Segundos_a_Pulsos(float segundos) {
  /* DISCLAIMER:
  El redondeo puede generar un error pequeño en el timing
  Pero este error sera del orden de los 0.01ms por lo que
  no se considera relevante.
  */
  if (segundos < 0.001) { segundos = 0.001; };
  return floor( segundos * 10000.0 );
}

inline float Pulsos_a_Segundos(float pulsos) {
  /* Detalle:
  Esta funcion retorna el valor en segundos redondeado
  a el segundo decimal.  
  */
  return floor( pulsos / 100.0 ) / 100.0;
}

inline void Espaciar_salida() {
  Serial.print("\n\n\n\n\n\n\n\n\n\n");
}