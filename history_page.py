from datetime import datetime
import matplotlib.dates as mdates
from database.data_handler import get_price_history
from tkinter import ttk
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def initialize(pages, content):
    pages['history'] = ttk.Frame(content)
    history_fig = Figure(figsize=(6, 4), dpi=100)
    global ax, history_canvas
    ax = history_fig.add_subplot(111)
    history_canvas = FigureCanvasTkAgg(history_fig, master=pages['history'])
    history_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def plot_price_history():
    """Draw one line per station showing price over time."""
    ax.clear()

    history = get_price_history()

    for station, points in history.items():
        dates = [datetime.strptime(d, '%Y-%m-%d') for d, _ in points]
        prices = [p for _, p in points]
        ax.plot(mdates.date2num(dates), prices, marker='o', markersize=3, label=station)

    ax.set_xlabel('Date')
    ax.set_ylabel('Price (EUR/litre)')
    ax.set_title('Fuel Price History')
    ax.grid(True, alpha=0.3)
    if history:
        ax.legend()

    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
    ax.figure.autofmt_xdate()

    history_canvas.draw()
