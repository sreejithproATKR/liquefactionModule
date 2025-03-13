import pandas as pd
from tkinter import ttk, messagebox
from CSR_Class import CSR
from CRR_Class import CRR
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import findVolumetricStrain


def load_spt_data_from_excel(file_path):
    """
    Load SPT data from an Excel sheet.

    Parameters:
    file_path (str): The path to the Excel file.

    Returns:
    pd.DataFrame: A DataFrame containing the SPT data.
    """
    try:
        # Load the Excel file
        df = pd.read_excel(file_path, engine='openpyxl')

        # Display the first few rows of the DataFrame
        print("SPT Data loaded successfully:")
        print(df.head())

        return df
    except Exception as e:
        print(f"Error loading SPT data from Excel: {e}")
        return None


def preview_spt_data(frame, spt_data):
    """
    Preview SPT data in the given frame.

    Parameters:
    frame (tk.Frame): The frame to display the SPT data.
    spt_data (pd.DataFrame): The DataFrame containing SPT data.
    """
    if spt_data is not None:
        # Clear the frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Create a treeview to display the data
        tree = ttk.Treeview(frame)
        tree.pack(fill="both", expand=True)

        #Scroll Bar for the tree view, temporarily abandoned
        # scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        # scrollbar.place()
        # tree.configure(yscrollcommand=scrollbar.set)
        # scrollbar.pack(side='right', fill='y')

        # Define columns
        tree["columns"] = list(spt_data.columns)
        tree["show"] = "headings"

        # Create column headers
        for col in spt_data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Insert data into the treeview
        for index, row in spt_data.iterrows():
            tree.insert("", "end", values=list(row))
    else:
        messagebox.showerror("Error", "Failed to load SPT data.")


def calculate_and_preview_csr(frame, spt_data, unit_weight_water, water_table_depth, peak_acceleration,manual_fs, water_table_depth_stat):
    """
    Calculate CSR for each depth in SPT data and preview in the given frame.

    Parameters:
    frame (tk.Frame): The frame to display the CSR data.
    spt_data (pd.DataFrame): The DataFrame containing SPT data.
    unit_weight_water (float): Unit weight of water.
    water_table_depth (float): Water table depth.
    peak_acceleration (float): Peak horizontal acceleration.
    """
    current_sigma_1 = 0
    current_sigma_0 = 0
    current_depth = 0
    print(manual_fs)

    if spt_data is not None:
        # Calculate CSR for each depth and add it to the DataFrame
        csr_values = []
        for index, row in spt_data.iterrows():
            depth = row["Depth"]
            gamma = row["Gamma"]
            if water_table_depth_stat == 1:
                water_table_depth = row["GWL"]
            else:
                water_table_depth = water_table_depth

            csr_calculator = CSR(depth, gamma, unit_weight_water, peak_acceleration, water_table_depth, current_sigma_1, current_sigma_0,current_depth,manual_fs)
            current_sigma_1,current_sigma_0, csr_value = csr_calculator.calculate_csr()
            csr_values.append(csr_value)
            current_depth = depth

        spt_data["CSR"] = csr_values

        # Preview the updated SPT data with CSR values
        preview_spt_data(frame, spt_data)
    else:
        messagebox.showerror("Error", "Failed to load SPT data.")


def calculate_and_preview_crr(frame, spt_data, unit_weight_water, water_table_depth, henergy_c, borehole_diameter_var, sampler_c, fines_correction_type, eq_magnitude, overburden_corr_cap):
    """
    Calculate CRR for each SPT data and preview in the given frame.

    Parameters:
    frame (tk.Frame): The frame to display the CSR data.
    spt_data (pd.DataFrame): The DataFrame containing SPT data.
    unit_weight_water (float): Unit weight of water.
    water_table_depth (float): Water table depth.
    peak_acceleration (float): Peak horizontal acceleration.
    """
    if spt_data is not None:
        # Calculate CSR for each depth and add it to the DataFrame
        crr_values = []
        for index, row in spt_data.iterrows():
            spt_n_value = row["SPT"]
            depth = row['Depth']
            gamma = row['Gamma']
            fines_content = row["Fines"]
            crr_calculator = CRR("SPT", depth, 0, overburden_corr_cap, water_table_depth, gamma,eq_magnitude, unit_weight_water,henergy_c,borehole_diameter_var,
                                 sampler_c,fines_content,fines_correction_type, spt_n_value)
            crr_value = crr_calculator.calculate_crr_spt()
            crr_values.append(crr_value)

        spt_data["CRR"] = crr_values

        if 'CSR' in spt_data.columns:
            # Calculate the ratio CRR/CSR as FOS
            spt_data['FOS'] = spt_data['CRR'] / spt_data['CSR']
            spt_data['FOS'] = spt_data['FOS'].round(2).clip(upper = 5.0)
        else:
            # Display a messagebox if CSR field does not exist
            messagebox.showinfo("Error", "Calculate CSR")


        # Preview the updated SPT data with CSR values
        preview_spt_data(frame, spt_data)
        print(eq_magnitude)
    else:
        messagebox.showerror("Error", "Failed to load SPT data.")

    def calculate_and_preview_fos(frame, spt_data):
        """
        Calculate CRR for each SPT data and preview in the given frame.

        Parameters:
        frame (tk.Frame): The frame to display the CSR data.
        spt_data (pd.DataFrame): The DataFrame containing SPT data.
        unit_weight_water (float): Unit weight of water.
        water_table_depth (float): Water table depth.
        peak_acceleration (float): Peak horizontal acceleration.
        """
        if spt_data is not None:
            # Calculate CSR for each depth and add it to the DataFrame
            fos_values = []
            spt_data['FOS'] = spt_data['CRR'] / spt_data['CSR']
            # Preview the updated SPT data with CSR values
            preview_spt_data(frame, spt_data)

        else:
            messagebox.showerror("Error", "Failed to load SPT data.")

def plot_crr_csr_vs_depth(frame, spt_data):
    """
    Plot CRR vs Depth and CSR vs Depth in a single graph.

    Parameters:
    spt_data (pd.DataFrame): The DataFrame containing SPT or CPT data with CRR and CSR values.
    """
    if spt_data is not None:
        for widget in frame.winfo_children():
            widget.destroy()

        depth = spt_data["Depth"]
        crr = spt_data["CRR"]
        csr = spt_data["CSR"]

        fig, ax = plt.subplots()
        ax.cla()

        ax.plot(crr, depth, label="CRR", marker='o')
        ax.plot(csr, depth, label="CSR", marker='x')

        ax.set_xlabel("CRR / CSR")
        ax.set_ylabel("Depth (m BGL)")
        ax.set_title("CRR/CSR vs Depth")
        ax.invert_yaxis()
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        messagebox.showerror("Error", "Failed to load SPT or CPT data.")

def export_crr_csr(file_path,spt_data):
    try:
        directory = os.path.dirname(file_path)
        processed_file_path = os.path.join(directory, "processed",
                                           f"{os.path.splitext(file_path)[0]}_Processed.xlsx")
        # Export the DataFrame to an Excel file
        spt_data.to_excel(processed_file_path, index=False)
        print(f"DataFrame successfully exported to {processed_file_path}")
    except Exception as e:
        print(f"An error occurred while exporting the DataFrame: {e}")

    pass


def export_interpolated_csr_crr(file_path,spt_data):
    df = interpolate_output(spt_data)
    try:
        directory = os.path.dirname(file_path)
        processed_file_path = os.path.join(directory, "processed",
                                           f"{os.path.splitext(file_path)[0]}_Processed.xlsx")
        # Export the DataFrame to an Excel file
        df.to_excel(processed_file_path, index=False)
        print(f"DataFrame successfully exported to {processed_file_path}")
    except Exception as e:
        print(f"An error occurred while exporting the DataFrame: {e}")

    pass

# Define the function to calculate volumetric strain for each row
def calculate_volumetric_strain_for_row(row):
    return findVolumetricStrain.calculate_volumetric_strain(row['Interpolated SPT'], row['Interpolated Fines'], row['Interpolated FOS'])


def interpolate_output(spt_data):

    spt_data_interpolated = spt_data.copy()

    # Identify consecutive occurrences of value 2
    # spt_data_interpolated['is_CRR_2'] = (spt_data_interpolated['CRR'] == 2).astype(int)
    # consecutive_2 = spt_data_interpolated['is_CRR_2'].groupby(
    #     spt_data_interpolated['CRR'].ne(2).cumsum()
    # ).cumsum()
    #
    # # Remove rows where CRR is equal to 2 and not consecutive more than twice
    # data_filtered = spt_data_interpolated[~((spt_data_interpolated['CRR'] == 2) & (consecutive_2 <= 2))]

    # Interpolation function
    interp_func_crr = interp1d(spt_data_interpolated['Depth'], spt_data_interpolated['CRR'], kind='cubic')
    interp_func_csr = interp1d(spt_data_interpolated['Depth'], spt_data_interpolated['CSR'], kind='cubic')
    interp_func_fines = interp1d(spt_data_interpolated['Depth'], spt_data_interpolated['Fines'], kind='cubic')
    interp_func_spt = interp1d(spt_data_interpolated['Depth'], spt_data_interpolated['SPT'], kind='cubic')

    # New depth values from min to max depth rounded to whole numbers with intervals of 0.1m
    new_depth = np.arange(min(spt_data_interpolated['Depth']), int(max(spt_data_interpolated['Depth'])) + 10, 0.1)

    # Ensure new_depth does not exceed the maximum depth in the provided data
    new_depth = new_depth[new_depth <= max(spt_data_interpolated['Depth'])]

    # Interpolated CRR values
    new_crr = interp_func_crr(new_depth)
    new_csr = interp_func_csr(new_depth)
    new_fines = interp_func_fines(new_depth)
    new_spt = interp_func_spt(new_depth)


    new_crr = np.maximum(new_crr, 0)

    spt_data_interpolated = pd.DataFrame(
        {'Depth': new_depth.round(1), 'Interpolated CRR': np.round(new_crr,decimals = 2), 'Interpolated CSR': np.round(new_csr,decimals = 2)
            ,'Interpolated SPT': np.round(new_spt,decimals = 0),'Interpolated Fines': np.round(new_csr,decimals = 2)})
    spt_data_interpolated['Interpolated FOS'] = spt_data_interpolated['Interpolated CRR'] / spt_data_interpolated['Interpolated CSR']
    spt_data_interpolated['Interpolated FOS'] = spt_data_interpolated['Interpolated FOS'].round(2).clip(upper=5.0)

    window_size = 5
    poly_order = 3

    # Smooth CSR, CRR, and FOS columns
    spt_data_interpolated['CSR_smooth'] = savgol_filter(spt_data_interpolated['Interpolated CSR'], window_size, poly_order)
    spt_data_interpolated['CRR_smooth'] = savgol_filter(spt_data_interpolated['Interpolated CRR'], window_size, poly_order)
    spt_data_interpolated['FOS_smooth'] = savgol_filter(spt_data_interpolated['Interpolated FOS'], window_size, poly_order)

    spt_data_interpolated['FOS_smooth'] = spt_data_interpolated['FOS_smooth'].clip(lower=0).clip(upper=5)
    spt_data_interpolated['CRR_smooth'] = spt_data_interpolated['CRR_smooth'].clip(lower=0).clip(upper=2)


    spt_data_interpolated['Volumetric Strain'] = spt_data_interpolated.apply(calculate_volumetric_strain_for_row, axis=1)
    spt_data_interpolated['Settlement'] = (spt_data_interpolated['Volumetric Strain']/100)*0.1
    spt_data_interpolated['Total Settlement'] = (spt_data_interpolated['Settlement'].cumsum())*1000


    return spt_data_interpolated

def plot_interpolated_output(frame1, frame2, spt_data):
    if spt_data is not None:
        for widget in frame1.winfo_children():
            widget.destroy()
        for widget in frame2.winfo_children():
            widget.destroy()
        fig1, ax1 = plt.subplots()
    # Update the copy of the DataFrame with interpolated values

        spt_data_interpolated = interpolate_output(spt_data)
    # Plotting the results
        ax1.cla()
        ax1.plot(spt_data['CRR'], spt_data['Depth'], 'o', label='Original CRR')
        ax1.plot(spt_data['CSR'], spt_data['Depth'], '*', label='Original CSR')
        ax1.plot(spt_data_interpolated['CRR_smooth'], spt_data_interpolated['Depth'], '-', label='Interpolated CRR')
        ax1.plot(spt_data_interpolated['CSR_smooth'], spt_data_interpolated['Depth'], '-', label='Interpolated CSR')
        ax1.plot(spt_data_interpolated['FOS_smooth'], spt_data_interpolated['Depth'], '-', label='Interpolated FOS')
        ax1.set_xlabel('CRR - CSR - FOS')
        ax1.set_ylabel('Depth')
        ax1.invert_yaxis()
        ax1.legend()
        ax1.set_title('CSR/CRR vs Depth')
        # ax.grid(False)
        canvas = FigureCanvasTkAgg(fig1, master=frame1)
        canvas.draw()
        canvas.get_tk_widget().pack()

        fig2, ax2 = plt.subplots()
        ax2.cla()
        ax2.plot(spt_data_interpolated['Total Settlement'], spt_data_interpolated['Depth'], '-', label='Settlement')
        ax2.set_xlabel('Settlement (mm)')
        ax2.set_ylabel('Depth')
        ax2.invert_yaxis()
        ax2.legend()
        ax2.set_title('Settlement vs Depth')

        canvas = FigureCanvasTkAgg(fig2, master=frame2)
        canvas.draw()
        canvas.get_tk_widget().pack()

    else:
        messagebox.showerror("Error", "Failed to load SPT or CPT data.")

