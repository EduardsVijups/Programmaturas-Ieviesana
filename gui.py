import tkinter as tk
from tkinter import ttk
import history_page
import main_page

# Lazy loading of widgets to avoid circular import issues
cheapest_label = None
average_label = None
prices_table = None
history_ax = None
history_canvas = None

# GUI state
current_page = 'prices'
pages = {}
switch_button = None


def fetch_and_show_cheapest():
    main_page.show_cheapest()


def fetch_and_plot_history():
    history_page.plot_price_history()


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

    main_page.initialize(pages, content)
    history_page.initialize(pages, content)
    

    show_page('prices')

    root.mainloop()
