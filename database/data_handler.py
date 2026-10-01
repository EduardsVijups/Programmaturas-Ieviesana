import sqlite3

conn = sqlite3.connect('database/fuel_prices.db')

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS fuel_prices (
        id INTEGER PRIMARY KEY,
        station TEXT,
        price REAL,
        price_date TEXT
    )
''')

conn.commit()

def save_data_to_db(data):
    for item in data['data']['fuel_types']['e95']:
        cursor.execute('''
            INSERT INTO fuel_prices (station, price, price_date)
            VALUES (?, ?, ?)
        ''', (item['station'], item['price'], item['price_date']))
    
    conn.commit()

def get_data_from_db():
    cursor.execute('SELECT * FROM fuel_prices')
    rows = cursor.fetchall()

    t = {}
    for row in rows:
        t[row[0]] = {'station': row[1], 'price': row[2], 'price_date': row[3]}
    return t