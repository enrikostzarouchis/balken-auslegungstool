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
lastfall = st.selectbox("Lastfall", ["Streckenlast", "Einzellast", "Kragarm Streckenlast", "Kragarm Einzellast", "Einzlelast beliebige Position", "Kombination Streckenlast + Einzellast Mitte", "Streckenlast + Einzellast beliebige Position","Zwei Einzellasten","Kragarm mit Streckenlast + Einzellast am freien Ende"])
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
elif lastfall == "Streckenlast + Einzellast beliebige Position":
    q = st.number_input("Streckenlast q [N/m]", value=10000.0)
    F = st.number_input("Einzellast F [N]", value=50000.0)
    a = st.slider("Position der Last [m]", min_value=0.01, max_value=L-0.01, value=L/2)
elif lastfall == "Zwei Einzellasten":
    F1 = st.number_input("Einzellast F1 [N]", value=50000.0)
    F2 = st.number_input("Einzellast F2 [N]", value=50000.0)
    a1 = st.slider("Position der Last 1 [m]", min_value=0.01, max_value=L-0.01, value=L/2)
    a2 = st.slider("Position der Last 2 [m]", min_value=0.01, max_value=L-0.01, value=L/2)
    q = 0
elif lastfall == "Kragarm mit Streckenlast + Einzellast am freien Ende":
    q = st.number_input("Streckenlast q [N/m]", value=10000.0)
    F = st.number_input("Einzellast F [N]", value=50000.0)
    a = 0
else:
    F = st.number_input("Einzellast F [N]", value=50000.0)
    q = 0
    a = 0

st.subheader("Querschnitt & Material")

# Dicitonairies
ipe_profile = {
    "IPE 100": {"W": 34.2e-6, "I": 171e-8, "A": 10.3e-4},
    "IPE 120": {"W": 53.0e-6, "I": 318e-8, "A": 13.2e-4},
    "IPE 140": {"W": 77.3e-6, "I": 541e-8, "A": 16.4e-4},
    "IPE 160": {"W": 123.0e-6, "I": 869e-8, "A": 20.1e-4},
    "IPE 180": {"W": 166.0e-6, "I": 1320e-8, "A": 23.9e-4},
    "IPE 200": {"W": 194.0e-6, "I": 1940e-8, "A": 28.5e-4},
    "IPE 220": {"W": 252.0e-6, "I": 2770e-8, "A": 33.4e-4},
    "IPE 240": {"W": 324.0e-6, "I": 3890e-8, "A": 39.1e-4},
    "IPE 300": {"W": 557.0e-6, "I": 8630e-8, "A": 53.8e-4},
}

hea_profile = {
    "HEA 100": {"W": 72.8e-6, "I": 349e-8, "A": 21.2e-4},
    "HEA 120": {"W": 106e-6, "I": 606e-8, "A": 25.3e-4},
    "HEA 140": {"W": 155e-6, "I": 1033e-8, "A": 31.4e-4},
    "HEA 160": {"W": 220e-6, "I": 1673e-8, "A": 38.8e-4},
    "HEA 180": {"W": 294e-6, "I": 2510e-8, "A": 45.3e-4},
    "HEA 200": {"W": 389e-6, "I": 3692e-8, "A": 53.8e-4},
    "HEA 220": {"W": 515e-6, "I": 5410e-8, "A": 64.3e-4},
    "HEA 240": {"W": 675e-6, "I": 7763e-8, "A": 76.8e-4},
    "HEA 300": {"W": 1260e-6, "I": 18260e-8, "A": 112.5e-4},
}

heb_profile = {
    "HEB 100": {"W": 90e-6, "I": 450e-8, "A": 26.0e-4},
    "HEB 120": {"W": 144e-6, "I": 864e-8, "A": 34.0e-4},
    "HEB 140": {"W": 216e-6, "I": 1510e-8, "A": 43.0e-4},
    "HEB 160": {"W": 311e-6, "I": 2490e-8, "A": 54.3e-4},
    "HEB 180": {"W": 426e-6, "I": 3830e-8, "A": 65.3e-4},
    "HEB 200": {"W": 570e-6, "I": 5700e-8, "A": 78.1e-4},
    "HEB 220": {"W": 736e-6, "I": 8090e-8, "A": 91.0e-4},
    "HEB 240": {"W": 938e-6, "I": 11260e-8, "A": 106e-4},
    "HEB 300": {"W": 1680e-6, "I": 25170e-8, "A": 149e-4},
}

werkstoffe = {
    "S235": 235e6,
    "S355": 355e6,
    "S460": 460e6,
    "Alu":  270e6,
    "Edelstahl 1.4301":200e6,
    "Gusseisen": 250e6,
    "Holz C24": 24e6
    
}

e_modul = {
    "S235": 210e9,
    "S355": 210e9,
    "S460": 210e9,
    "Alu":  70e9,
    "Edelstahl 1.4301":200e9,
    "Gusseisen": 110e9,
    "Holz C24": 11e9
}

dichte = {
    "S235": 7850,
    "S355": 7850,
    "S460": 7850,
    "Alu": 2700,
    "Edelstahl 1.4301":8000,
    "Gusseisen": 7200,
    "Holz C24": 420
}

# Selectboxen
profil_wahl = st.selectbox("Querschnitt", ["Eigener Querschnitt", "Kreisquerschnitt"] + list(ipe_profile.keys()) + list(hea_profile.keys()) + list(heb_profile.keys()))
material = st.selectbox("Material", ["S235", "S355", "S460", "Alu", "Edelstahl 1.4301", "Gusseisen", "Holz C24"])

if profil_wahl == "Eigener Querschnitt":
    col1, col2 = st.columns(2)
    with col1:
        b = st.number_input("Breite b [m]", value=0.05)
    with col2:
        h = st.number_input("Höhe h [m]", value=0.1)
    W = (b * h**2) / 6
    I = (b * h**3) / 12
    A = b*h

elif profil_wahl == "Kreisquerschnitt":
    d = st.number_input("Durchmesser d [m]", value=0.05)
    W = (np.pi*d**3)/32
    I = (np.pi*d**4)/64
    A = (np.pi*d**2)/4

elif profil_wahl in hea_profile:
    W = hea_profile[profil_wahl]["W"]
    I = hea_profile[profil_wahl]["I"]
    A = hea_profile[profil_wahl]["A"]

elif profil_wahl in heb_profile:
    W = heb_profile[profil_wahl]["W"]
    I = heb_profile[profil_wahl]["I"]
    A = heb_profile[profil_wahl]["A"]

else:
    W = ipe_profile[profil_wahl]["W"]
    I = ipe_profile[profil_wahl]["I"]
    A = ipe_profile[profil_wahl]["A"]

Re = werkstoffe[material]
E = e_modul[material]

eigenlast_check = st.checkbox("Eigengewicht des Balkens berücksichtigen?")

if eigenlast_check:
    q_eigen = dichte[material] * A * 9.81
else:
    q_eigen = 0

# Berechnung
x = np.linspace(0, L, 200)

if lastfall == "Streckenlast":
    M = (q * x / 2) * (L - x) + (q_eigen * x / 2) * (L - x)
    Q = (q / 2) * (L - 2 * x) + (q_eigen / 2) * (L - 2 * x)
    M_max = np.max(np.abs(M))
    titel = f"Streckenlast (q={q} N/m, L={L} m)"

elif lastfall == "Kragarm Streckenlast":
    M = (q/2) * (L-x)**2 + (q_eigen/2) * (L-x)**2
    Q = q * (L-x) + q_eigen * (L - x)
    M_max = np.max(np.abs(M))
    titel = f"Kragarm Streckenlast (q={q} N/m, L={L} m)"

elif lastfall == "Kragarm Einzellast":
    M = F * (L - x) + (q_eigen/2) * (L-x)**2
    Q = np.full(200, F) + q_eigen * (L - x)
    M_max = np.max(np.abs(M))
    titel = f"Kragarm Einzellast (F={F} N, L={L} m)"

elif lastfall == "Einzellast beliebige Position":
    R_A = F*(L - a) / L
    R_B = F * a / L
    M = np.where(x <= a, R_A*x, R_B*(L - x)) + (q_eigen * x / 2) * (L - x)
    Q = np.where(x <= a, R_A, -R_B) + (q_eigen / 2) * (L - 2 * x)
    M_max = np.max(np.abs(M))
    titel = f"Einzellast beliebige Position (F={F} N, L={L} m)"

elif lastfall == "Kombination Streckenlast + Einzellast Mitte":
    M_strecke = (q * x / 2) * (L - x) + (q_eigen * x / 2) * (L - x)
    M_einzel = np.where(x <= L/2, (F/2) * x, (F/2) * (L - x))
    M = M_strecke + M_einzel
    Q_strecke = (q / 2) * (L - 2 * x) + (q_eigen / 2) * (L - 2 * x)
    Q_einzel = np.where(x <= L/2, F/2, -F/2)
    Q = Q_strecke + Q_einzel
    M_max = np.max(np.abs(M))
    titel = f"Kombination Streckenlast + Einzellast Mitte (q={q} N/m, F={F} N, L={L} m)"
    
elif lastfall == "Streckenlast + Einzellast beliebige Position":
    R_A = F*(L - a) / L
    R_B = F * a / L
    M_einzel = np.where(x <= a, R_A*x, R_B*(L - x))
    M_strecke = (q * x / 2) * (L - x) + (q_eigen * x / 2) * (L - x)
    M = M_strecke + M_einzel
    Q_einzel= np.where(x <= a, R_A, -R_B)
    Q_strecke = (q / 2) * (L - 2 * x) + (q_eigen / 2) * (L - 2 * x)
    Q = Q_strecke + Q_einzel
    M_max = np.max(np.abs(M))
    titel = f"Streckenlast + Einzellast beliebige Position (q={q} N/m, F={F} N, L={L} m)"
    
elif lastfall == "Zwei Einzellasten":
    R_A = F1*(L - a1)/L + F2*(L - a2)/L
    R_B = F1*a1/L + F2*a2/L
    if a1 <= a2:
      a_klein, F_klein = a1, F1
      a_gross, F_gross = a2, F2
    else:
      a_klein, F_klein = a2, F2
      a_gross, F_gross = a1, F1
    M = np.where(x <= a_klein, R_A * x, np.where(x <= a_gross, R_A*x - F_klein*(x - a_klein), R_B*(L - x)))+ (q_eigen * x / 2) * (L - x)
    Q = np.where(x <= a_klein, R_A, np.where(x <= a_gross, R_A-F_klein, -R_B))+ (q_eigen / 2) * (L - 2 * x)
    M_max = np.max(np.abs(M))
    titel = f"Zwei Einzellasten (F1={F1} N bei {a1} m, F2={F2} N bei {a2} m, L={L} m)"

elif lastfall == "Kragarm mit Streckenlast + Einzellast am freien Ende":
    M_strecke = (q/2) * (L-x)**2 + (q_eigen/2) * (L-x)**2
    M_einzel = F * (L-x)
    M = M_strecke + M_einzel
    Q_strecke = q * (L-x) + q_eigen * (L - x)
    Q_einzel = np.full(200, F)
    Q = Q_strecke + Q_einzel
    M_max = np.max(np.abs(M))
    titel = f"Kragarm mit Streckenlast + Einzellast am freien Ende (q={q} N/m, F={F} N, L={L} m)"
    
else:
    M = np.where(x <= L/2, (F/2) * x, (F/2) * (L - x)) + (q_eigen * x / 2) * (L - x)
    Q = np.where(x <= L/2, F/2, -F/2) + (q_eigen / 2) * (L - 2 * x)
    M_max = np.max(np.abs(M))
    titel = f"Einzellast (F={F} N, L={L} m)"


sigma = M_max / W
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
    f_max = (5 * q * L**4) / (384 * E * I) + (F * L**3) / (48 * E * I)
elif lastfall == "Streckenlast + Einzellast beliebige Position":
    f_max = (F * a * (L-a) * (L+a)) / (6 * E * I * L)+(5 * q * L**4) / (384 * E * I)
elif lastfall == "Zwei Einzellasten":
    f_max_F1 = (F1 * a1 * (L-a1) * (L+a1)) / (6 * E * I * L)
    f_max_F2 = (F2 * a2 * (L-a2) * (L+a2)) / (6 * E * I * L)
    f_max = f_max_F1 + f_max_F2
elif lastfall == "Kragarm mit Streckenlast + Einzellast am freien Ende":
    f_max = (q * L**4) / (8 * E * I)+ (F * L**3) / (3 * E * I)

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