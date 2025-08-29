# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

import numpy as np
import matplotlib.pyplot as plt

V = np.array([1.59, 1.7, 2.37])
f = np.array([4.54, 5.08, 6.38])
e = 1.6e-19 #Coulomb
plt.plot(f, V, "o")

a, b = np.polyfit(f, V, 1)
x = np.linspace(min(f), max(f))
g = lambda x: a*x+b
h = a*10**(-15)*e

plt.plot(x, g(x), label=r"$y=ax+b$"+"\n"+f"a={np.round(a,2)}"+"\n"+f"b={np.round(b,2)}")
plt.xlabel("f"+r"[$10^{-14}Hz$]")
plt.ylabel(r"$\Delta V$ [V]")
plt.legend()
plt.title(r"$e\Delta V = h f$")
plt.text(6, 2, f"h={h:.3}"+r"$Js$")