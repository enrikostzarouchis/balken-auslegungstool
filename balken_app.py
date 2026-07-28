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
lastfall = st.selectbox("Lastfall", ["Streckenlast", "Einzellast", "Kragarm Streckenlast", "Kragarm Einzellast", "Einzellast beliebige Position", "Kombination Streckenlast + Einzellast Mitte"])
L = st.number_input("Balkenlänge L [m]", value=5.0)


if lastfall == "Streckenlast" or lastfall == "Kragarm Streckenlast":
    q = st.number_input("Streckenlast q [N/m]", value=10000.0)
    F = 0
    a = 0
elif lastfall == "Einzellast beliebige Position":
    F = st.number_input("Einzellast F [N]", value=50000.0)
    a = st.slider("Position der Last [m]", min_value=0.01, max_value=L-0.01, value=L/2)
    q = 0
elif lastfall == "Kombination Streckenlast + Einzellast Mitte":
    q = st.number_input("Streckenlast q [N/m]", value=10000.0)
    F = st.number_input("Einzellast F [N]", value=50000.0)
    a = 0
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
    
elif lastfall == "Kombination Streckenlast + Einzellast Mitte":
    M_strecke = (q * x / 2) * (L - x)
    M_einzel = np.where(x <= L/2, (F/2) * x, (F/2) * (L - x))
    M = M_strecke + M_einzel
    Q_strecke = (q / 2) * (L - 2 * x)
    Q_einzel = np.where(x <= L/2, F/2, -F/2)
    Q = Q_strecke + Q_einzel
    M_max = np.max(M)
    titel = f"Kombination (q={q} N/m, F={F} N, L={L} m)"

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

ipe_profile = {
    "IPE 100": {"W": 34.2e-6, "I": 171e-8},
    "IPE 120": {"W": 53.0e-6, "I": 318e-8},
    "IPE 140": {"W": 77.3e-6, "I": 541e-8},
    "IPE 160": {"W": 123.0e-6, "I": 869e-8},
    "IPE 180": {"W": 166.0e-6, "I": 1320e-8},
    "IPE 200": {"W": 194.0e-6, "I": 1940e-8},
    "IPE 220": {"W": 252.0e-6, "I": 2770e-8},
    "IPE 240": {"W": 324.0e-6, "I": 3890e-8},
    "IPE 300": {"W": 557.0e-6, "I": 8630e-8},
}

hea_profile = {
    "HEA 100": {"W": 72.8e-6, "I": 349e-8},
    "HEA 120": {"W": 106e-6, "I": 606e-8},
    "HEA 140": {"W": 155e-6, "I": 1033e-8},
    "HEA 160": {"W": 220e-6, "I": 1673e-8},
    "HEA 180": {"W": 294e-6, "I": 2510e-8},
    "HEA 200": {"W": 389e-6, "I": 3692e-8},
    "HEA 220": {"W": 515e-6, "I": 5410e-8},
    "HEA 240": {"W": 675e-6, "I": 7763e-8},
    "HEA 300": {"W": 1260e-6, "I": 18260e-8},
}

heb_profile = {
    "HEB 100": {"W": 90e-6, "I": 450e-8},
    "HEB 120": {"W": 144e-6, "I": 864e-8},
    "HEB 140": {"W": 216e-6, "I": 1510e-8},
    "HEB 160": {"W": 311e-6, "I": 2490e-8},
    "HEB 180": {"W": 426e-6, "I": 3830e-8},
    "HEB 200": {"W": 570e-6, "I": 5700e-8},
    "HEB 220": {"W": 736e-6, "I": 8090e-8},
    "HEB 240": {"W": 938e-6, "I": 11260e-8},
    "HEB 300": {"W": 1680e-6, "I": 25170e-8},
}

profil_wahl = st.selectbox("Querschnitt", ["Eigener Querschnitt", "Kreisquerschnitt"] + list(ipe_profile.keys()) + list(hea_profile.keys()) + list(heb_profile.keys()))
material = st.selectbox("Material", ["S235", "S355", "Alu"])

if profil_wahl == "Eigener Querschnitt":
    col1, col2 = st.columns(2)
    with col1:
        b = st.number_input("Breite b [m]", value=0.05)
    with col2:
        h = st.number_input("Höhe h [m]", value=0.1)
    W = (b * h**2) / 6
    I = (b * h**3) / 12
    
elif profil_wahl == "Kreisquerschnitt":
    d = st.number_input("Durchmesser d [m]", value = 0.05)
    W = (np.pi*d**3)/32
    I = (np.pi*d**4)/64
    
elif profil_wahl in hea_profile:
    W = hea_profile[profil_wahl]["W"]
    I = hea_profile[profil_wahl]["I"]
    
elif profil_wahl in heb_profile:
    W = heb_profile[profil_wahl]["W"]
    I = heb_profile[profil_wahl]["I"]

else: 
    W = ipe_profile[profil_wahl]["W"]
    I = ipe_profile[profil_wahl]["I"]
    
werkstoffe = {
    "S235": 235e6,
    "S355": 355e6,
    "Alu":  270e6
}

sigma = M_max / W
Re = werkstoffe[material]
e_modul = {
    "S235": 210e9,
    "S355": 210e9,
    "Alu":  70e9
}
E = e_modul[material]
S = Re / sigma

if lastfall == "Streckenlast":
    f_max = (5 * q * L**4) / (384 * E * I)
elif lastfall == "Einzellast":
    f_max = (F * L**3) / (48 * E * I)
elif lastfall == "Einzellast beliebige Position":
    f_max = (F * a * (L-a) * (L+a)) / (6 * E * I * L)
elif lastfall == "Kragarm Streckenlast":
    f_max = (q * L**4) / (8 * E * I)
elif lastfall == "Kragarm Einzellast":
    f_max = (F * L**3) / (3 * E * I)
elif lastfall == "Kombination Streckenlast + Einzellast Mitte":
    f_max = (5 * q * L**4) / (384 * E * I)+(F * L**3) / (48 * E * I)
    
st.write(f"**Maximale Durchbiegung:** {f_max*1000:.2f} mm")

if f_max < L/300:
   st.success("✅ Durchbiegung in Ordnung!")
else:
   st.error("❌ Durchbiegung zu gross — Profil vergrössern!")
    
st.write(f"**Biegespannung:** {sigma/1e6:.2f} MPa")
st.write(f"**Streckgrenze {material}:** {Re/1e6:.0f} MPa")
st.write(f"**Sicherheitsfaktor:** {S:.2f}")

if S >= 2:
    st.success("✅ Auslegung sicher!")
else:
    st.error("❌ Zu gefährlich — Querschnitt vergrößern!")