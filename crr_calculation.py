import math

def calculate_depth_correction(sigma_0):
    depth_c = (1/sigma_0) ** 0.5
    return max(min(depth_c, 1.17), 0.4)



class CRR:
    def __init__(self, data_type, depth, water_table_depth,gamma, unit_weight_water=10, henergy_c=1, boreholed_c=1, rod_length_c=1,
                 sampler_c=1,fines_content=0, fines_correction_type="No Correction" ,spt_n_value=None, cpt_qc_value=None):
        self.fines_correction_type = fines_correction_type
        self.fines_content = fines_content
        self.henergy_c = henergy_c
        self.unit_weight_water = unit_weight_water
        self.gamma = gamma
        self.water_table_depth = water_table_depth
        self.depth = depth
        self.sampler_c = sampler_c
        self.rod_length_c = rod_length_c
        self.boreholed_c = boreholed_c
        self.data_type = data_type
        self.spt_n_value = spt_n_value
        self.cpt_qc_value = cpt_qc_value


    def calculate_alpha_beta_idriss(self):
        if self.fines_content <= 5:
            alpha = 0
            beta = 1.0
        elif 5 < self.fines_content <= 35:
            alpha = math.exp(1.76-(190/pow(self.fines_content,2)))
            beta = (0.99+ pow(self.fines_content,1.5))/100
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
            fines_c = self.modified_star_olsen_corr()

        return self.spt_n_value


    def idriss_seed_corr(self):
        alpha, beta = self.calculate_alpha_beta_idriss()
        corrected_n = alpha + (beta * self.spt_n_value)
        return corrected_n

    def star_olsen_corr(self,):
        corrected_n = self.fines_content * 0.5
        return corrected_n

    def modified_star_olsen_corr(self):
        corrected_n = self.fines_content * 0.25
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
        denominator = 1 + (b * self.spt_n_value) + (d * self.spt_n_value ** 2) + (f * self.spt_n_value ** 3) + (h * self.spt_n_value ** 4)
        sigma_1, sigma_0 = self.calculate_stresses()

        crr_value = ((numerator / denominator) * calculate_depth_correction(sigma_0) * self.henergy_c * self.boreholed_c
                     * self.rod_length_c * self.sampler_c)
        return round(crr_value,3)

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

# Example usage
# crr_spt = CRR(data_type="SPT", spt_n_value=30)
# print(crr_spt.calculate_crr())

# crr_cpt = CRR(data_type="CPT", cpt_qc_value=15)
# print(crr_cpt.calculate_crr())