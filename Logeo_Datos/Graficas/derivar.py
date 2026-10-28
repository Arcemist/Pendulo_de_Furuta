import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks
import numpy as np


# Traer los datos
df = pd.read_csv("arduino_data.csv")

# Conversion de pulsos del encoder a grados
df['Pendulo_grados'] = df['Pendulo'] * (360 / 1024)
# Y desplazamiento para que quede centrado
df['Pendulo_grados'] = df['Pendulo_grados'] - 180

dt = 0.2 / 1000

df["Milisegundos_desde_inicio"] = df.index * 0.2

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

indices_picos, _ = find_peaks(df['Posicion'], prominence=10)

tiempos_picos = df['Milisegundos_desde_inicio'].iloc[indices_picos[:5]].values

periodos = np.diff(tiempos_picos)

periodo_promedio = np.mean(periodos)

# Verificar que el filtro no cambia mucho
# la posicion inicial antes de derivar
graf_verificacion = df.plot.line(
    y=['Pendulo_grados', 'Posicion'],
    x='Milisegundos_desde_inicio',
    yticks = [90, 0, -90],
    xlabel = 'Milisegundos',
    ylabel = 'Grados',
    title = 'Verificacion'
)

graf_primeros_picos = df.plot.line(
    y='Posicion',
    x='Milisegundos_desde_inicio',
    yticks = [90, 45, 0, -45, -90],
    xlim = [0, tiempos_picos[-1] + 40],
    grid = True,
    xlabel = 'Milisegundos',
    ylabel = 'Grados',
    title = "Primeros 5 picos"
)
graf_primeros_picos.scatter(
    tiempos_picos,
    df['Posicion'].iloc[indices_picos[:5]],
    color = 'green',
    zorder = 5,
    label = 'Primeros 5 picos'
)
graf_primeros_picos.legend()

for i in range(4):
    x_inicio = tiempos_picos[i]
    x_final = tiempos_picos[i+1]

    color = "yellow" if i % 2 == 0 else "orange"

    graf_primeros_picos.axvspan(
        x_inicio,
        x_final,
        color = color,
        alpha = 0.2
    )


    longitud_x = x_final - x_inicio
    posicion = x_inicio + (longitud_x / 2)
    texto = f"ΔT: {longitud_x:.1f}ms"

    graf_primeros_picos.text(
        posicion,
        df['Posicion'].iloc[indices_picos[i]],
        texto,
        ha = "center",
        va = "center",
        fontsize = 9,
        weight = "bold",
        bbox=dict(facecolor="white", alpha=0.0, edgecolor="none") # con alpha en 0 no aparece
    )



graf_velocidad = df.plot.line(
    y='Velocidad',
    x='Milisegundos_desde_inicio',
    xlim = [0, tiempos_picos[-1] + 40], # Temporal
    xlabel = 'Milisegundos',
    ylabel = 'Deg / S',
    title = "Velocidad"
)

graf_aceleracion = df.plot.line(
    y='Aceleracion',
    x='Milisegundos_desde_inicio',
    xlim = [0, tiempos_picos[-1] + 40], # Temporal
    xlabel = 'Milisegundos',
    ylabel = 'Deg / S^2',
    title = "Aceleracion"
)

plt.show()

print(periodos)
