import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from database.data_handler import get_data_from_db

def fetch_and_plot_data():
    # Clear the current figure
    ax.clear()

    # Fetch data from the database
    data_dict = get_data_from_db()

    # Extract stations and prices
    stations = []
    prices = []
    for _, value in data_dict.items():
        stations.append(value['station'])
        prices.append(value['price'])

    # Create bar chart
    ax.bar(stations, prices)
    ax.set_xlabel('Station')
    ax.set_ylabel('Price (EUR/litre)')
    ax.set_title('Fuel Prices by Station')
    # Set the tick positions and labels
    ax.set_xticks(range(len(stations)))
    ax.set_xticklabels(stations, rotation=45, ha='right')

    # Redraw the canvas
    canvas.draw()

# Create the main window
root = tk.Tk()
root.title("Fuel Prices GUI")
root.geometry("800x600")

# Create a frame for the button and the plot
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Create a button to refresh the data
refresh_button = ttk.Button(frame, text="Refresh Data", command=fetch_and_plot_data)
refresh_button.pack(pady=10)

# Create a matplotlib figure and axis
fig = Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)
# Create a canvas to embed the figure in Tkinter
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Initial plot
fetch_and_plot_data()

# Start the Tkinter event loop
root.mainloop()