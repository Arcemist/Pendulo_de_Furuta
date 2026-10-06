import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Traer los datos
df = pd.read_csv("arduino_data.csv")
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Conversion de pulsos del encoder a grados
df['Pendulo_grados'] = df['Pendulo'] * (360 / 1024)

# Y desplazamiento para que quede centrado
df['Pendulo_grados'] = df['Pendulo_grados'] - 180

# Intento de hacer tiempo desde inicio
df['Delta_Tiempo'] = pd.to_timedelta(df['Timestamp'] - df['Timestamp'][0])
df['Segundos_desde_inicio'] = df['Delta_Tiempo'].dt.total_seconds()

# Definicion del array de deltas en el tiempo
# Sorpresivamente importante para que las derivadas no sean 10^-6 veces mas chicas
dt = df['Delta_Tiempo'] / np.timedelta64(1, 's')

# Calculo de la derivada del angulo y su subsecuente filtrado
df['Velocidad'] = np.gradient(df['Pendulo_grados'], dt)
df['Velocidad'] = df['Velocidad'].rolling(
    window=25, center=True
).mean()

# Calculo de la derivada de la velocidad filtrada y su posterior filtrado
# Necesita calcularse con la velocidad ya filtrada y ser filtrado devuelta
# Almenos con este tipo de filtro
df['Aceleracion'] = np.gradient(df['Velocidad'], dt)
df['Aceleracion'] = df['Aceleracion'].rolling(
    window=25, center=True
).mean()

# Ploteado de los resultados
df.plot.line(
    y=[
        'Pendulo_grados',
        'Velocidad',
        'Aceleracion'
    ],
    x='Segundos_desde_inicio'
)
plt.show()

