from database.data_handler import get_data_from_db_at_date
from datetime import datetime
import tkinter as tk
from tkinter import ttk

def initialize(pages, content):
    pages['prices'] = ttk.Frame(content)
    global cheapest_label, average_label, prices_table
    cheapest_label = ttk.Label(
        pages['prices'],
        text="",
        font=("Segoe UI", 20, "bold"),
        justify=tk.LEFT,
        anchor=tk.W,
    )
    cheapest_label.pack(fill=tk.X, padx=20, pady=(20, 5))

    average_label = ttk.Label(
        pages['prices'],
        text="",
        font=("Segoe UI", 14),
        justify=tk.LEFT,
        anchor=tk.W,
    )
    average_label.pack(fill=tk.X, padx=20, pady=(0, 20))

    table_frame = ttk.Frame(pages['prices'])
    table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

    prices_table = ttk.Treeview(
        table_frame, columns=('station', 'price'), show='headings', height=8
    )
    prices_table.heading('station', text='Station', anchor=tk.W)
    prices_table.heading('price', text='Price (EUR/litre)', anchor=tk.W)
    prices_table.column('station', anchor=tk.W, width=300)
    prices_table.column('price', anchor=tk.W, width=200)

    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=prices_table.yview)
    prices_table.configure(yscrollcommand=scrollbar.set)
    prices_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def show_cheapest():    
    data_dict = get_data_from_db_at_date(datetime.today().strftime('%Y-%m-%d'))

    # Clear the table before refilling it
    prices_table.delete(*prices_table.get_children())

    if not data_dict:
        cheapest_label.config(text="No price data for today")
        average_label.config(text="")
        return

    # Table: all stations, cheapest first
    for value in sorted(data_dict.values(), key=lambda v: v['price']):
        prices_table.insert('', tk.END, values=(value['station'], f"{value['price']:.3f}"))

    cheapest = min(data_dict.values(), key=lambda v: v['price'])
    cheapest_label.config(
        text=f"Cheapest station today:\n{cheapest['station']}\n{cheapest['price']:.3f} EUR/litre"
    )

    average = sum(v['price'] for v in data_dict.values()) / len(data_dict)
    average_label.config(text=f"Average price today: {average:.3f} EUR/litre")