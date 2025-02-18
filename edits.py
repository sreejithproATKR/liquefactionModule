def calculate_gamma_d(self, depth):
    # Example equations for gamma_d based on depth ranges
    if depth <= 9.15:
        gamma_d = 1.0 - 0.00765 * depth
    elif depth <= 23:
        gamma_d = 1.174 - 0.0267 * depth
    elif depth <= 30:
        gamma_d = 0.744 - 0.008 * depth
    else:
        gamma_d = 0.5
    return gamma_d

# Add radio buttons for Energy Ratio of SPT
energy_ratio_label = ttk.Label(spt_left_frame, text="Type of Hammer:")
energy_ratio_label.grid(row=0, column=1, padx=5, pady=5, sticky='w')

energy_ratio_var = tk.StringVar()
energy_ratio_var.set("Safety Hammer")

safety_hammer_rb = ttk.Radiobutton(spt_left_frame, text="Safety Hammer", variable=energy_ratio_var,
                                   value="Safety Hammer")
safety_hammer_rb.grid(row=1, column=1, padx=5, pady=5, sticky='w')

donut_hammer_rb = ttk.Radiobutton(spt_left_frame, text="Donut Hammer", variable=energy_ratio_var, value="Donut Hammer")
donut_hammer_rb.grid(row=2, column=1, padx=5, pady=5, sticky='w')

automatic_trip_rb = ttk.Radiobutton(spt_left_frame, text="Automatic Trip", variable=energy_ratio_var,
                                    value="Automatic Trip")
automatic_trip_rb.grid(row=3, column=1, padx=5, pady=5, sticky='w')

# Add radio buttons for Borehole Diameter
borehole_diameter_label = ttk.Label(spt_left_frame, text="Borehole Diameter:")
borehole_diameter_label.grid(row=0, column=2, padx=5, pady=5, sticky='w')

borehole_diameter_var = tk.StringVar()
borehole_diameter_var.set("65mm to 115mm")

diameter_65_115_rb = ttk.Radiobutton(spt_left_frame, text="65mm to 115mm", variable=borehole_diameter_var,
                                     value="65mm to 115mm")
diameter_65_115_rb.grid(row=1, column=2, padx=5, pady=5, sticky='w')

diameter_150_rb = ttk.Radiobutton(spt_left_frame, text="150mm", variable=borehole_diameter_var, value="150mm")
diameter_150_rb.grid(row=2, column=2, padx=5, pady=5, sticky='w')

diameter_200_rb = ttk.Radiobutton(spt_left_frame, text="200mm", variable=borehole_diameter_var, value="200mm")
diameter_200_rb.grid(row=3, column=2, padx=5, pady=5, sticky='w')

# Add radio buttons for Rod Length
rod_length_label = ttk.Label(spt_left_frame, text="Rod Length:")
rod_length_label.grid(row=0, column=3, padx=5, pady=5, sticky='w')

rod_length_var = tk.StringVar()
rod_length_var.set("3 m to 4 m")

rod_length_3_4_rb = ttk.Radiobutton(spt_left_frame, text="3 m to 4 m", variable=rod_length_var, value="3 m to 4 m")
rod_length_3_4_rb.grid(row=1, column=3, padx=5, pady=5, sticky='w')

rod_length_4_6_rb = ttk.Radiobutton(spt_left_frame, text="4 m to 6 m", variable=rod_length_var, value="4 m to 6 m")
rod_length_4_6_rb.grid(row=2, column=3, padx=5, pady=5, sticky='w')

rod_length_6_10_rb = ttk.Radiobutton(spt_left_frame, text="6 m to 10 m", variable=rod_length_var, value="6 m to 10 m")
rod_length_6_10_rb.grid(row=3, column=3, padx=5, pady=5, sticky='w')

rod_length_10_30_rb = ttk.Radiobutton(spt_left_frame, text="10 m to 30 m", variable=rod_length_var,
                                      value="10 m to 30 m")
rod_length_10_30_rb.grid(row=4, column=3, padx=5, pady=5, sticky='w')

rod_length_30_rb = ttk.Radiobutton(spt_left_frame, text=">30 m", variable=rod_length_var, value=">30 m")
rod_length_30_rb.grid(row=5, column=3, padx=5, pady=5, sticky='w')


#___________Backup of spt_data.py_________________________________

import pandas as pd
from tkinter import filedialog, messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from CRR_Class import calculate_crr
from CSR_Class import calculate_csr


def add_crr_column(df):
    df['CRR'] = df['SPT'].apply(lambda x: calculate_crr(x))
    return df



# def add_crr_column(df):
#     df['CSR'] = df['SPT'].apply(lambda x: calculate_csr(x))
#     return df


# def export_spt_data(spt_data):
#     file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
#     if file_path:
#         try:
#             if file_path.endswith('.csv'):
#                 spt_data.to_csv(file_path, index=False)
#             else:
#                 spt_data.to_excel(file_path, index=False, engine='openpyxl')
#             messagebox.showinfo("Export Successful", f"SPT data exported successfully to {file_path}")
#         except Exception as e:
#             messagebox.showerror("Export Error", f"An error occurred while exporting the data: {e}")

def preview_spt_data(spt_data, spt_preview_frame):
    for widget in spt_preview_frame.winfo_children():
        widget.destroy()
    tree = ttk.Treeview(spt_preview_frame)
    tree["columns"] = list(spt_data.columns)
    tree["show"] = "headings"

    for column in spt_data.columns:
        tree.heading(column, text=column)
        tree.column(column, width=100)

    for index, row in spt_data.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(fill="both", expand=True)

# def load_spt_data(spt_preview_frame):
#     global spt_data
#     file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"),("CSV files", "*.csv")])
#     if file_path:
#         try:
#             if file_path.endswith('.csv'):
#                 spt_data = pd.read_csv(file_path)
#             else:
#                 spt_data = pd.read_excel(file_path, engine='openpyxl')
#             preview_spt_data(spt_data, spt_preview_frame)
#         except Exception as e:
#             messagebox.showerror("Load Error", f"An error occurred while loading the data: {e}")

def load_spt_data(spt_preview_frame, unit_weight_water, water_table_depth):
    global spt_data
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"),("CSV files", "*.csv")])
    if file_path:
        try:
            if file_path.endswith('.csv'):
                spt_data = pd.read_csv(file_path)
            else:
                spt_data = pd.read_excel(file_path, engine='openpyxl')

            # Calculate Total Weight and Effective Unit Weight

            spt_data['Total Stress'] = round(spt_data['Depth'] * spt_data['Gamma'],1)
            spt_data['Effective Stress'] = spt_data.apply(
                lambda row: round(row['Gamma'] * row['Depth'],1) if row['Depth'] <= water_table_depth else round(row['Gamma']* water_table_depth + (row['Depth'] - water_table_depth) * (row['Gamma'] - unit_weight_water),1), axis=1)

            preview_spt_data(spt_data, spt_preview_frame)
        except Exception as e:
            messagebox.showerror("Load Error", f"An error occurred while loading the data: {e}")

def add_csr_column(df, a_max):
    df['CSR'] = df['Depth'].apply(lambda row: calculate_csr(row['Depth'],row['Total Stress'],row['Effective Stress'], a_max))
    return df


def calculate_and_preview_crr(spt_preview_frame):
    global spt_data
    try:
        spt_data = add_crr_column(spt_data)

        preview_spt_data(spt_data, spt_preview_frame)
    except Exception as e:
        messagebox.showerror("Calculation Error", f"An error occurred while calculating CRR: {e}")

def calculate_and_preview_csr(spt_preview_frame,a_max):
    global spt_data
    try:
        spt_data = add_csr_column(spt_data,a_max)

        preview_spt_data(spt_data, spt_preview_frame)
    except Exception as e:
        messagebox.showerror("Calculation Error", f"An error occurred while calculating CRR: {e}")

def plot_crr_graph(plot_frame):
    global spt_data
    if 'Depth' not in spt_data.columns:
        messagebox.showerror("Plot Error", "The SPT data does not contain a 'Depth' column.")
        return

    depths = spt_data['Depth']
    crr_values = spt_data['CRR']

    fig, ax = plt.subplots()
    ax.plot(crr_values, depths)
    ax.set_xlabel('CRR')
    ax.set_ylabel('Depth (m)')
    ax.invert_yaxis()  # Invert y-axis to have depth increasing downwards

    for widget in plot_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


# Initialize global variable for SPT data
spt_data = pd.DataFrame()

#___________Backup of csr_calculation.py_________________________________

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def calculate_gamma_d(depth):
    # Example equations for gamma_d based on depth ranges
    if depth <= 9.15:
        gamma_d = 1.0 - 0.00765 * depth
    elif depth <= 23:
        gamma_d = 1.174 - 0.0267 * depth
    elif depth <= 30:
        gamma_d = 0.744 - 0.008 * depth
    else:
        gamma_d = 0.5
    return gamma_d

def calculate_csr(depth, sig_0, sig_1, a_max):
    gamma_d = self.calculate_gamma_d(depth)
    # CSR calculation using the provided formula
    csr = 0.65 * (sig_0 / sig_1) * a_max * gamma_d
    return csr

def plot_graph(csr_values, soil_layers, water_table_depth, right_frame):
    depths, csrs = zip(*csr_values)

    fig, ax = plt.subplots()
    ax.plot(csrs, depths)
    ax.set_xlabel('CSR')
    ax.set_ylabel('Depth (m)')
    ax.invert_yaxis()  # Invert y-axis to have depth increasing downwards

    # Draw lines on top of each soil layer and mark the water table depth in dotted blue lines.
    accumulated_depth = 0
    for layer in soil_layers:
        accumulated_depth += layer.thickness
        ax.axhline(y=accumulated_depth, color='black', linestyle='-')

    ax.axhline(y=water_table_depth, color='blue', linestyle='--', label='Water Table Depth')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

