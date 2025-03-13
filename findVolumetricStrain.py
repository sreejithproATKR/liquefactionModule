import numpy as np
from scipy.optimize import fsolve
from scipy.interpolate import interp1d


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


curve_set_5_table = {
    'x': [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1,
          1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2,
          2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3,
          3.1, 3.2, 3.3, 3.4],
    'y': np.array([2.0211, 2.3208, 2.5793, 2.6601, 2.5075, 2.2214, 1.9302, 1.6928, 1.515, 1.3854, 1.2906,
                   1.2204, 1.1676, 1.1272, 1.0956, 1.0707, 1.0506, 1.0343, 1.0209, 1.0097, 1.0003, 0.9923,
                   0.9855, 0.9796, 0.9745, 0.97, 0.9661, 0.9627, 0.9596, 0.9569, 0.9545, 0.9523, 0.9503,
                   0.9485, 0.9469])
}

curve_set_6_table = {
    'x': [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2,
          2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3,
          3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4,
          4.1, 4.2, 4.3, 4.4, 4.5],
    'y': np.array([1.0693, 1.0578, 1.0461, 1.0351, 1.0252, 1.0166, 1.0091, 1.0026, 0.9972,
                   0.9925, 0.9885, 0.9851, 0.9822, 0.9796, 0.9775, 0.9756, 0.9739,
                   0.9724, 0.9711, 0.97, 0.969, 0.9681, 0.9673, 0.9665, 0.9659,
                   0.9653, 0.9647, 0.9642, 0.9638, 0.9634, 0.963, 0.9627, 0.9623,
                   0.962, 0.9618, 0.9615])
}


def curve_set_7(x, y):
    return -0.0056243 * x + 1.010753 - y


# Dictionary to map Dr values to corresponding curve sets
curve_sets = {
    90: curve_set_1,
    80: curve_set_2,
    70: curve_set_3,
    60: curve_set_4,
    50: curve_set_5_table,
    40: curve_set_6_table,
    30: curve_set_7
}


# Function to determine Dr from SPT N value
def determine_Dr(SPT_N):
    SPT_to_Dr = {
        3: 30,
        6: 40,
        10: 50,
        14: 60,
        20: 70,
        25: 80,
        30: 90
    }

    if SPT_N in SPT_to_Dr:
        return SPT_to_Dr[SPT_N]

    else:
        # Find the two nearest SPT values in the mapping list
        lower_SPT = max([spt for spt in SPT_to_Dr.keys() if spt < SPT_N], default=None)
        upper_SPT = min([spt for spt in SPT_to_Dr.keys() if spt > SPT_N], default=None)

        if lower_SPT is None:
            return 30

        elif upper_SPT is None:
            return 90

        # Interpolate to find the Dr value for the given SPT N value
        interpolator = interp1d([lower_SPT, upper_SPT], [SPT_to_Dr[lower_SPT], SPT_to_Dr[upper_SPT]])

        return interpolator(SPT_N)


# Function to determine volumetric strain (x) given factor of safety (y) and Dr value
def determine_volumetric_strain(y, Dr):
    Dr = float(Dr)

    if Dr in curve_sets:

        # Select the corresponding curve set function
        if Dr == 90 and y <= 0.41:
            return 1.31

        if Dr == 80 and y <= 0.51:
            return 2.18

        if Dr == 70 and y <= 0.77:
            return 2.77

        if Dr == 60 and y <= 0.98:
            return 5.50

        if Dr == 50 and y <= 0.93:
            return 3.40

        if Dr == 40 and y <= 0.95:
            return 4.40

        if Dr == 30 and y <= 0.98:
            return 5.5


        if Dr == 50:
            table = curve_sets[Dr]
            interpolator = interp1d(table['y'], table['x'], fill_value="extrapolate")
            return interpolator(y)

        elif Dr == 40:
            table = curve_sets[Dr]
            interpolator = interp1d(table['y'], table['x'], fill_value="extrapolate")
            return interpolator(y)

        else:
            curve_function = curve_sets[Dr]
            volumetric_strain = fsolve(lambda x: curve_function(x, y), x0=0)
            return volumetric_strain[0]

    else:
        # Find the two nearest Dr values in the mapping list
        lower_Dr = max([d for d in curve_sets.keys() if d < Dr], default=None)
        upper_Dr = min([d for d in curve_sets.keys() if d > Dr], default=None)

        if lower_Dr is None or upper_Dr is None:
            raise ValueError("Dr value is out of interpolation range.")

        # Calculate volumetric strain for the two nearest Dr values
        lower_strain = determine_volumetric_strain(y, lower_Dr)
        upper_strain = determine_volumetric_strain(y, upper_Dr)

        # Interpolate to find the volumetric strain for the given Dr value
        interpolator = interp1d([lower_Dr, upper_Dr], [lower_strain, upper_strain])
        return interpolator(Dr)


# Function to determine volumetric strain given SPT N value, Fines, and FOS
def calculate_volumetric_strain(SPT_N, fines, FOS):
    # Determine Dr from SPT N value
    Dr = determine_Dr(SPT_N)
    # Calculate volumetric strain using the determined Dr and given FOS
    volumetric_strain = max(determine_volumetric_strain(FOS, Dr),0)
    return volumetric_strain


# Example usage
SPT_N = 20  # SPT N value
fines = None  # Fines (not used in current calculation)
FOS = 3.5  # Factor of safety

volumetric_strain = calculate_volumetric_strain(SPT_N, fines, FOS)
print(f"Volumetric strain for SPT N value {SPT_N}, fines {fines}, and factor of safety {FOS} is {volumetric_strain}.")