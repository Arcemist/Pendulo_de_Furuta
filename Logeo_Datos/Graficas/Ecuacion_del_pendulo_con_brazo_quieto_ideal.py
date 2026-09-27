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

theta = sol.y[0]
omega = sol.y[1]

# Convertir a grados
theta_deg = np.rad2deg(theta)

# ============================================================
# GRÁFICA DEL ÁNGULO
# ============================================================

plt.figure(figsize=(12, 5))

plt.plot(t, theta_deg)

plt.xlabel("Tiempo [s]")
plt.ylabel(r"$\theta_2$ [°]")
plt.title("Movimiento del péndulo durante 20 segundos")

plt.grid(True)

plt.xlim(0, 20)

plt.show()
