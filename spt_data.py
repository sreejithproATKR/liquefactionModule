import pandas as pd
import tkinter as tk
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

# from main import spt_data

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


def preview_spt_data(frame, input_spt_data):
    """
    Preview SPT data in the given frame.

    Parameters:
    frame (tk.Frame): The frame to display the SPT data.
    spt_data (pd.DataFrame): The DataFrame containing SPT data.
    """
    if input_spt_data is not None:
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
        tree["columns"] = list(input_spt_data.columns)
        tree["show"] = "headings"

        # Create column headers
        for col in input_spt_data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Insert data into the treeview
        for index, row in input_spt_data.iterrows():
            tree.insert("", "end", values=list(row))
    else:
        messagebox.showerror("Error", "Failed to load SPT data.")


def calculate_and_preview(frame, input_spt_data, unit_weight_water, water_table_depth, peak_acceleration,
                          manual_fs, water_table_depth_stat, overburden_corr_cap, eq_magnitude, henergy_c,
                          borehole_diameter_var, sampler_c, fines_correction_type):
    global spt_data  # Ensure spt_data is updated globally
    if input_spt_data is not None:
        # Initialize an empty DataFrame to store the results
        # Group the data by borehole
        all_boreholes = pd.DataFrame()
        grouped = input_spt_data.groupby('Borehole')
        for borehole, data in grouped:
            current_sigma_1 = 0
            current_sigma_0 = 0
            current_depth = 0
            # Calculate CSR for each depth and add it to the DataFrame
            csr_values = []
            crr_values = []
            for index, row in data.iterrows():
                depth = row["Depth"]
                gamma = row["Gamma"]
                spt_n_value = row['SPT']
                fines_content = row['Fines']
                if water_table_depth_stat == 1:
                    water_table_depth = row["GWL"]
                else:
                    water_table_depth = water_table_depth
                csr_calculator = CSR(depth, gamma, unit_weight_water, peak_acceleration, water_table_depth, current_sigma_1, current_sigma_0, current_depth, manual_fs)
                current_sigma_1, current_sigma_0, csr_value = csr_calculator.calculate_csr()
                csr_values.append(csr_value)
                crr_calculator = CRR("SPT", depth, 0, overburden_corr_cap, water_table_depth, gamma, eq_magnitude,
                                     unit_weight_water, henergy_c, borehole_diameter_var,
                                     sampler_c, fines_content, fines_correction_type, spt_n_value)
                crr_value = crr_calculator.calculate_crr_spt()
                crr_values.append(crr_value)
                current_depth = depth
            data["CSR"] = csr_values
            data["CRR"] = crr_values
            data["FOS"] = csr_values
            data['FOS'] = data['CRR'] / data['CSR']
            data['FOS'] = data['FOS'].round(2).clip(upper=5.0)
            # Append the CSR data for the current borehole to the final DataFrame
            all_boreholes = pd.concat([all_boreholes, data], ignore_index=True)
            spt_data = all_boreholes
        # Update the global spt_data DataFrame
        preview_spt_data(frame, spt_data)
        return spt_data
    else:
        messagebox.showerror("Error", "Failed to load SPT data.")


# def calculate_and_preview_crr(frame, spt_data, unit_weight_water, water_table_depth, henergy_c, borehole_diameter_var, sampler_c, fines_correction_type, eq_magnitude, overburden_corr_cap):
#     """
#     Calculate CRR for each SPT data and preview in the given frame.
#
#     Parameters:
#     frame (tk.Frame): The frame to display the CSR data.
#     spt_data (pd.DataFrame): The DataFrame containing SPT data.
#     unit_weight_water (float): Unit weight of water.
#     water_table_depth (float): Water table depth.
#     peak_acceleration (float): Peak horizontal acceleration.
#     """
#     if spt_data is not None:
#         # Calculate CSR for each depth and add it to the DataFrame
#         crr_values = []
#         for index, row in spt_data.iterrows():
#             spt_n_value = row["SPT"]
#             depth = row['Depth']
#             gamma = row['Gamma']
#             fines_content = row["Fines"]
#             crr_calculator = CRR("SPT", depth, 0, overburden_corr_cap, water_table_depth, gamma,eq_magnitude, unit_weight_water,henergy_c,borehole_diameter_var,
#                                  sampler_c,fines_content,fines_correction_type, spt_n_value)
#             crr_value = crr_calculator.calculate_crr_spt()
#             crr_values.append(crr_value)
#
#         spt_data["CRR"] = crr_values
#
#         if 'CSR' in spt_data.columns:
#             # Calculate the ratio CRR/CSR as FOS
#             spt_data['FOS'] = spt_data['CRR'] / spt_data['CSR']
#             spt_data['FOS'] = spt_data['FOS'].round(2).clip(upper = 5.0)
#         else:
#             # Display a messagebox if CSR field does not exist
#             messagebox.showinfo("Error", "Calculate CSR")
#
#
#         # Preview the updated SPT data with CSR values
#         preview_spt_data(frame, spt_data)
#         print(eq_magnitude)
#     else:
#         messagebox.showerror("Error", "Failed to load SPT data.")
#
#     def calculate_and_preview_fos(frame, spt_data):
#         """
#         Calculate CRR for each SPT data and preview in the given frame.
#
#         Parameters:
#         frame (tk.Frame): The frame to display the CSR data.
#         spt_data (pd.DataFrame): The DataFrame containing SPT data.
#         unit_weight_water (float): Unit weight of water.
#         water_table_depth (float): Water table depth.
#         peak_acceleration (float): Peak horizontal acceleration.
#         """
#         if spt_data is not None:
#             # Calculate CSR for each depth and add it to the DataFrame
#             fos_values = []
#             spt_data['FOS'] = spt_data['CRR'] / spt_data['CSR']
#             # Preview the updated SPT data with CSR values
#             preview_spt_data(frame, spt_data)
#
#         else:
#             messagebox.showerror("Error", "Failed to load SPT data.")

def plot_crr_csr_vs_depth(frame, spt_data):
    """
    Plot CRR vs Depth and CSR vs Depth in a single graph.

    Parameters:
    spt_data (pd.DataFrame): The DataFrame containing SPT or CPT data with CRR and CSR values.
    """

    spt_data.head()
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
    # Initialize an empty DataFrame to store the results
    all_boreholes_interpolated = pd.DataFrame()

    # Group the data by borehole
    grouped = spt_data.groupby('Borehole')

    for borehole, data in grouped:
        spt_data_interpolated = data.copy()

        # Interpolation functions
        interp_func_crr = interp1d(spt_data_interpolated['Depth'], spt_data_interpolated['CRR'], kind='cubic')
        interp_func_csr = interp1d(spt_data_interpolated['Depth'], spt_data_interpolated['CSR'], kind='cubic')
        interp_func_fines = interp1d(spt_data_interpolated['Depth'], spt_data_interpolated['Fines'], kind='cubic')
        interp_func_spt = interp1d(spt_data_interpolated['Depth'], spt_data_interpolated['SPT'], kind='cubic')

        # New depth values from min to max depth rounded to whole numbers with intervals of 0.1m
        new_depth = np.arange(min(spt_data_interpolated['Depth']), int(max(spt_data_interpolated['Depth'])) + 1, 0.1)

        # Ensure new_depth does not exceed the maximum depth in the provided data
        new_depth = new_depth[new_depth <= max(spt_data_interpolated['Depth'])]

        # Interpolated values
        new_crr = interp_func_crr(new_depth)
        new_csr = interp_func_csr(new_depth)
        new_fines = interp_func_fines(new_depth)
        new_spt = interp_func_spt(new_depth)

        new_crr = np.maximum(new_crr, 0)

        interpolated_data = pd.DataFrame({
            'Borehole': borehole,
            'Depth': new_depth.round(1),
            'Interpolated CRR': np.round(new_crr, decimals=2),
            'Interpolated CSR': np.round(new_csr, decimals=2),
            'Interpolated SPT': np.round(new_spt, decimals=0),
            'Interpolated Fines': np.round(new_fines, decimals=2)
        })

        interpolated_data['Interpolated FOS'] = interpolated_data['Interpolated CRR'] / interpolated_data[
            'Interpolated CSR']
        interpolated_data['Interpolated FOS'] = interpolated_data['Interpolated FOS'].round(2).clip(upper=5.0)

        window_size = 5
        poly_order = 3

        # Smooth CSR, CRR, and FOS columns
        interpolated_data['CSR_smooth'] = savgol_filter(interpolated_data['Interpolated CSR'], window_size, poly_order)
        interpolated_data['CRR_smooth'] = savgol_filter(interpolated_data['Interpolated CRR'], window_size, poly_order)
        interpolated_data['FOS_smooth'] = savgol_filter(interpolated_data['Interpolated FOS'], window_size, poly_order)

        interpolated_data['FOS_smooth'] = interpolated_data['FOS_smooth'].clip(lower=0).clip(upper=5)
        interpolated_data['CRR_smooth'] = interpolated_data['CRR_smooth'].clip(lower=0).clip(upper=2)

        interpolated_data['Volumetric Strain'] = interpolated_data.apply(calculate_volumetric_strain_for_row, axis=1)
        interpolated_data['Settlement'] = (interpolated_data['Volumetric Strain'] / 100) * 0.1
        interpolated_data['Total Settlement'] = (interpolated_data['Settlement'].cumsum()) * 1000

        # Append the interpolated data for the current borehole to the final DataFrame
        all_boreholes_interpolated = pd.concat([all_boreholes_interpolated, interpolated_data], ignore_index=True)

    return all_boreholes_interpolated


def plot_interpolated_output(frame1, frame2, spt_data):
    if spt_data is not None:
        # Clear the existing widgets in the frames
        for widget in frame1.winfo_children():
            widget.destroy()
        for widget in frame2.winfo_children():
            widget.destroy()

        # Update the copy of the DataFrame with interpolated values
        spt_data_interpolated = interpolate_output(spt_data)
        # Group the interpolated data by borehole
        grouped = spt_data_interpolated.groupby('Borehole')

        for borehole, data in grouped:
            # Create a new window for each borehole plot
            plot_window = tk.Toplevel()
            plot_window.title(f'Plots for Borehole {borehole}')

            # Create a figure for CSR/CRR vs Depth
            fig1, ax1 = plt.subplots()
            ax1.plot(data['CRR_smooth'], data['Depth'], '-', label='CRR')
            ax1.plot(data['CSR_smooth'], data['Depth'], '-', label='CSR')
            ax1.plot(data['FOS_smooth'], data['Depth'], '-', label='FOS')
            ax1.set_xlabel('CRR - CSR - FOS')
            ax1.set_ylabel('Depth')
            ax1.invert_yaxis()
            ax1.legend()
            ax1.set_title(f'CSR/CRR vs Depth for Borehole {borehole}')
            canvas1 = FigureCanvasTkAgg(fig1, master=plot_window)
            canvas1.draw()
            canvas1.get_tk_widget().pack()

            # Create a figure for Settlement vs Depth
            fig2, ax2 = plt.subplots()
            ax2.plot(data['Total Settlement'], data['Depth'], '-', label='Settlement')
            ax2.set_xlabel('Settlement (mm)')
            ax2.set_ylabel('Depth')
            ax2.invert_yaxis()
            ax2.legend()
            ax2.set_title(f'Settlement vs Depth for Borehole {borehole}')
            canvas2 = FigureCanvasTkAgg(fig2, master=plot_window)
            canvas2.draw()
            canvas2.get_tk_widget().pack()
    else:
        messagebox.showerror("Error", "Failed to load SPT or CPT data.")

