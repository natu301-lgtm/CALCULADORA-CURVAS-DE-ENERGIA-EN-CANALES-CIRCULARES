import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# Configuración visual
st.set_page_config(page_title="Hidráulica - Ingeniería Ambiental", layout="wide")

st.title("🌊 Cálculo de Energía Específica - Sección Circular")
st.markdown("### Datos del ejercicio actual:")

# --- ENTRADA DE DATOS (Ajustados a tu foto) ---
col_in1, col_in2, col_in3 = st.columns(3)
with col_in1:
    d0 = st.number_input("Diámetro (d0) [m]", value=1.50, format="%.3f")
with col_in2:
    Q = st.number_input("Caudal (Q) [m³/s]", value=0.70, format="%.2f")
with col_in3:
    E_target = st.number_input("Energía (E) [m]", value=0.950, format="%.3f")

g = 9.81

# --- FUNCIONES MATEMÁTICAS ---
def area_func(theta, d0):
    return (d0**2 / 8) * (theta - np.sin(theta))

def espejo_func(theta, d0):
    return d0 * np.sin(theta / 2)

def tirante_y(theta, d0):
    return (d0 / 2) * (1 - np.cos(theta / 2))

# --- CÁLCULOS ---
# 1. Hallar Theta Crítico (θc)
def ec_critica(t):
    if t <= 0: return 1e9
    A = area_func(t, d0)
    T = espejo_func(t, d0)
    return (Q**2 * T) / (g * A**3) - 1

theta_c = fsolve(ec_critica, 2.5)[0]
yc = tirante_y(theta_c, d0)
Ac = area_func(theta_c, d0)
Ec = yc + (Q**2 / (2 * g * Ac**2))

# 2. Hallar Tirantes Alternos (y1, y2) para la Energía E_target
def ec_energia(t):
    y = tirante_y(t, d0)
    A = area_func(t, d0)
    if A <= 0: return 1e9
    return y + (Q**2 / (2 * g * A**2)) - E_target

# Buscamos en las dos ramas de la curva
theta1 = fsolve(ec_energia, 1.5)[0] # Rama supercrítica
y1 = tirante_y(theta1, d0)

theta2 = fsolve(ec_energia, 3.5)[0] # Rama subcrítica
y2 = tirante_y(theta2, d0)

# --- MOSTRAR RESULTADOS ---
st.divider()
res1, res2 = st.columns([1, 2])

with res1:
    st.subheader("📋 Resultados del Cálculo")
    st.write(f"**Ángulo Crítico (θc):** `{theta_c:.4f} rad`")
    st.success(f"**Tirante Crítico (yc):** `{yc:.4f} m` ✅")
    st.write(f"**Energía Mínima (Ec):** `{Ec:.4f} m`")
    
    st.divider()
    st.write(f"**Para E = {E_target} m:**")
    st.info(f"**y₁ (Rápido):** {y1:.4f} m")
    st.info(f"**y₂ (Lento):** {y2:.4f} m")

with res2:
    # Generar Curva
    t_vals = np.linspace(0.5, 5.8, 500)
    y_vals = tirante_y(t_vals, d0)
    E_vals = y_vals + (Q**2 / (2 * g * area_func(t_vals, d0)**2))
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(E_vals, y_vals, label="Curva de Energía (C)", color="blue", lw=2)
    ax.axvline(E_target, color="red", linestyle="--", label=f"E = {E_target}m")
    
    # Puntos clave
    ax.scatter([Ec], [yc], color="black", s=50, label=f"Crítico (yc={yc:.3f})")
    ax.scatter([E_target, E_target], [y1, y2], color="green", s=50, label="Tirantes Alternos")
    
    ax.set_xlabel("Energía E específica [m]")
    ax.set_ylabel("Tirante y [m]")
    ax.set_xlim(Ec * 0.9, E_target * 1.3)
    ax.set_ylim(0, d0 * 0.8)
    ax.grid(True, which='both', linestyle='--', alpha=0.5)
    ax.legend()
    st.pyplot(fig)
