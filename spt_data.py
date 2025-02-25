import pandas as pd
from tkinter import ttk, messagebox
from CSR_Class import CSR
from CRR_Class import CRR
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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


def calculate_and_preview_csr(frame, spt_data, unit_weight_water, water_table_depth, peak_acceleration,manual_fs):
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
            csr_calculator = CSR(depth, gamma, unit_weight_water, peak_acceleration, water_table_depth, current_sigma_1, current_sigma_0,current_depth,manual_fs)
            current_sigma_1,current_sigma_0, csr_value = csr_calculator.calculate_csr()
            csr_values.append(csr_value)
            current_depth = depth

        spt_data["CSR"] = csr_values

        # Preview the updated SPT data with CSR values
        preview_spt_data(frame, spt_data)
    else:
        messagebox.showerror("Error", "Failed to load SPT data.")


def calculate_and_preview_crr(frame, spt_data, unit_weight_water, water_table_depth, henergy_c, borehole_diameter_var, sampler_c, fines_correction_type, eq_magnitude):
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
            crr_calculator = CRR("SPT", depth, 0, water_table_depth, gamma,eq_magnitude, unit_weight_water,henergy_c,borehole_diameter_var,
                                 sampler_c,fines_content,fines_correction_type, spt_n_value)
            crr_value = crr_calculator.calculate_crr_spt()
            crr_values.append(crr_value)

        spt_data["CRR"] = crr_values

        # Preview the updated SPT data with CSR values
        preview_spt_data(frame, spt_data)
        print(eq_magnitude)
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

    def export_crr_csr(spt_data_):


        pass

