import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.special import ellipk
from scipy.signal import find_peaks

# ==========================================
# 1. PARÁMETROS FÍSICOS Y CONSTANTES
# ==========================================
m2 = 0.0992       # Masa del péndulo [kg]
L2 = 0.136        # Distancia al CM / Longitud [m]
J2 = 2.24e-3      # Momento de inercia J2 [kg*m^2]
g = 9.81          # Aceleración de la gravedad [m/s^2]

K = (m2 * g * L2) / J2
theta0_deg = 90.0
theta0_rad = np.radians(theta0_deg)
omega0 = 0.0

# ==========================================
# 2. CÁLCULO ANALÍTICO / TEÓRICO EXACTO
# ==========================================
# Período lineal (aproximación pequeñas oscilaciones)
T_lineal = 2 * np.pi / np.sqrt(K)

# Período exacto no lineal (Integral Elíptica)
k_param = np.sin(theta0_rad / 2)**2
T_exacto = 4 * np.sqrt(J2 / (m2 * g * L2)) * ellipk(k_param)
f_exacta = 1 / T_exacto

# Valores cinemáticos máximos teóricos
v_max_teo = np.sqrt(2 * K * (1 - np.cos(theta0_rad)))  # [rad/s]
a_max_teo = K * np.sin(theta0_rad)                     # [rad/s^2]

# ==========================================
# 3. SIMULACIÓN NUMÉRICA (EDO)
# ==========================================
def pendulo_edo(t, y):
    theta, omega = y
    dtheta_dt = omega
    domega_dt = K * np.sin(theta)
    return [dtheta_dt, domega_dt]

t_span = (0, 20)
t_eval = np.linspace(0, 20, 10000)
sol = solve_ivp(pendulo_edo, t_span, [theta0_rad, omega0], t_eval=t_eval, rtol=1e-9, atol=1e-9)

t = sol.t
theta_rad = sol.y[0]
omega_rad = sol.y[1]                  # Velocidad angular [rad/s]
alpha_rad = K * np.sin(theta_rad)     # Aceleración angular [rad/s^2]

# Conversión a grados para visualización
theta_deg = np.degrees(theta_rad)
omega_deg = np.degrees(omega_rad)
alpha_deg = np.degrees(alpha_rad)

# ==========================================
# 4. EXTRACCIÓN NUMÉRICA DE PARÁMETROS
# ==========================================
picos, _ = find_peaks(theta_rad, distance=100)
tiempos_picos = t[picos]
periodos_inter_picos = np.diff(tiempos_picos)

T_num_promedio = np.mean(periodos_inter_picos)
f_num_promedio = 1 / T_num_promedio

# ==========================================
# 5. REPORTE EN CONSOLA (REPALDO MATEMÁTICO)
# ==========================================
print("==================================================")
print("     REPORTE DE PARÁMETROS TEÓRICOS DEL PÉNDULO   ")
print("==================================================")
print(f"Constante K = (m2*g*L2)/J2:      {K:.4f} s^-2")
print(f"Ángulo Inicial (theta_0):         {theta0_deg:.2f}° ({theta0_rad:.4f} rad)")
print("--------------------------------------------------")
print("1. PROPIEDADES FRECUENCIALES / TEMPORALES:")
print(f"   - Período Exacto (Analítico): {T_exacto:.4f} s")
print(f"   - Período Numérico Simulado:  {T_num_promedio:.4f} s")
print(f"   - Período Lineal (Ref):       {T_lineal:.4f} s")
print(f"   - Frecuencia Natural Exacta:  {f_exacta:.4f} Hz")
print("--------------------------------------------------")
print("2. VALORES CINEMÁTICOS MÁXIMOS:")
print(f"   - Amplitud Máxima:            {theta0_deg:.2f}° ({theta0_rad:.4f} rad)")
print(f"   - Velocidad Angular Máx:      {np.degrees(v_max_teo):.2f}°/s ({v_max_teo:.4f} rad/s)")
print(f"   - Aceleración Angular Máx:    {np.degrees(a_max_teo):.2f}°/s² ({a_max_teo:.4f} rad/s²)")
print("==================================================")

# ==========================================
# 6. GENERACIÓN DE LAS 3 GRÁFICAS
# ==========================================
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True, dpi=120)

# Grafico 1: Posición Angular
ax1.plot(t, theta_deg, 'b-', linewidth=1.5, label=r'$\theta_2(t)$ Posición')
ax1.plot(tiempos_picos, theta_deg[picos], 'ro', markersize=4, label='Máximos (Picos)')
ax1.set_ylabel(r'Posición [$\circ$]')
ax1.set_title('Respuesta Teórica Ideal del Péndulo Libre ($100\%$ Conservativo)')
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(loc='upper right')

# Grafico 2: Velocidad Angular
ax2.plot(t, omega_deg, 'g-', linewidth=1.5, label=r'$\dot{\theta}_2(t)$ Velocidad')
ax2.axhline(np.degrees(v_max_teo), color='r', linestyle=':', alpha=0.7, label=r'$+\dot{\theta}_{max}$')
ax2.axhline(-np.degrees(v_max_teo), color='r', linestyle=':', alpha=0.7, label=r'$-\dot{\theta}_{max}$')
ax2.set_ylabel(r'Vel. Angular [$\circ/s$]')
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.legend(loc='upper right')

# Grafico 3: Aceleración Angular
ax3.plot(t, alpha_deg, 'm-', linewidth=1.5, label=r'$\ddot{\theta}_2(t)$ Aceleración')
ax3.set_xlabel('Tiempo [s]')
ax3.set_ylabel(r'Acel. Angular [$\circ/s^2$]')
ax3.grid(True, linestyle='--', alpha=0.6)
ax3.legend(loc='upper right')

plt.xlim(0, 10)  # Mostramos los primeros 10s para una mejor apreciación
plt.tight_layout()
plt.show()
