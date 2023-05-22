import tkinter as tk
import subprocess

class AirodumpGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Interface dropdown
        self.interface_label = tk.Label(self, text="Interface:")
        self.interface_label.pack()
        self.interface_var = tk.StringVar(self)
        self.interface_dropdown = tk.OptionMenu(self, self.interface_var, *self.get_interfaces())
        self.interface_dropdown.pack()

        # GPS checkbox
        self.gps_var = tk.IntVar()
        self.gps_checkbox = tk.Checkbutton(self, text="Enable GPSD", variable=self.gps_var)
        self.gps_checkbox.pack()

        # BSSID filter checkbox and entry
        self.bssid_var = tk.IntVar()
        self.bssid_checkbox = tk.Checkbutton(self, text="Enable BSSID filter", variable=self.bssid_var, command=self.toggle_bssid)
        self.bssid_checkbox.pack()
        self.bssid_entry = tk.Entry(self, state="disabled")
        self.bssid_entry.pack()

        # Channel filter checkbox and entry
        self.channel_var = tk.IntVar()
        self.channel_checkbox = tk.Checkbutton(self, text="Enable channel filter", variable=self.channel_var)
        self.channel_checkbox.pack()
        self.channel_entry = tk.Entry(self, state="disabled")
        self.channel_entry.pack()

        # Save survey checkbox and filename entry
        self.save_var = tk.IntVar()
        self.save_checkbox = tk.Checkbutton(self, text="Save survey", variable=self.save_var, command=self.toggle_save)
        self.save_checkbox.pack()
        self.filename_entry = tk.Entry(self, state="disabled")
        self.filename_entry.pack()

        # Start button
        self.start_button = tk.Button(self, text="Start Survey", command=self.start_survey)
        self.start_button.pack()

    def get_interfaces(self):
        process = subprocess.run(['iwconfig'], stdout=subprocess.PIPE)
        output = process.stdout.decode()
        interfaces = [line.split()[0] for line in output.split('\n') if line and not line.startswith(' ')]
        return interfaces

    def toggle_bssid(self):
        if self.bssid_var.get() == 1:
            self.bssid_entry.configure(state="normal")
        else:
            self.bssid_entry.configure(state="disabled")

    def toggle_save(self):
        if self.save_var.get() == 1:
            self.filename_entry.configure(state="normal")
        else:
            self.filename_entry.configure(state="disabled")

    def start_survey(self):
        interface = self.interface_var.get()
        command = ['airodump-ng', interface]

        if self.gps_var.get() == 1:
            command += ['--gpsd']

        if self.bssid_var.get() == 1:
            bssid = self.bssid_entry.get().strip()
            if bssid:
                command += ['--bssid', bssid]

        if self.channel_var.get() == 1:
            channel = self.channel_entry.get().strip()
            if channel:
                command += ['--channel', channel]

        if self.save_var.get() == 1:
            filename = self.filename_entry.get().strip()
            if filename:
                command += ['-w', filename]



        subprocess.Popen(command)

root = tk.Tk()
app = AirodumpGUI(master=root)
app.mainloop()
