import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import ttk
import sv_ttk
from datetime import datetime
import time
import sys
from lonroy import LeakDetector  # assuming LeakDetector has the necessary functions
from pathlib import Path




file = f"leakDetectorData-{datetime.now().strftime("%m-%d-%Y-%H-%M-%S")}.csv"


# GUI setup
class LeakDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Leak Detector App")
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.root.geometry("1200x1000")
        # Initialize data lists
        self.start_time = time.time()
        self.timestamp = []
        self.uptime = []
        self.leakrate = []
        self.status = None

        self.leakdetector = LeakDetector(debug=True)


        self.units = self.leakdetector.get_leak_rate_unit()
        

        # Set up the figure and plot
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [],color="m", lw=2)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel(f'Leak Rate {self.units}')
        self.fill = None
        
        # Embed matplotlib figure in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        

        # Animation setup
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=250)


    def update_plot(self, frame):
        timestamp = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        uptime = round((time.time()-self.start_time),2)
        status = self.leakdetector.get_status()
        leakrate = self.leakdetector.get_leak_rate()

        with open(file,'a+') as log:
            log.writelines(f"{timestamp}, {uptime}, {status}, {leakrate}, {self.units}\n")
            log.close()

        self.timestamp.append(timestamp)
        self.uptime.append(uptime)
        self.leakrate.append(leakrate)
        self.status = status
        if len(self.timestamp) > 120*2:
            self.timestamp.pop(0)
            self.uptime.pop(0)
            self.leakrate.pop(0)

        
        # Update plot data
        self.line.set_data(self.uptime,self.leakrate)
        self.ax.relim()
        #y0,x0 = self.ax.get_ybound()
        #self.fill = self.ax.fill_between(self.uptime,[y0 for tmp in range(120)],self.leakrate,color="m",alpha=0.6)
        for txt in self.ax.texts:
            txt.remove()
        self.ax.text(0.05,0.95,f"Status: {status}\n{leakrate} {self.units}", transform=self.ax.transAxes, fontsize=14,verticalalignment='top', bbox=self.props)
        self.ax.autoscale_view()
        self.canvas.draw()

    def close_app(self):
        # Ensure leakdetector is closed before destroying the Tkinter window
        self.leakdetector.close()
        self.root.destroy()
        sys.exit()
        

# Run the app
root = tk.Tk()
app = LeakDetectorApp(root)
sv_ttk.set_theme("dark")
root.mainloop()
