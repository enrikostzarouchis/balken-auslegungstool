# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 18:14:18 2026

@author: hhh289
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🔧 Balken-Auslegungstool")

# Eingabefelder
lastfall = st.selectbox("Lastfall", ["Streckenlast", "Einzellast", "Kragarm Streckenlast", "Kragarm Einzellast", "Einzellast beliebige Position"])
L = st.number_input("Balkenlänge L [m]", value=5.0)


if lastfall == "Streckenlast" or lastfall == "Kragarm Streckenlast":
    q = st.number_input("Streckenlast q [N/m]", value=10000.0)
    F = 0
    a = 0
elif lastfall == "Einzellast beliebige Position":
    F = st.number_input("Einzellast F [N]", value=50000.0)
    a = a = st.slider("Position der Last [m]", min_value=0.01, max_value=L-0.01, value=L/2)
    q = 0
else:
    F = st.number_input("Einzellast F [N]", value=50000.0)
    q = 0
    a = 0
    
# Berechnung
x = np.linspace(0, L, 200)

if lastfall == "Streckenlast":
    M = (q * x / 2) * (L - x)
    Q = (q / 2) * (L - 2 * x)
    M_max = (q * L**2) / 8
    
elif lastfall == "Kragarm Streckenlast":
    M = (q/2) * (L-x)**2 
    Q = q * (L-x)
    M_max = (q * L**2) / 2
    titel = f"Kragarm Streckenlast (q={q} N/m, L={L} m)"
    
elif lastfall == "Kragarm Einzellast":
    M = F * (L - x)
    Q = np.full(200, F)
    M_max = F*L
    titel = f"Kragarm Einzellast (F={F} N, L={L} m)"

elif lastfall == "Einzellast beliebige Position":
    A = F*(L - a) /L
    B = F * a /L
    M = np.where(x <= a, A*x, B*(L - x))
    Q = np.where(x <= a, A, -B)
    M_max = F*a*(L-a) /L
    titel = f"Einzellast beliebige Position (F={F} N, L={L} m)"

else:
    M = np.where(x <= L/2, (F/2) * x, (F/2) * (L - x))
    Q = np.where(x <= L/2, F/2, -F/2)
    M_max = (F * L) / 4

# Diagramme
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 5))

ax1.plot(x, M, color="blue")
ax1.set_ylabel("Biegemoment [Nm]")
ax1.set_title("Biegemomentenlinie")
ax1.grid(True)

ax2.plot(x, Q, color="red")
ax2.set_xlabel("Position [m]")
ax2.set_ylabel("Querkraft [N]")
ax2.set_title("Querkraftverlauf")
ax2.grid(True)

plt.tight_layout()
st.pyplot(fig)

st.write(f"**Maximales Biegemoment:** {M_max:.2f} Nm")

st.subheader("Querschnitt & Material")

col1, col2 = st.columns(2)
with col1:
    b = st.number_input("Breite b [m]", value=0.05)
with col2:
    h = st.number_input("Höhe h [m]", value=0.1)

material = st.selectbox("Material", ["S235", "S355", "Alu"])

werkstoffe = {
    "S235": 235e6,
    "S355": 355e6,
    "Alu":  270e6
}

W = (b * h**2) / 6
sigma = M_max / W
Re = werkstoffe[material]
S = Re / sigma

st.write(f"**Biegespannung:** {sigma/1e6:.2f} MPa")
st.write(f"**Streckgrenze {material}:** {Re/1e6:.0f} MPa")
st.write(f"**Sicherheitsfaktor:** {S:.2f}")

if S >= 2:
    st.success("✅ Auslegung sicher!")
else:
    st.error("❌ Zu gefährlich — Querschnitt vergrößern!")