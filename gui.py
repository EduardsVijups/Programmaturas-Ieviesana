import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from database.data_handler import get_data_from_db_at_date
from history_page import plot_price_history
from datetime import datetime

# Lazy loading of widgets to avoid circular import issues
cheapest_label = None
prices_table = None
history_ax = None
history_canvas = None

# GUI state
current_page = 'prices'
pages = {}
switch_button = None


def fetch_and_show_cheapest():
    data_dict = get_data_from_db_at_date(datetime.today().strftime('%Y-%m-%d'))

    # Clear the table before refilling it
    prices_table.delete(*prices_table.get_children())

    if not data_dict:
        cheapest_label.config(text="No price data for today")
        return

    # Table: all stations, cheapest first
    for value in sorted(data_dict.values(), key=lambda v: v['price']):
        prices_table.insert('', tk.END, values=(value['station'], f"{value['price']:.3f}"))

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

    # Page 1: cheapest station (label), table of all stations
    pages['prices'] = ttk.Frame(content)
    global cheapest_label, prices_table
    cheapest_label = ttk.Label(
        pages['prices'],
        text="",
        font=("Segoe UI", 28, "bold"),
        justify=tk.CENTER,
        anchor=tk.CENTER,
    )
    cheapest_label.pack(fill=tk.X, pady=20)

    table_frame = ttk.Frame(pages['prices'])
    table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

    prices_table = ttk.Treeview(
        table_frame, columns=('station', 'price'), show='headings', height=8
    )
    prices_table.heading('station', text='Station')
    prices_table.heading('price', text='Price (EUR/litre)')
    prices_table.column('station', anchor=tk.W, width=300)
    prices_table.column('price', anchor=tk.E, width=200)

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=prices_table.yview)
    prices_table.configure(yscrollcommand=scrollbar.set)
    prices_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Page 2: price history (line chart)
    pages['history'] = ttk.Frame(content)
    history_fig = Figure(figsize=(6, 4), dpi=100)
    global history_ax, history_canvas
    history_ax = history_fig.add_subplot(111)
    history_canvas = FigureCanvasTkAgg(history_fig, master=pages['history'])
    history_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    show_page('prices')

    root.mainloop()
