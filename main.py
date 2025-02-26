import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from spt_data import (preview_spt_data, calculate_and_preview_csr, calculate_and_preview_crr, load_spt_data_from_excel,
                      plot_crr_csr_vs_depth)

# Global variable to store SPT data
spt_data = None

# Function to open file dialog and load SPT data
def load_spt_data_with_dialog(frame):
    global spt_data
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:
        spt_data = load_spt_data_from_excel(file_path)
        preview_spt_data(frame, spt_data)

# Create the main window
root = tk.Tk()
root.title("AtkinsRéalis - Soil Liquefaction Analysis")

# Create a notebook for tabs
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=10, pady=10)

# Create frames for the tabs
general_frame = ttk.Frame(notebook)
spt_details_frame = ttk.Frame(notebook)
cpt_details_frame = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(general_frame, text="General")
notebook.add(spt_details_frame, text="SPT Details")
notebook.add(cpt_details_frame, text="CPT Details")

# Create frames for left and right columns in the ground model tab
left_frame = ttk.Frame(general_frame)
left_frame.grid(row=0, column=0, padx=10, pady=10)
right_frame = ttk.Frame(general_frame)
right_frame.grid(row=0, column=1, padx=10, pady=10)

default_unit_weight_water = 10.0
default_a_max = 0.25
default_water_table_depth = 0.0
default_eq_mag = 7.5
default_msf = 1.0
default_manual_fs = 1.0

# Create input field for unit weight of water in the left frame
ttk.Label(left_frame, text="Unit Weight of Water (kN/m³):").grid(row=1, column=0, padx=5, pady=5, sticky='w')
unit_weight_water_entry = ttk.Entry(left_frame)
unit_weight_water_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
unit_weight_water_entry.insert(0, str(default_unit_weight_water))
unit_weight_water = float(unit_weight_water_entry.get())

# Create input field for water table depth in the left frame
ttk.Label(left_frame, text="Water Table Depth (m):").grid(row=2, column=0, padx=5, pady=5, sticky='w')
water_table_depth_entry = ttk.Entry(left_frame)
water_table_depth_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
water_table_depth_entry.insert(0, str(default_water_table_depth))
water_table_depth = float(water_table_depth_entry.get())

# Create input field for a_max in the left frame
ttk.Label(left_frame, text="Peak Horizontal Acceleration (a_max):").grid(row=3, column=0, padx=5, pady=5, sticky='w')
a_max_entry = ttk.Entry(left_frame)
a_max_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
a_max_entry.insert(0, str(default_a_max))
a_max = float(a_max_entry.get())

# Create input field for magnitude in the left frame
ttk.Label(left_frame, text="Earthquake Magnitude:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
eq_mag_entry = ttk.Entry(left_frame)
eq_mag_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')
eq_mag_entry.insert(0, str(default_eq_mag))
eq_mag = float(eq_mag_entry.get())

# Create input field for magnitude in the left frame
ttk.Label(left_frame, text="or Magnitude Correction Factor (MSF):").grid(row=4, column=2, padx=5, pady=5, sticky='w')
msf_entry = ttk.Entry(left_frame)
msf_entry.grid(row=4, column=3, padx=5, pady=5, sticky='w')
msf_entry.insert(0, str(default_msf))
msf = float(eq_mag_entry.get())

# Create input field for Manual FS in the left frame
ttk.Label(left_frame, text="Manual Factor of Safety:").grid(row=5, column=0, padx=5, pady=5, sticky='w')
manual_fs_entry = ttk.Entry(left_frame)
manual_fs_entry.grid(row=5, column=1, padx=5, pady=5, sticky='w')
manual_fs_entry.insert(0, str(default_manual_fs))
manual_fs = float(manual_fs_entry.get())

# Add Combobox for selecting SPT or CPT data
data_type_label = ttk.Label(left_frame, text="Select Data Type:")
data_type_label.grid(row=1, column=2, padx=5, pady=5, sticky='w')
data_type_var = tk.StringVar()
data_type_combobox = ttk.Combobox(left_frame, textvariable=data_type_var,state='readonly')
data_type_combobox['values'] = ("SPT", "CPT")
data_type_combobox.current(0)  # Set default value to "SPT"
data_type_combobox.grid(row=2, column=2, padx=10, pady=10, sticky='w')

def toggle_tabs(*args):
    if data_type_var.get() == "SPT":
        notebook.tab(spt_details_frame, state="normal")
        notebook.tab(cpt_details_frame, state="hidden")
    else:
        notebook.tab(spt_details_frame, state="hidden")
        notebook.tab(cpt_details_frame, state="normal")

data_type_var.trace("w", toggle_tabs)  # Trace changes to data_type_var

toggle_tabs()  # Initialize the tabs based on the default selection

# Create frames for left and right columns in the SPT details tab
spt_left_frame = ttk.Frame(spt_details_frame)
spt_left_frame.grid(row=0, column=0, padx=10, pady=10)
spt_right_frame = ttk.Frame(spt_details_frame)
spt_right_frame.grid(row=0, column=1, padx=10, pady=10)
spt_rightB_frame = ttk.Frame(spt_details_frame)
spt_rightB_frame.grid(row=1, column=1, padx=10, pady=10)

# Create a frame to preview SPT data in the right frame of SPT details tab
spt_preview_frame = ttk.Frame(spt_right_frame)
spt_preview_frame.pack(fill="both", expand=True)
tree = ttk.Treeview(spt_preview_frame, columns='Four')
tree.pack(fill="both", expand=True)

# Add Combobox for Energy Ratio of SPT
energy_ratio_label = ttk.Label(spt_left_frame, text="Type of Hammer:")
energy_ratio_label.grid(row=0, column=1, padx=5, pady=5, sticky='w')
energy_ratio_var = tk.StringVar()
energy_ratio_combobox = ttk.Combobox(spt_left_frame, textvariable=energy_ratio_var,state='readonly')
energy_ratio_combobox['values'] = ("Safety Hammer", "Donut Hammer", "Automatic Trip")
energy_ratio_combobox.current(0)  # Set default value
energy_ratio_combobox.grid(row=1, column=1, padx=5, pady=5, sticky='w')


# Mapping for energy ratio values
energy_ratio_mapping = {
    "Safety Hammer": 1.0,
    "Donut Hammer": 0.73,
    "Automatic Trip": 1.25
}


# Variable to hold the energy ratio value
henergy_c = energy_ratio_mapping[energy_ratio_var.get()]

# Function to update henergy_c
def update_henergy_c(*args):
    global henergy_c
    henergy_c = energy_ratio_mapping[energy_ratio_var.get()]

# Trace the variable to call update_henergy_c whenever it changes
energy_ratio_var.trace_add("write", update_henergy_c)

# Add Combobox for Borehole Diameter
borehole_diameter_label = ttk.Label(spt_left_frame, text="Borehole Diameter:")
borehole_diameter_label.grid(row=0, column=2, padx=5, pady=5, sticky='w')
borehole_diameter_var = tk.StringVar()
borehole_diameter_combobox = ttk.Combobox(spt_left_frame, textvariable=borehole_diameter_var,state='readonly')
borehole_diameter_combobox['values'] = ("65mm to 115mm", "150mm", "200mm")
borehole_diameter_combobox.current(0)  # Set default value
borehole_diameter_combobox.grid(row=1, column=2, padx=5, pady=5, sticky='w')

# Variable to hold the borehole diameter value
# Mapping for borehole diameter values
borehole_diameter_mapping = {
    "65mm to 115mm": 1.0,
    "150mm": 1.05,
    "200mm": 1.15
}

# Variable to hold the borehole diameter value
boreholed_c = borehole_diameter_mapping[borehole_diameter_var.get()]

# Function to update boreholed_c
def update_boreholed_c(*args):
    global boreholed_c
    boreholed_c = borehole_diameter_mapping[borehole_diameter_var.get()]

# Trace the variable to call update_boreholed_c whenever it changes
borehole_diameter_var.trace_add("write", update_boreholed_c)

# Add Combobox for Fines Correction
fines_correction_label = ttk.Label(spt_left_frame, text="Fines Correction:")
fines_correction_label.grid(row=0, column=4, padx=5, pady=5, sticky='w')
fines_correction_var = tk.StringVar()
fines_correction_combobox = ttk.Combobox(spt_left_frame, textvariable=fines_correction_var,state='readonly')
fines_correction_combobox['values'] = ("No Correction", "Idriss & Seed, 1997", "Stark & Olsen, 1995", "Modified Stark & Olsen")
fines_correction_combobox.current(1)  # Set default value
fines_correction_combobox.grid(row=1, column=4, padx=5, pady=5, sticky='w')

# Mapping for fines correction values
fines_correction_mapping = {
    "No Correction": "No Correction",
    "Idriss & Seed, 1997": "Idriss & Seed, 1997",
    "Stark & Olsen, 1995": "Stark & Olsen, 1995",
    "Modified Stark & Olsen": "Modified Stark & Olsen"
}

# Variable to hold the fines correction type
fines_correction_type = fines_correction_mapping[fines_correction_var.get()]

# Function to update fines_correction_type
def update_fines_correction_type(*args):
    global fines_correction_type
    fines_correction_type = fines_correction_mapping[fines_correction_var.get()]

# Trace the variable to call update_fines_correction_type whenever it changes
fines_correction_var.trace_add("write", update_fines_correction_type)

# Add Combobox for Sampler Correction
sampler_correction_label = ttk.Label(spt_left_frame, text="Sampler Correction:")
sampler_correction_label.grid(row=0, column=3, padx=5, pady=5, sticky='w')
sampler_correction_var = tk.StringVar()
sampler_correction_combobox = ttk.Combobox(spt_left_frame, textvariable=sampler_correction_var)
sampler_correction_combobox['values'] = ("Standard Sampler", "Sampler Without Liners")
sampler_correction_combobox.current(0)  # Set default value
sampler_correction_combobox.grid(row=1, column=3, padx=5, pady=5, sticky='w')

# Mapping for sampler correction values
sampler_correction_mapping = {
    "Standard Sampler": 1.0,
    "Sampler Without Liners": 1.2
}

# Variable to hold the sampler correction value
sampler_c = sampler_correction_mapping[sampler_correction_var.get()]

# Function to update sampler_c
def update_sampler_c(*args):
    global sampler_c
    sampler_c = sampler_correction_mapping[sampler_correction_var.get()]

# Trace the variable to call update_sampler_c whenever it changes
sampler_correction_var.trace_add("write", update_sampler_c)

# Add Checkbutton for Overburden Correction
overburden_corr_val = tk.IntVar()
overburden_corr_val.set(0)
overburden_corr_tick = ttk.Checkbutton(spt_left_frame, text="Set Overburden", variable=overburden_corr_val)
overburden_corr_tick.grid(row=4, column=1, padx=5, pady=0, sticky='w')

# Variable to hold the overburden correction value
overburden_corr_cap = overburden_corr_val.get()

# Function to update overburden_corr_cap
def set_overburden_corr_val(*args):
    global overburden_corr_cap
    if overburden_corr_val.get():
        overburden_corr_cap = 1
        print(overburden_corr_cap)
    else:
        overburden_corr_cap = 0

# Trace the variable to call set_overburden_corr_val whenever it changes
overburden_corr_val.trace_add("write", set_overburden_corr_val)


# Create buttons to load and export SPT data in the left frame of SPT details tab
load_button = ttk.Button(spt_left_frame, text="Load SPT Data", command=lambda: load_spt_data_with_dialog(spt_preview_frame))
load_button.grid(row=0, column=0, padx=5, pady=5)

# Create a button to calculate CSR
calculate_csr_button = ttk.Button(spt_left_frame, text="Calculate CSR", command=lambda: calculate_and_preview_csr(spt_preview_frame, spt_data,
    float(unit_weight_water_entry.get()),
    float(water_table_depth_entry.get()),
    float(a_max_entry.get()), float(manual_fs_entry.get())))
calculate_csr_button.grid(row=1, column=0, padx=5, pady=5, sticky='w')

# Create a button to calculate CRR
calculate_crr_button = ttk.Button(spt_left_frame, text="Calculate CRR", command=lambda: calculate_and_preview_crr(spt_preview_frame, spt_data,
    float(unit_weight_water_entry.get()),
    float(water_table_depth_entry.get()),
    henergy_c, boreholed_c, sampler_c, fines_correction_type, float(eq_mag_entry.get()), overburden_corr_cap))
calculate_crr_button.grid(row=2, column=0, padx=5, pady=5, sticky='w')

# Create a button to plot CRR vs Depth and CSR vs Depth
plot_button = ttk.Button(spt_left_frame, text="Plot", command=lambda: plot_crr_csr_vs_depth(spt_rightB_frame, spt_data))
plot_button.grid(row=3, column=0, padx=5, pady=5, sticky='w')

# Create a button to export the data
export_button = ttk.Button(spt_left_frame, text="Export", command=lambda: plot_crr_csr_vs_depth(spt_rightB_frame, spt_data))
export_button.grid(row=4, column=0, padx=5, pady=5, sticky='w')

# Run the application
root.mainloop()