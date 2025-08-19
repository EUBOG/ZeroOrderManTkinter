import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'новый',
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_order(customer_name, product, quantity):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO orders (customer_name, product, quantity, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (customer_name, product, quantity, 'новый', now, now))
    conn.commit()
    conn.close()

def get_all_orders():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders ORDER BY id DESC')
    orders = cursor.fetchall()
    conn.close()
    return orders

def update_order_status(order_id, new_status):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('UPDATE orders SET status = ?, updated_at = ? WHERE id = ?',
                   (new_status, now, order_id))
    conn.commit()
    conn.close()