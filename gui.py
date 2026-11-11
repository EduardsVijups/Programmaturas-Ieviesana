import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from database.data_handler import get_data_from_db_at_date
from history_page import plot_price_history
from datetime import datetime

# Lazy loading of widgets to avoid circular import issues
cheapest_label = None
history_ax = None
history_canvas = None

# GUI state
current_page = 'prices'
pages = {}
switch_button = None


def fetch_and_show_cheapest():
    data_dict = get_data_from_db_at_date(datetime.today().strftime('%Y-%m-%d'))

    if not data_dict:
        cheapest_label.config(text="No price data for today")
        return

    cheapest = min(data_dict.values(), key=lambda v: v['price'])
    cheapest_label.config(
        text=f"Cheapest station today:\n{cheapest['station']}\n{cheapest['price']:.3f} EUR/litre"
    )


def fetch_and_plot_history():
    plot_price_history(history_ax)
    history_canvas.draw()


def refresh_current_page():
    if current_page == 'prices':
        fetch_and_show_cheapest()
    else:
        fetch_and_plot_history()


def show_page(name):
    global current_page
    current_page = name

    for page in pages.values():
        page.pack_forget()
    pages[name].pack(fill=tk.BOTH, expand=True)

    if name == 'prices':
        switch_button.config(text="Show Price History")
    else:
        switch_button.config(text="Show Current Prices")

    refresh_current_page()


def toggle_page():
    show_page('history' if current_page == 'prices' else 'prices')


def initialize_gui():
    root = tk.Tk()
    root.title("Fuel Prices GUI")
    root.geometry("800x600")

    # Top bar with buttons
    toolbar = ttk.Frame(root)
    toolbar.pack(fill=tk.X)

    refresh_button = ttk.Button(toolbar, text="Refresh Data", command=refresh_current_page)
    refresh_button.pack(side=tk.LEFT, padx=10, pady=10)

    global switch_button
    switch_button = ttk.Button(toolbar, text="Show Price History", command=toggle_page)
    switch_button.pack(side=tk.LEFT, padx=10, pady=10)

    # Container holding both pages
    content = ttk.Frame(root)
    content.pack(fill=tk.BOTH, expand=True)

    # Page 1: cheapest station (label)
    pages['prices'] = ttk.Frame(content)
    global cheapest_label
    cheapest_label = ttk.Label(
        pages['prices'],
        text="",
        font=("Segoe UI", 28, "bold"),
        justify=tk.CENTER,
        anchor=tk.CENTER,
    )
    cheapest_label.pack(fill=tk.BOTH, expand=True)

    # Page 2: price history (line chart)
    pages['history'] = ttk.Frame(content)
    history_fig = Figure(figsize=(6, 4), dpi=100)
    global history_ax, history_canvas
    history_ax = history_fig.add_subplot(111)
    history_canvas = FigureCanvasTkAgg(history_fig, master=pages['history'])
    history_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    show_page('prices')

    root.mainloop()
