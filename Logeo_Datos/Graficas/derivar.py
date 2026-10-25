import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks

# Traer los datos
df = pd.read_csv("arduino_data.csv")
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Conversion de pulsos del encoder a grados
df['Pendulo_grados'] = df['Pendulo'] * (360 / 1024)
# Y desplazamiento para que quede centrado
df['Pendulo_grados'] = df['Pendulo_grados'] - 180

# Intento de hacer tiempo desde inicio
df['Segundos_desde_inicio'] = pd.to_timedelta( df['Timestamp'] - df['Timestamp'][0] ).dt.total_seconds()
dt = np.mean( np.diff( df['Segundos_desde_inicio'].values ) )

# Filtrado de la posicion
df['Posicion'] = savgol_filter(
    df['Pendulo_grados'],
    window_length=31,
    polyorder=3,
    deriv=0,
)

# Calculo y filtrado de la Velocidad
df['Velocidad'] = savgol_filter(
    df['Pendulo_grados'],
    window_length=31,
    polyorder=3,
    deriv=1,
    delta=dt
)

# Calculo y filtrado de la Aceleracion
df['Aceleracion'] = savgol_filter(
    df['Pendulo_grados'],
    window_length=71,
    polyorder=3,
    deriv=2,
    delta=dt
)

# Ploteado de los resultados
df.plot.line(
    y=[
        'Posicion',
        'Velocidad',
        'Aceleracion'
    ],
    x='Segundos_desde_inicio'
)
plt.show()
