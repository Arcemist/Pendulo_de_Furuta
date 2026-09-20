import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# ============================================================
# PARÁMETROS
# ============================================================

m2 = 0.0992          # kg
l2 = 0.13            # m
J2 = 2.24e-3         # kg*m^2
g = 9.81             # m/s^2

# Constante del sistema
K = m2 * g * l2 / J2

print(f"K = {K:.4f} rad/s²")

# ============================================================
# CONDICIONES INICIALES
# ============================================================

theta0 = np.deg2rad(90)   # 90°
omega0 = 0.0              # rad/s

x0 = [theta0, omega0]

# ============================================================
# ECUACIÓN DIFERENCIAL
# ============================================================

def pendulo(t, x):

    theta = x[0]
    omega = x[1]

    dtheta_dt = omega
    domega_dt = K * np.sin(theta)

    return [dtheta_dt, domega_dt]

# ============================================================
# SIMULACIÓN DE 20 SEGUNDOS
# ============================================================

t_inicio = 0
t_final = 20

t_eval = np.linspace(t_inicio, t_final, 10000)

sol = solve_ivp(
    pendulo,
    [t_inicio, t_final],
    x0,
    t_eval=t_eval,
    rtol=1e-9,
    atol=1e-11
)

# ============================================================
# RESULTADOS
# ============================================================

t = sol.t

theta = sol.y[0]       # Posición angular [rad]
omega = sol.y[1]       # Velocidad angular [rad/s]

# Aceleración angular
alpha = K * np.sin(theta)  # [rad/s²]

# ============================================================
# CONVERSIONES
# ============================================================

theta_deg = np.rad2deg(theta)  # Posición [°]

omega_deg = np.rad2deg(omega)  # Velocidad [°/s]

alpha_deg = np.rad2deg(alpha)  # Aceleración [°/s²]

# ============================================================
# GRÁFICAS
# ============================================================

fig, axs = plt.subplots(3, 1, figsize=(12, 10))

# ------------------------------------------------------------
# 1. POSICIÓN ANGULAR
# ------------------------------------------------------------

axs[0].plot(t, theta_deg)

axs[0].set_xlabel("Tiempo [s]")
axs[0].set_ylabel(r"$\theta_2$ [°]")
axs[0].set_title("Posición angular del péndulo")

axs[0].grid(True)
axs[0].set_xlim(0, 20)

# ------------------------------------------------------------
# 2. VELOCIDAD ANGULAR
# ------------------------------------------------------------

axs[1].plot(t, omega_deg)

axs[1].set_xlabel("Tiempo [s]")
axs[1].set_ylabel(r"$\dot{\theta}_2$ [°/s]")
axs[1].set_title("Velocidad angular del péndulo")

axs[1].grid(True)
axs[1].set_xlim(0, 20)

# ------------------------------------------------------------
# 3. ACELERACIÓN ANGULAR
# ------------------------------------------------------------

axs[2].plot(t, alpha_deg)

axs[2].set_xlabel("Tiempo [s]")
axs[2].set_ylabel(r"$\ddot{\theta}_2$ [°/s²]")
axs[2].set_title("Aceleración angular del péndulo")

axs[2].grid(True)
axs[2].set_xlim(0, 20)

# Ajustar espacios
plt.tight_layout()

plt.show()
