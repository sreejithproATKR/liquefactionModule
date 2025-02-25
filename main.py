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

# Create input fields for soil layers in the left frame
thickness_entries = []
total_unit_weight_entries = []

# default_thickness = [2.5, 8.5, 8.0, 2.5]
# default_unit_weight = [18, 17, 16, 17]
default_unit_weight_water = 10.0
default_a_max = 1.5
default_water_table_depth = 2.5
default_eq_mag = 5.0
default_msf = 1.0
default_manual_fs = 1.0

# Create input field for unit weight of water in the left frame
ttk.Label(left_frame, text="Unit Weight of Water (kN/m³):").grid(row=1, column=0, padx=5, pady=5, sticky = 'w')
unit_weight_water_entry = ttk.Entry(left_frame)
unit_weight_water_entry.grid(row=1, column=1, padx=5, pady=5, sticky = 'w')
unit_weight_water_entry.insert(0, str(default_unit_weight_water))
unit_weight_water = float(unit_weight_water_entry.get())



# Create input field for water table depth in the left frame
ttk.Label(left_frame, text="Water Table Depth (m):").grid(row=2, column=0, padx=5, pady=5, sticky = 'w')
water_table_depth_entry = ttk.Entry(left_frame)
water_table_depth_entry.grid(row=2, column=1, padx=5, pady=5, sticky = 'w')
water_table_depth_entry.insert(0, str(default_water_table_depth))
water_table_depth = float(water_table_depth_entry.get())

# Create input field for a_max in the left frame
ttk.Label(left_frame, text="Peak Horizontal Acceleration (a_max):").grid(row=3, column=0, padx=5, pady=5, sticky = 'w')
a_max_entry = ttk.Entry(left_frame)
a_max_entry.grid(row=3, column=1, padx=5, pady=5, sticky = 'w')
a_max_entry.insert(0, str(default_a_max))
a_max = float(a_max_entry.get())

# Create input field for magnitude in the left frame
ttk.Label(left_frame, text="Earthquake Magnitude:").grid(row=4, column=0, padx=5, pady=5, sticky = 'w')
eq_mag_entry = ttk.Entry(left_frame)
eq_mag_entry.grid(row=4, column=1, padx=5, pady=5, sticky = 'w')
eq_mag_entry.insert(0, str(default_eq_mag))
eq_mag = float(eq_mag_entry.get())

# Create input field for magnitude in the left frame
ttk.Label(left_frame, text="or Magnitude Correction Factor (MSF):").grid(row=4, column=2, padx=5, pady=5, sticky = 'w')
msf_entry = ttk.Entry(left_frame)
msf_entry.grid(row=4, column=3, padx=5, pady=5, sticky = 'w')
msf_entry.insert(0, str(default_msf))
msf = float(eq_mag_entry.get())

# Create input field for Manual FS in the left frame
ttk.Label(left_frame, text="Manual Factor of Safety:").grid(row=5, column=0, padx=5, pady=5, sticky = 'w')
manual_fs_entry = ttk.Entry(left_frame)
manual_fs_entry.grid(row=5, column=1, padx=5, pady=5, sticky = 'w')
manual_fs_entry.insert(0, str(default_manual_fs))
manual_fs = float(manual_fs_entry.get())

# Add radio buttons for selecting SPT or CPT data
data_type_label = ttk.Label(left_frame, text="Select Data Type:")
data_type_label.grid(row=1, column=2, padx=5, pady=5, sticky='w')

data_type_var = tk.StringVar()
data_type_var.set("SPT")

def toggle_tabs():
    if data_type_var.get() == "SPT":
        notebook.tab(spt_details_frame, state="normal")
        notebook.tab(cpt_details_frame, state="hidden")
    else:
        notebook.tab(spt_details_frame, state="hidden")
        notebook.tab(cpt_details_frame, state="normal")

toggle_tabs()  # Initialize the tabs based on the default selection

spt_rb = ttk.Radiobutton(left_frame, text="SPT Data", variable=data_type_var, value="SPT", command=lambda: toggle_tabs())
spt_rb.grid(row=2, column=2, padx=5, pady=5, sticky='w')

cpt_rb = ttk.Radiobutton(left_frame, text="CPT Data", variable=data_type_var, value="CPT", command=lambda: toggle_tabs())
cpt_rb.grid(row=3, column=2, padx=5, pady=5, sticky='w')

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
tree = ttk.Treeview(spt_preview_frame,columns='Four')
tree.pack(fill="both", expand=True)

# Add radio buttons for Energy Ratio of SPT
energy_ratio_label = ttk.Label(spt_left_frame, text="Type of Hammer:")
energy_ratio_label.grid(row=0, column=1, padx=5, pady=5, sticky='w')

energy_ratio_var = tk.StringVar()
energy_ratio_var.set("0.89")

safety_hammer_rb = ttk.Radiobutton(spt_left_frame, text="Safety Hammer", variable=energy_ratio_var,
                                   value="0.89")
safety_hammer_rb.grid(row=1, column=1, padx=5, pady=5, sticky='w')

donut_hammer_rb = ttk.Radiobutton(spt_left_frame, text="Donut Hammer", variable=energy_ratio_var, value="0.73")
donut_hammer_rb.grid(row=2, column=1, padx=5, pady=5, sticky='w')

automatic_trip_rb = ttk.Radiobutton(spt_left_frame, text="Automatic Trip", variable=energy_ratio_var,
                                    value="1.25")
automatic_trip_rb.grid(row=3, column=1, padx=5, pady=5, sticky='w')

# Debugging function to print the current value of energy_ratio_var

# Variable to hold the energy ratio value
henergy_c = float(energy_ratio_var.get())
# Function to update henergy_c
def update_henergy_c(*args):
    global henergy_c
    henergy_c = float(energy_ratio_var.get())
# Trace the variable to call update_henergy_c whenever it changes
energy_ratio_var.trace_add("write", update_henergy_c)



# Add radio buttons for Borehole Diameter
borehole_diameter_label = ttk.Label(spt_left_frame, text="Borehole Diameter:")
borehole_diameter_label.grid(row=0, column=2, padx=5, pady=5, sticky='w')

borehole_diameter_var = tk.StringVar()
borehole_diameter_var.set("1.0")

diameter_65_115_rb = ttk.Radiobutton(spt_left_frame, text="65mm to 115mm", variable=borehole_diameter_var,
                                     value="1.0")
diameter_65_115_rb.grid(row=1, column=2, padx=5, pady=5, sticky='w')

diameter_150_rb = ttk.Radiobutton(spt_left_frame, text="150mm", variable=borehole_diameter_var, value="1.05")
diameter_150_rb.grid(row=2, column=2, padx=5, pady=5, sticky='w')

diameter_200_rb = ttk.Radiobutton(spt_left_frame, text="200mm", variable=borehole_diameter_var, value="1.15")
diameter_200_rb.grid(row=3, column=2, padx=5, pady=5, sticky='w')

boreholed_c = float(borehole_diameter_var.get())
# Function to update boreholed_c
def update_boreholed_c(*args):
    global boreholed_c
    boreholed_c = float(borehole_diameter_var.get())
# Trace the variable to call update_boreholed_c whenever it changes
borehole_diameter_var.trace_add("write", update_boreholed_c)

# # Add radio buttons for Rod Length
# rod_length_label = ttk.Label(spt_left_frame, text="Rod Length:")
# rod_length_label.grid(row=0, column=3, padx=5, pady=5, sticky='w')
#
# rod_length_var = tk.StringVar()
# rod_length_var.set("0.75")
#
# rod_length_3_4_rb = ttk.Radiobutton(spt_left_frame, text="3 m to 4 m", variable=rod_length_var, value="0.75")
# rod_length_3_4_rb.grid(row=1, column=3, padx=5, pady=5, sticky='w')
#
# rod_length_4_6_rb = ttk.Radiobutton(spt_left_frame, text="4 m to 6 m", variable=rod_length_var, value="0.85")
# rod_length_4_6_rb.grid(row=2, column=3, padx=5, pady=5, sticky='w')
#
# rod_length_6_10_rb = ttk.Radiobutton(spt_left_frame, text="6 m to 10 m", variable=rod_length_var, value="0.95")
# rod_length_6_10_rb.grid(row=3, column=3, padx=5, pady=5, sticky='w')
#
# rod_length_10_30_rb = ttk.Radiobutton(spt_left_frame, text="10 m to 30 m", variable=rod_length_var,
#                                       value="1.0")
# rod_length_10_30_rb.grid(row=4, column=3, padx=5, pady=5, sticky='w')
#
# rod_length_30_rb = ttk.Radiobutton(spt_left_frame, text=">30 m", variable=rod_length_var, value="0.9")
# rod_length_30_rb.grid(row=5, column=3, padx=5, pady=5, sticky='w')
#
# def disable_entry(entry):
#     entry.config(state="disabled")
#
# # Add the "Specify" radio button and the text input
# specify_entry = ttk.Entry(spt_left_frame)
# specify_entry.grid(row=7, column=3, padx=5, pady=5, sticky='w')
# specify_entry.insert(0, "0.5")
# disable_entry(specify_entry)
#
#
#
# def enable_text_input():
#     specify_entry.config(state='normal')
#
#
# specify_rb = ttk.Radiobutton(spt_left_frame, text="Specify", variable=rod_length_var, value=specify_entry.get(), command=enable_text_input())
# specify_rb.grid(row=6, column=3, padx=5, pady=5, sticky='w')
#
#
#
# # if rod_length_var == "specify":
# #     rod_length_c = float(specify_entry.get())
# # else:
# #     rod_length_c = float(rod_length_var.get())
# # Function to update rod_length_c
# rod_length_c = float(rod_length_var.get())
# def update_rod_length_c(*args):
#     global rod_length_c
#     rod_length_c = float(rod_length_var.get())
#     print(rod_length_c)
# # Trace the variable to call update_rod_length_c whenever it changes
# rod_length_var.trace_add("write", update_rod_length_c)

# Add radio buttons for Fines Correction
fines_correction_label = ttk.Label(spt_left_frame, text="Fines Correction:")
fines_correction_label.grid(row=0, column=4, padx=5, pady=5, sticky='w')

fines_correction_var = tk.StringVar()
fines_correction_var.set("No Correction")

no_correction_rb = ttk.Radiobutton(spt_left_frame, text="No Correction", variable=fines_correction_var,
                                     value="No Correction")
no_correction_rb.grid(row=1, column=4, padx=5, pady=5, sticky='w')

idriss_seed_rb = ttk.Radiobutton(spt_left_frame, text="Idriss & Seed, 1997", variable=fines_correction_var,
                                     value="Idriss & Seed, 1997")
idriss_seed_rb.grid(row=2, column=4, padx=5, pady=5, sticky='w')

stark_olsen_rb = ttk.Radiobutton(spt_left_frame, text="Stark & Olsen, 1995", variable=fines_correction_var, value="Stark & Olsen, 1995")
stark_olsen_rb.grid(row=3, column=4, padx=5, pady=5, sticky='w')

mstark_olsen_rb = ttk.Radiobutton(spt_left_frame, text="Modified Stark & Olsen", variable=fines_correction_var, value="Modified Stark & Olsen")
mstark_olsen_rb.grid(row=4, column=4, padx=5, pady=5, sticky='w')

fines_correction_type = fines_correction_var.get()
# Function to update fines_correction_type
def update_fines_correction_type(*args):
    global fines_correction_type
    fines_correction_type = fines_correction_var.get()
    print(fines_correction_type)
# Trace the variable to call update_fines_correction_type whenever it changes
fines_correction_var.trace_add("write", update_fines_correction_type)



# Add radio buttons for Sampler Correction
sampler_correction_label = ttk.Label(spt_left_frame, text="Sampler Correction:")
sampler_correction_label.grid(row=0, column=3, padx=5, pady=5, sticky='w')

sampler_correction_var = tk.StringVar()
sampler_correction_var.set("1.0")

standard_sampler_rb = ttk.Radiobutton(spt_left_frame, text="Standard Sampler", variable=sampler_correction_var,
                                     value="1.0")
standard_sampler_rb.grid(row=1, column=3, padx=5, pady=5, sticky='w')

standard_sampler_liner_rb = ttk.Radiobutton(spt_left_frame, text="Sampler Without Liners", variable=sampler_correction_var,
                                     value="1.2")
standard_sampler_liner_rb.grid(row=2, column=3, padx=5, pady=5, sticky='w')


sampler_c = float(sampler_correction_var.get())
# Function to update sampler_c
def update_sampler_c(*args):
    global sampler_c
    sampler_c = float(sampler_correction_var.get())
# Trace the variable to call update_sampler_c whenever it changes
sampler_correction_var.trace_add("write", update_sampler_c)




# Create buttons to load and export SPT data in the left frame of SPT details tab
load_button = ttk.Button(spt_left_frame, text="Load SPT Data", command=lambda: load_spt_data_with_dialog(spt_preview_frame))
load_button.grid(row=0, column=0, padx=5, pady=5)

# Create a button to calculate CSR
calculate_csr_button = ttk.Button(spt_left_frame, text="Calculate CSR", command=lambda: calculate_and_preview_csr(spt_preview_frame, spt_data,
                                                                                                                  float(unit_weight_water_entry.get()),
                                                                                                                  float(water_table_depth_entry.get()),
                                                                                                                  float(a_max_entry.get()),float(manual_fs_entry.get())))
calculate_csr_button.grid(row=1, column=0, padx=5, pady=5, sticky='w')

calculate_crr_button = ttk.Button(spt_left_frame, text="Calculate CRR", command=lambda: calculate_and_preview_crr(spt_preview_frame, spt_data,
                                                                                                                  float(unit_weight_water_entry.get()),
                                                                                                                  float(water_table_depth_entry.get()),
                                                                                                                  henergy_c,boreholed_c, sampler_c, fines_correction_type,float(eq_mag_entry.get())))
calculate_crr_button.grid(row=2, column=0, padx=5, pady=5, sticky='w')

# Create a button to plot CRR vs Depth and CSR vs Depth
plot_button = ttk.Button(spt_left_frame, text="Plot", command=lambda: plot_crr_csr_vs_depth(spt_rightB_frame, spt_data))
plot_button.grid(row=3, column=0, padx=5, pady=5, sticky='w')

export_button = ttk.Button(spt_left_frame, text="Export", command=lambda: plot_crr_csr_vs_depth(spt_rightB_frame, spt_data))
export_button.grid(row=4, column=0, padx=5, pady=5, sticky='w')
# Run the application

# sv_ttk.set_theme("dark")
root.mainloop()