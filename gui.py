import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from database.data_handler import get_data_from_db_at_date
from datetime import datetime

# Lazy loading of ax and canvas to avoid circular import issues
ax = None
canvas = None

def fetch_and_plot_data():
    # Clear the current figure
    ax.clear()

    data_dict = get_data_from_db_at_date(datetime.today().strftime('%Y-%m-%d'))

    stations = []
    prices = []
    for _, value in data_dict.items():
        stations.append(value['station'])
        prices.append(value['price'])

    ax.bar(stations, prices)
    ax.set_xlabel('Station')
    ax.set_ylabel('Price (EUR/litre)')
    ax.set_title('Fuel Prices by Station')
    ax.set_xticks(range(len(stations)))
    ax.set_xticklabels(stations, ha='center')

    canvas.draw()

def initialize_gui():
    root = tk.Tk()
    root.title("Fuel Prices GUI")
    root.geometry("800x600")

    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    refresh_button = ttk.Button(frame, text="Refresh Data", command=fetch_and_plot_data)
    refresh_button.pack(pady=10)

    # Create a matplotlib figure and axis
    fig = Figure(figsize=(6, 4), dpi=100)
    global ax
    ax = fig.add_subplot(111)
    
    # Create a canvas to embed the figure in Tkinter
    global canvas
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    fetch_and_plot_data()

    root.mainloop()
