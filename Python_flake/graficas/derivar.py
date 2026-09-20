import numpy as np
import pandas as pd

# 1. Cargar el archivo CSV
# Reemplaza 'tus_datos.csv' con la ruta de tu archivo
df = pd.read_csv("arduino_data.csv")#, parse_dates=["Timestamp"])

# Asegúrate de ordenar por tiempo si los datos no vienen en orden secuencial
df = df.sort_values(by="Timestamp").reset_index(drop=True)

# 2. Extraer las columnas de tiempo y la variable a derivar
t = df["Timestamp"].values
y = df["Pendulo"].values

# 3. Calcular los diferenciales (delas) correlativos: t[i+1] - t[i] e y[i+1] - y[i]
#dt = np.diff(t)
#dy = np.diff(y)

# 4. Calcular la derivada (razón de cambio dy/dt)
# Esto devolverá un arreglo con un elemento menos que el original (N-1)
#derivada_atras = dy / dt

# 5. Alinear el tamaño de los datos para guardarlos en el DataFrame original
# Usamos np.gradient para mantener el mismo tamaño (N) mediante diferencias centrales
# donde es posible, e interpolación en los extremos.
df["derivada_exacta"] = np.gradient(y, t)

# Opcional: Si prefieres la aproximación por diferencias hacia atrás estricta (tamaño N),
# agregamos un NaN o un cero al inicio para rellenar el primer registro:
##df["derivada_diferencias"] = np.insert(derivada_atras, 0, np.nan)

# 6. Guardar el resultado en un nuevo archivo CSV
df.to_csv("datos_con_derivada.csv", index=False)

print("Cálculo completado. Resumen de los datos:")
print(df.head())
