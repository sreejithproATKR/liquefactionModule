import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# Load the Excel file
data = pd.read_excel('Ishihara Yoshamine Curves.xlsx', engine='openpyxl')

# Extract the data sets
sets = []
for i in range(7):
    x = data.iloc[2:, 2 * i].dropna().values
    y = data.iloc[2:, 2 * i + 1].dropna().values
    sets.append((x, y))

# Define fitting function for 6th order polynomial
def polynomial_6th_order(x, *coeffs):
    return sum(c * x ** i for i, c in enumerate(coeffs))

# Perform 6th order polynomial fitting for first 4 sets and generate equations
equations = []
for i in range(4):
    x, y = sets[i]
    coeffs, _ = curve_fit(polynomial_6th_order, x, y, p0=[1] * 7)
    equation = " + ".join([f"{coeff:.6f}*x^{i}" for i, coeff in enumerate(coeffs)])
    equations.append(f"Set {i+1}: y = {equation}")

# Print the equations
for eq in equations:
    print(eq)