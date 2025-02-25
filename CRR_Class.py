import math


def calculate_depth_correction(sigma_0):
    depth_c = (1 / sigma_0) ** 0.5
    return max(min(depth_c, 1.17), 0.4)


class CRR:
    def __init__(self, data_type, depth, offset, water_table_depth, gamma, eq_magnitude=7.5, unit_weight_water=10,
                 henergy_c=1, boreholed_c=1,
                 sampler_c=1, fines_content=0, fines_correction_type="No Correction", spt_n_value=None,
                 cpt_qc_value=None):
        self.offset = offset
        self.eq_magnitude = eq_magnitude
        self.fines_correction_type = fines_correction_type
        self.fines_content = fines_content
        self.henergy_c = henergy_c
        self.unit_weight_water = unit_weight_water
        self.gamma = gamma
        self.water_table_depth = water_table_depth
        self.depth = depth
        self.sampler_c = sampler_c
        self.boreholed_c = boreholed_c
        self.data_type = data_type
        self.spt_n_value = spt_n_value
        self.cpt_qc_value = cpt_qc_value

    def rod_length_corr(self):

        if self.depth + self.offset < 3.0:
            rod_length_c = 0.75
        elif 3.0 < self.depth + self.offset < 4.0:
            rod_length_c = 0.80
        elif 4.0 < self.depth + self.offset < 6.0:
            rod_length_c = 0.85
        elif 6.0 < self.depth + self.offset < 10.0:
            rod_length_c = 0.95
        else:
            rod_length_c = 1.0

        return rod_length_c

    def calculate_deltan_3(self):
        if self.fines_content <= 5:
            deltaN60 = 0.0
        elif 5 <= self.fines_content <= 35:
            deltaN60 = 0.24 * self.fines_content + 1.20
        else:
            deltaN60 = 7.2
        return deltaN60

    def calculate_deltan_4(self):
        if self.fines_content <= 5:
            deltaN60 = 0.0
        else:
            deltaN60 = 5 <= self.fines_content <= 35
        return deltaN60

    def calculate_alpha_beta_idriss(self):
        if self.fines_content <= 5:
            alpha = 0
            beta = 1.0
        elif 5 < self.fines_content <= 35:
            alpha = math.exp(1.76 - (190 / pow(self.fines_content, 2)))
            beta = (0.99 + pow(self.fines_content, 1.5)) / 100
        else:
            alpha = 5.0
            beta = 1.2
        return alpha, beta

    def calculate_fines_c(self):
        if self.fines_correction_type == "No Correction":
            self.spt_n_value = self.spt_n_value
        elif self.fines_correction_type == "Idriss & Seed, 1997":
            self.spt_n_value = self.idriss_seed_corr()
        elif self.fines_correction_type == "Stark & Olsen, 1995":
            self.spt_n_value = self.star_olsen_corr()
        else:
            self.spt_n_value = self.modified_star_olsen_corr()

        return self.spt_n_value

    def idriss_seed_corr(self):
        alpha, beta = self.calculate_alpha_beta_idriss()
        corrected_n = alpha + (beta * self.spt_n_value)
        return corrected_n

    def star_olsen_corr(self, ):
        deltaN60 = self.calculate_deltan_3()
        corrected_n = self.spt_n_value + deltaN60
        return corrected_n

    def modified_star_olsen_corr(self):
        deltaN60 = self.calculate_deltan_4()
        corrected_n = self.spt_n_value + deltaN60
        return corrected_n

    def calculate_stresses(self):
        if self.depth <= self.water_table_depth:
            sigma_1 = self.depth * self.gamma
            sigma_0 = sigma_1
        else:
            sigma_1 = self.depth * self.gamma
            sigma_0 = self.water_table_depth * self.gamma + (self.depth - self.water_table_depth) * (
                    self.gamma - self.unit_weight_water)

        return sigma_1, sigma_0

    def overburden_corr(self, crr_value):

        k_alpha = 1.0
        sigma_1, sigma_0 = self.calculate_stresses()
        sigma_m = (0.65 * sigma_0) / 96.0
        k_sigma = 0.0068 * pow(sigma_m, 2) - 0.1159 * sigma_m + 1.00778
        corrected_crr = crr_value * k_alpha * k_sigma
        return corrected_crr

    def magnitude_corr(self, crr_value):
        msf = pow(10, 2.24) / pow(self.eq_magnitude, 2.56)
        corrected_crr = crr_value * msf
        return corrected_crr

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
        self.spt_n_value = self.calculate_fines_c()

        a = 0.048
        b = -0.1248
        c = -0.004721
        d = 0.009578
        e = 0.0006136
        f = -0.0003285
        g = -1.673 * pow(10, -5)
        h = 3.714 * pow(10, -6)
        numerator = a + (c * self.spt_n_value) + (e * pow(self.spt_n_value, 2)) + (g * pow(self.spt_n_value, 3))
        denominator = 1 + (b * self.spt_n_value) + (d * self.spt_n_value ** 2) + (f * self.spt_n_value ** 3) + (
                    h * self.spt_n_value ** 4)
        sigma_1, sigma_0 = self.calculate_stresses()

        crr_value = ((numerator / denominator) * calculate_depth_correction(sigma_0) * self.henergy_c * self.boreholed_c
                     * self.sampler_c * self.rod_length_corr())

        crr_value = self.overburden_corr(crr_value)
        crr_value = self.magnitude_corr(crr_value)

        if crr_value < 0:
            crr_value = 2.0
        else:
            crr_value = min(crr_value, 2.0)

        return round(crr_value, 3)

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
        return round(crr_value, 3)