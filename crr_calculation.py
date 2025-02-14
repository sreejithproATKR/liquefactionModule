def calculate_depth_correction(sigma_0):
    henergy_c = (1/sigma_0) ** 0.5
    return max(min(henergy_c, 1.17), 0.4)


class CRR:
    def __init__(self, data_type, depth, water_table_depth,gamma, unit_weight_water, depth_c, boreholed_c, rod_length_c, sampler_c,spt_n_value=None, cpt_qc_value=None):
        self.unit_weight_water = unit_weight_water
        self.gamma = gamma
        self.water_table_depth = water_table_depth
        self.depth = depth
        self.sampler_c = sampler_c
        self.rod_length_c = rod_length_c
        self.boreholed_c = boreholed_c
        self.depth_c = depth_c
        self.data_type = data_type
        self.spt_n_value = spt_n_value
        self.cpt_qc_value = cpt_qc_value


    def calculate_stresses(self):
        if self.depth <= self.water_table_depth:
            sigma_1 = self.depth * self.gamma
            sigma_0 = sigma_1
        else:
            sigma_1 = self.depth * self.gamma
            sigma_0 = self.water_table_depth * self.gamma + (self.depth - self.water_table_depth) * (
                    self.gamma - self.unit_weight_water)

        return sigma_1, sigma_0


    def calculate_crr(self):
        """
        Calculate the Cyclic Resistance Ratio (CRR).

        Returns:
        float: The calculated CRR value.
        """
        if self.data_type == "SPT":
            return self.calculate_crr_spt()
        elif self.data_type == "CPT":
            return self.calculate_crr_cpt()
        else:
            raise ValueError("Invalid data type. Must be 'SPT' or 'CPT'.")

    def calculate_crr_spt(self):
        """
        Calculate CRR using SPT data.

        Returns:
        float: The calculated CRR value.
        """
        if self.spt_n_value is None:
            raise ValueError("SPT N-value is required for CRR calculation using SPT data.")

        a = 0.048
        b = -0.1248
        c = -0.004721
        d = 0.009578
        e = 0.0006136
        f = -0.0003285
        g = -1.673 * pow(10, -5)
        h = 3.714 * pow(10, -6)
        numerator = a + (c * self.spt_n_value) + (e * pow(self.spt_n_value, 2)) + (g * pow(self.spt_n_value, 3))
        denominator = 1 + (b * self.spt_n_value) + (d * self.spt_n_value ** 2) + (f * self.spt_n_value ** 3) + (h * self.spt_n_value ** 4)
        crr_value = numerator / denominator
        sigma_1, sigma_0 = self.calculate_stresses()
        crr_value = (numerator / denominator) * calculate_depth_correction(sigma_0)
        return round(crr_value,2)

    def calculate_crr_cpt(self):
        """
        Calculate CRR using CPT data.

        Returns:
        float: The calculated CRR value.
        """
        if self.cpt_qc_value is None:
            raise ValueError("CPT qc-value is required for CRR calculation using CPT data.")

        # Example formula for CRR calculation using CPT data (replace with actual formula)
        crr_value = 0.2 * self.cpt_qc_value
        return round(crr_value, 2)

# Example usage
# crr_spt = CRR(data_type="SPT", spt_n_value=30)
# print(crr_spt.calculate_crr())

# crr_cpt = CRR(data_type="CPT", cpt_qc_value=15)
# print(crr_cpt.calculate_crr())