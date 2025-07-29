import pandapower as pp
import matplotlib.pyplot as plt 
import threading
import time
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.colors as mcolors

# Create a power network
net=pp.create_empty_network()
# Add buses to the network
b1=pp.create_bus(net , vn_kv=132 ,name ="Slack Grid")
b2=pp.create_bus(net , vn_kv=33 ,name ="Solar Farm Bus")
b3=pp.create_bus(net , vn_kv=33 ,name ="Wind Turbine Bus")
b4=pp.create_bus(net , vn_kv=66 ,name ="Industrial Zone Bus A")
b5=pp.create_bus(net , vn_kv=11 ,name ="Residential Zone Bus B")
b6=pp.create_bus(net , vn_kv=11 ,name ="EV Charging Station ")
b7=pp.create_bus(net , vn_kv=11 ,name ="Battery  Station Bus ")
b8=pp.create_bus(net , vn_kv=11 ,name ="Hospital Zone C ")
b9=pp.create_bus(net , vn_kv=33 ,name ="Substation  ")
b10=pp.create_bus(net , vn_kv=0.4 ,name ="Rural Load End")

pp.create_transformer_from_parameters(net, hv_bus=b1, lv_bus=b9, sn_mva=63, vn_hv_kv=132, vn_lv_kv=33,
    vk_percent=10, vkr_percent=0.5, pfe_kw=0.1, i0_percent=0.1, shift_degree=0, name="Grid to Substation")

pp.create_transformer_from_parameters(net, hv_bus=b9, lv_bus=b2, sn_mva=63, vn_hv_kv=33, vn_lv_kv=33,
    vk_percent=10, vkr_percent=0.5, pfe_kw=0.1, i0_percent=0.1, shift_degree=0, name="Solar Setup")

pp.create_transformer_from_parameters(net, hv_bus=b9, lv_bus=b3, sn_mva=40, vn_hv_kv=33, vn_lv_kv=33,
    vk_percent=10, vkr_percent=0.5, pfe_kw=0.1, i0_percent=0.1, shift_degree=0, name="Wind Setup")

pp.create_transformer_from_parameters(net, hv_bus=b9, lv_bus=b5, sn_mva=25, vn_hv_kv=33, vn_lv_kv=11,
    vk_percent=10, vkr_percent=0.5, pfe_kw=0.1, i0_percent=0.1, shift_degree=0, name="Residential Transformer")

pp.create_transformer_from_parameters(net, hv_bus=b9, lv_bus=b6, sn_mva=25, vn_hv_kv=33, vn_lv_kv=11,
    vk_percent=10, vkr_percent=0.5, pfe_kw=0.2, i0_percent=0.1, shift_degree=0, name="EV Transformer")

pp.create_transformer_from_parameters(net, hv_bus=b9, lv_bus=b8, sn_mva=25, vn_hv_kv=33, vn_lv_kv=11,
    vk_percent=10, vkr_percent=0.5, pfe_kw=0.1, i0_percent=0.1, shift_degree=0, name="Hospital Transformer")


pp.create_transformer_from_parameters(net, hv_bus=b9, lv_bus=b7, sn_mva=25, vn_hv_kv=33, vn_lv_kv=11,
    vk_percent=10, vkr_percent=0.5, pfe_kw=0.1, i0_percent=0.1, shift_degree=0, name="Substation-Battery")

# create the  Residential loads
pp.create_load(net , bus=b5  , p_mw=1.0  , q_mvar=1.0 , name="Residental Load")
# EV charging station Load
pp.create_load(net , bus=b6  , p_mw=1.5  , q_mvar=0.6  , name="EV Charging Station")
# Hospital Load
pp.create_load(net , bus=b8  , p_mw=2.5  , q_mvar=0.8  , name="Hospital Load")
# Rural Area Load
pp.create_load(net , bus=b10  , p_mw=1.0  , q_mvar= 0.3  , name="Rural Area Load")
pp.create_load(net, bus=b4, p_mw=4.0, q_mvar=0.5, name="Industrial Load")
# Add Solar generator to bus 2
solar_gen=pp.create_sgen(net,bus=b2, p_mw=0.2, q_mvar=0.0, name="Solar Generator", in_service=True)

# Line 1: Substation to Residential
pp.create_line_from_parameters(net, from_bus=b9, to_bus=b5, length_km=1.0,
    r_ohm_per_km=0.642, x_ohm_per_km=0.083, c_nf_per_km=210, max_i_ka=2.8, name="Line_Sub_Res")

# Line 2: Substation to EV
pp.create_line_from_parameters(net, from_bus=b9, to_bus=b6, length_km=1.0,
    r_ohm_per_km=0.642, x_ohm_per_km=0.083, c_nf_per_km=210, max_i_ka=4.0, name="Line_Sub_EV")

# Line 3: Substation to Hospital
pp.create_line_from_parameters(net, from_bus=b9, to_bus=b8, length_km=1.2,
    r_ohm_per_km=0.642, x_ohm_per_km=0.083, c_nf_per_km=210, max_i_ka=5.0, name="Line_Sub_Hosp")

# Line 4: Substation to Solar
pp.create_line_from_parameters(net, from_bus=b9, to_bus=b2, length_km=1.0,
    r_ohm_per_km=0.642, x_ohm_per_km=0.083, c_nf_per_km=210, max_i_ka=3.5, name="Line_Sub_Solar")

#  Add parallel line to relieve overloading on Line_Sub_Solar
pp.create_line_from_parameters(net, from_bus=b9, to_bus=b2, length_km=1.0,
    r_ohm_per_km=0.642, x_ohm_per_km=0.083, c_nf_per_km=210, max_i_ka=3.5, name="Line_Sub_Solar_Parallel")


# Line 5: Substation to Wind
pp.create_line_from_parameters(net, from_bus=b9, to_bus=b3, length_km=1.0,
    r_ohm_per_km=0.642, x_ohm_per_km=0.083, c_nf_per_km=210, max_i_ka=3.2, name="Line_Sub_Wind")

# Line 6: Residential to Rural
pp.create_line_from_parameters(net, from_bus=b5, to_bus=b10, length_km=0.5,
    r_ohm_per_km=0.5, x_ohm_per_km=0.05, c_nf_per_km=100, max_i_ka=8.0, name="Line_Res_Rural")

# Line between Industrial Zone (Bus 4) and Substation (Bus 9)
pp.create_line_from_parameters(net, from_bus=b4, to_bus=b9, length_km=1.5,
    r_ohm_per_km=0.3, x_ohm_per_km=0.05, c_nf_per_km=210, max_i_ka=2.5, name="Line_Indus_Sub")


# Capacitor bank introduced at Bus  
pp.create_shunt(net, bus=b5, q_mvar=-4.0, p_mw=0.0, name="Capacitor Bank at B5")
pp.create_shunt(net, bus=b6, q_mvar=-2.5, p_mw=0.0, name="Capacitor at EV")
pp.create_shunt(net, bus=b8, q_mvar=-2.5, p_mw=0.0, name="Capacitor at Hospital")


# Grid Generator at b1
pp.create_ext_grid(net, bus=b1, vm_pu=1.10, name="Grid Generator", slack=True)

#pp.create_gen(net, bus=b2, p_mw=6.0, vm_pu=1.0, name="Solar Generator")
pp.create_gen(net, bus=b3, p_mw=10.0, vm_pu=1.0, name="Wind Generator")

# Solar Generator at b2
pp.create_sgen(net, bus=b2, p_mw=6.0, q_mvar=5.0, name="Solar Plant")
net.sgen["auto_vm_control"] = True

# Wind Generator at b3
pp.create_sgen(net, bus=b3, p_mw=10.0, q_mvar=5.0, name="Wind Turbine")
net.sgen["auto_vm_control"] = True
# Enable tap changer on Solar Transformer (index 1)
net.trafo.at[1, 'tap_side'] = 'lv'
net.trafo.at[1, 'tap_neutral'] = 0
net.trafo.at[1, 'tap_min'] = -5
net.trafo.at[1, 'tap_max'] = 5
net.trafo.at[1, 'tap_step_percent'] = 2.5
net.trafo.at[1, 'tap_pos'] = 5  # raise voltage

# Enable tap changer on Wind Transformer (index 2)
net.trafo.at[2, 'tap_side'] = 'lv'
net.trafo.at[2, 'tap_neutral'] = 0
net.trafo.at[2, 'tap_min'] = -5
net.trafo.at[2, 'tap_max'] = 5
net.trafo.at[2, 'tap_step_percent'] = 2.5
net.trafo.at[2, 'tap_pos'] = 5  # raise voltage
pp.runpp(net)

# GUI Function

for i, row in net.res_line.iterrows():
    loading = row["loading_percent"]
    if loading > 100:
        fbus = net.bus.at[net.line.at[i, "from_bus"], "name"]
        tbus = net.bus.at[net.line.at[i, "to_bus"], "name"]
        print(f"⚠️ Line {i} ({fbus} → {tbus}): {loading:.2f}% loaded")

# Voltage Plot
def update_voltage_graph():
    for widget in voltage_frame.winfo_children():
        widget.destroy()
    fig, ax1 = plt.subplots(figsize=(6,5))
    # New show solar ON/OFF status on plot
    solar_on = net.sgen.at[solar_gen, 'in_service']
    solar_status = 'ON' if solar_on else 'OFF'
    status_color = 'green' if solar_on else 'red'
    ax1.text(
        0.05, 1.05,
        f'☀Solar: {solar_status}',
        transform=ax1.transAxes,
        color=status_color,
        fontsize=12,
        fontweight='bold',
        bbox=dict(facecolor='white', alpha=0.7)
    )
    ax1.plot(net.res_bus.vm_pu, marker='o', linestyle='-')
    ax1.set_title('Bus Voltage profile')
    ax1.set_xlabel('Bus Index')
    ax1.set_ylabel('Voltage (p.u.)')
    plt.grid(True)
    plt.tight_layout()
    #plt.show()
    canvas = FigureCanvasTkAgg(fig, master=voltage_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
# Line Loading Plot
def update_loading_graph():
    for widget in loading_frame.winfo_children():
        widget.destroy()
        
    fig, ax = plt.subplots(figsize=(6, 5))
    current_heights = [bar.get_height() if 'bar' in locals() else 0 for bar in getattr(ax, 'containers',[[]])[0]]
    target_heights = net.res_line.loading_percent.tolist()
    current_heights = [0] * len(target_heights)
    bars = ax.bar(range(len(target_heights)), current_heights, color='orange')
    ax.bar(range(len(net.res_line)), net.res_line.loading_percent, color='Orange')
    ax.axhline(100,linestyle='--'  , color='red')
    ax.set_title("Line Loading Percentage")
    ax.set_xlabel("Line Index")
    ax.set_ylabel("Loading %")
    
    plt.tight_layout()
    animate_bars(current_heights, target_heights, bars, ax)
    #plt.show()
    canvas = FigureCanvasTkAgg(fig, master=loading_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    animate_bars(current_heights, target_heights, bars, ax)

def draw_heatmap(ax, data, labels, title, cmap, vmin=None, vmax=None):
    ax.clear()
    heatmap = ax.imshow([data], cmap=cmap, aspect="auto", vmin=vmin, vmax=vmax)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticks([])  # Hide Y-axis ticks
    ax.set_title(title)
    return heatmap

def update_time():
    global current_hour, time_running
    if not time_running:
        return
    current_hour=(current_hour+1)% 24
    time_label.config(text=f"Time: {current_hour}:00")
    #Enable solar from 6:00 to 18:00
    if 6 <= current_hour< 18:
        net.sgen.at[0, 'in_service'] = True
        print(f"Solar ON at {current_hour}:00")
    else:
        net.sgen.at[0, 'in_service'] = False
        print(f"Solar OFF at {current_hour}:00")
    run_loadflow()
    root.after(2000, update_time)    # Repeat every 2 sec  
def draw_heatmap(ax, data, labels, title, cmap, vmin=None, vmax=None):
    ax.clear()
    heatmap = ax.imshow([data], cmap=cmap, aspect="auto", vmin=vmin, vmax=vmax)
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticks([])  # Hide Y-axis ticks
    ax.set_title(title)
    return heatmap
def update_heatmap_graph():
    pp.runpp(net)
    """Updates the heatmaps for bus voltages and line loading."""
    # Clear previous plots
    for widget in heatmap_frame.winfo_children():
        widget.destroy()

    # Retrieve results from the last power flow
    voltages = net.res_bus.vm_pu.tolist()
    bus_labels = net.bus['name'].tolist()
    loadings = net.res_line.loading_percent.tolist()
    line_labels = net.line['name'].tolist()

    # Create a two-panel figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))
    draw_heatmap(ax1, voltages, bus_labels, "Bus Voltage Heatmap (p.u.)", cmap='coolwarm', vmin=0.9, vmax=1.1)
    draw_heatmap(ax2, loadings, line_labels, "Line Loading (%)", cmap='YlOrRd', vmin=0, vmax=120)
    plt.tight_layout()
# Embed plot in the Tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=heatmap_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)      
def run_loadflow():
    try:
        # Check Voltage Violations
        update_heatmap_graph()
        volt_pct = net.res_bus.vm_pu * 100
        if any(volt_pct < 90) or any(volt_pct > 110):
            messagebox.showwarning("Voltage Alert ⚠️" ,"one buses out of 0.9-1.1 p.u. range")
        
        # Check Loading Violations
        #loading=net.res_line.loading_percent
        if any(net.res_line.loading_percent >100):
            messagebox.showwarning("Overload Alert ⚠️" , "some lines are >100% loaded")
    except Exception as e:
        messagebox.showerror("Error", str(e))
# controller callbacks for the buttons
current_hour = 0
time_running = False
def start_time_sim():
    global time_running
    time_running = True
    update_time()
def stop_time_sim():
    global time_running
    time_running = False                
def toggle_line():
    idx = net.line.index[0]
    net.line.at[idx, 'in_service'] = not net.line.at[idx, 'in_service']
    run_loadflow()        
        
    
def trigger_fault():
    idx_fault = net.line.index[0]
    idx_backup = net.line.index[3]
    net.line.at[idx_fault,'in_service'] = False
    net.line.at[idx_backup,'in_service']= True
    run_loadflow()
    messagebox.showinfo("Fault", "Fault triggered, backup line activated.")

current_hour = 0
running = False

def time_step():
    global current_hour
    if not running: return
    current_hour = (current_hour+1)%24
    time_label.config(text=f"Time: {current_hour}:00")
    # solar ON 6–18
    net.sgen.at[solar_gen,'in_service'] = 6<=current_hour<18
    run_loadflow()
    root.after(2000, time_step)


def start_sim():
    global running
    running = True
    time_step()

def stop_sim():
    global running
    running = False        
def start_real_time_plot():
    def update_time():
        current_hour = (current_hour+1)%24
        hour_label.config(text=f"Time: {current_hour}:00")
        # Enable Solar between 6:00 and 18:00
        if 6 <= current_hour < 18:
            net.sgen.in_service.at[solar_index] = True
        else:
            net.sgen.in_service.at[solar_index] = False
        # Run power flow
        pp.runpp(net)
        # check voltage violations
        voltage_ok = all(0.95 <= vm <= 1.05 for vm in net.res_bus.vm_pu)
        loading_ok = all(loading <= 100 for loading in net.res_line.loading_percent)
        # Auto disconnect logic
        if 6 <= current_hour < 18:  # Only when solar was supposed to be ON
            if not voltage_ok or not loading_ok:
                if net.sgen.in_service.at[solar_index]:
                    net.sgen.in_service.at[solar_index] = False
                    print(f"🔴 Solar Disconnected at {current_hour}:00 due to violation")
            else:
                if not net.sgen.in_service.at[solar_index]:
                    net.sgen.in_service.at[solar_index] = True
                    print(f"✅ Solar Reconnected at {current_hour}:00")
                # Update solar status label
        status = "ON" if net.sgen.in_service.at[solar_index] else "OFF"
        solar_status_label.config(text=f"Solar Status: {status}")

        # Re-run load flow after status change
        pp.runpp(net)

        # Update plots
        update_plot()

def build_gui(root):
    root.title("SmartGrid Load Flow GUI")
    root.geometry("800x600")

    style = ttk.Style(root)
    style.theme_use('clam')

    pw = ttk.Panedwindow(root, orient=tk.HORIZONTAL)
    pw.pack(fill=tk.BOTH, expand=True)

    plot_container = ttk.Frame(pw)
    pw.add(plot_container, weight=3)
    heatmap_frame = ttk.LabelFrame(plot_container, text="Heatmaps")
    voltage_frame = ttk.LabelFrame(plot_container, text="Voltages")
    loading_frame = ttk.LabelFrame(plot_container, text="Line Loadings")
    for fr in (heatmap_frame, voltage_frame, loading_frame):
        fr.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    control_container = ttk.Frame(pw, width=200)
    pw.add(control_container, weight=1)

    lbl_time      = ttk.Label(control_container, text="Time: 00:00", font=("Arial", 12))
    lbl_gen_stat  = ttk.Label(control_container, text="Generator Status: --", font=("Arial", 12))
    lbl_volt_stat = ttk.Label(control_container, text="Voltage Status: Normal", font=("Arial", 12))
    btn_toggle    = ttk.Button(control_container, text="Line 1: ON")
    btn_start     = ttk.Button(control_container, text="Start Time Sim")
    btn_stop      = ttk.Button(control_container, text="Stop Time Sim")
    btn_live      = ttk.Button(control_container, text="Start Real-Time Graph")
    btn_run       = ttk.Button(control_container, text="Run Load Flow", style="Accent.TButton")
    btn_fault     = ttk.Button(control_container, text="Trigger Fault", style="Danger.TButton")

    lbl_time     .grid(row=0, column=0, columnspan=2, pady=(10,5), sticky="w")
    lbl_gen_stat .grid(row=1, column=0, columnspan=2, pady=5, sticky="w")
    lbl_volt_stat.grid(row=2, column=0, columnspan=2, pady=(5,15), sticky="w")
    btn_toggle   .grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")
    ttk.Separator(control_container).grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)

    btn_start    .grid(row=5, column=0, padx=5, pady=5, sticky="ew")
    btn_stop     .grid(row=5, column=1, padx=5, pady=5, sticky="ew")
    btn_live     .grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    ttk.Separator(control_container).grid(row=7, column=0, columnspan=2, sticky="ew", pady=10)

    btn_run      .grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
    btn_fault    .grid(row=9, column=0, columnspan=2, padx=5, pady=(5,15), sticky="ew")

    for i in range(2):
        control_container.columnconfigure(i, weight=1)

    return heatmap_frame, voltage_frame, loading_frame, lbl_time, lbl_gen_stat, lbl_volt_stat, btn_toggle, btn_start, btn_stop, btn_live, btn_run, btn_fault

if __name__ == "__main__":
    root = tk.Tk()
    (heatmap_frame,
    voltage_frame,
    loading_frame,
    lbl_time,
    lbl_gen_stat,
    lbl_volt_stat,
    btn_toggle,
    btn_start,
    btn_stop,
    btn_live,
    btn_run,
    btn_fault) = build_gui(root)
    global time_label
    time_label = lbl_time
    btn_start.config(command=start_time_sim)
    btn_stop.config(command=stop_time_sim)
 
    # -- now wire up your callbacks --
    btn_start   .config(command=start_time_sim)
    btn_stop    .config(command=stop_time_sim)
    btn_run     .config(command=run_loadflow)
    btn_live    .config(command=start_real_time_plot)
    btn_fault   .config(command=trigger_fault)
    btn_toggle  .config(command=toggle_line)

    root.mainloop()
