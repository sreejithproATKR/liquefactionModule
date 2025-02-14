class CSR:
    def __init__(self, depth, gamma, unit_weight_water, peak_acceleration, water_table_depth):
        self.depth = depth
        self.gamma = gamma
        self.unit_weight_water = unit_weight_water
        self.peak_acceleration = peak_acceleration
        self.water_table_depth = water_table_depth

    def calculate_gamma_d(self):
        # Example equations for gamma_d based on depth ranges
        if self.depth <= 9.15:
            gamma_d = 1.0 - 0.00765 * self.depth
        elif self.depth <= 23:
            gamma_d = 1.174 - 0.0267 * self.depth
        elif self.depth <= 30:
            gamma_d = 0.744 - 0.008 * self.depth
        else:
            gamma_d = 0.5
        return gamma_d

    def calculate_stresses(self):
        if self.depth <= self.water_table_depth:
            sigma_1 = self.depth * self.gamma
            sigma_0 = sigma_1
        else:
            sigma_1 = self.depth * self.gamma
            sigma_0 = self.water_table_depth * self.gamma + (self.depth - self.water_table_depth) * (
                    self.gamma - self.unit_weight_water)

        return sigma_1, sigma_0



    def calculate_csr(self):
        """
        Calculate the Cyclic Stress Ratio (CSR).

        Returns:
        float: The calculated CSR value.
        """
        # Calculate total stress (σ1) and effective stress (σ0)
        sigma_1, sigma_0 = self.calculate_stresses()

        # Calculate CSR using the given formula
        gamma_d = self.calculate_gamma_d()
        csr_value = 0.65 * (sigma_1 / sigma_0) * self.peak_acceleration * gamma_d
        return round(csr_value,2)