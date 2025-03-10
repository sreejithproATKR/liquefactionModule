import numpy as np
from scipy.optimize import fsolve


# Define the equations for each set of curves
def curve_set_1(x, y):
    return 1.829636 + (-5.541204 * x) + (17.662387 * x ** 2) + (-33.533314 * x ** 3) + (34.157882 * x ** 4) + (
                -17.305186 * x ** 5) + (3.377813 * x ** 6) - y


def curve_set_2(x, y):
    return 1.859296 + (-3.870802 * x) + (7.557173 * x ** 2) + (-7.672841 * x ** 3) + (3.382194 * x ** 4) + (
                -0.272989 * x ** 5) + (-0.135060 * x ** 6) - y


def curve_set_3(x, y):
    return 1.841110 + (-3.148252 * x) + (5.129643 * x ** 2) + (-4.206087 * x ** 3) + (1.482850 * x ** 4) + (
                -0.087245 * x ** 5) + (-0.040607 * x ** 6) - y


def curve_set_4(x, y):
    return 1.853302 + (-2.394398 * x) + (2.802242 * x ** 2) + (-1.661380 * x ** 3) + (0.449340 * x ** 4) + (
                -0.031075 * x ** 5) + (-0.004449 * x ** 6) - y


def curve_set_5(x, y):
    return 0.914434 + (1.98353 / (1 + 4 * ((x + 0.3559) / 0.735229) ** 2)) - y


def curve_set_6(x, y):
     return 0.956739 + (0.13328 / (1 + 4 * ((x -0.6841) /1.47243) ^ 2)) - y


def curve_set_7(x, y):
    return -0.0056243 * x + 1.010753 - y


# Dictionary to map Dr values to corresponding curve sets
curve_sets = {
    90: curve_set_1,
    80: curve_set_2,
    70: curve_set_3,
    60: curve_set_4,
    50: curve_set_5,
    40: curve_set_6,
    30: curve_set_7
}


# Function to determine volumetric strain (x) given factor of safety (y) and Dr value
def determine_volumetric_strain(y, Dr):
    if Dr not in curve_sets:
        raise ValueError("Invalid Dr value provided.")

    # Select the corresponding curve set function
    curve_function = curve_sets[Dr]

    if Dr == 50 and y < 0.9:
        return 3.4

    if Dr == 40 and y < 0.95:
        return 4.4

    if Dr == 30 and y < 0.98:
        return 5.5

    # Wrapper function to handle array input for fsolve
    def wrapped_curve_function(x):
        return np.array([curve_function(xi, y) for xi in x])

    # Use fsolve with a larger initial guess range to find the root of the equation
    volumetric_strain = fsolve(wrapped_curve_function, x0=np.linspace(-10, 10, num=100))

    # Filter out any non-finite results and return the first valid result
    valid_strains = [strain for strain in volumetric_strain if np.isfinite(strain)]

    if valid_strains:
        return valid_strains[0]
    else:
        raise RuntimeError("Failed to converge to a solution.")


# Example usage
y = 0.991133  # Factor of safety
Dr = 30  # Dr value

volumetric_strain = determine_volumetric_strain(y, Dr)
print(f"Volumetric strain for factor of safety {y} and Dr {Dr} is {volumetric_strain}.")