import tkinter as tk
from tkinter import messagebox, ttk
from database import init_db, add_order, get_all_orders, update_order_status
from datetime import datetime


class OrderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система управления заказами")
        self.root.geometry("1000x700")

        init_db()

        # Поля ввода
        tk.Label(root, text="Имя клиента:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.customer_entry = tk.Entry(root, width=30)
        self.customer_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(root, text="Товар:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.product_entry = tk.Entry(root, width=30)
        self.product_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(root, text="Количество:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.quantity_entry = tk.Entry(root, width=30)
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Кнопка добавления заказа
        tk.Button(root, text="Добавить заказ", command=self.add_order, bg="lightgreen", width=20).grid(row=3, column=0,
                                                                                                       columnspan=2,
                                                                                                       pady=10)

        # Таблица заказов
        columns = ("ID", "Клиент", "Товар", "Кол-во", "Статус", "Создан", "Изменен")
        self.tree = ttk.Treeview(root, columns=columns, show="headings", height=20)

        # Настройка заголовков и ширины колонок
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=50)
        self.tree.heading("Клиент", text="Клиент")
        self.tree.column("Клиент", width=150)
        self.tree.heading("Товар", text="Товар")
        self.tree.column("Товар", width=150)
        self.tree.heading("Кол-во", text="Кол-во")
        self.tree.column("Кол-во", width=70)
        self.tree.heading("Статус", text="Статус")
        self.tree.column("Статус", width=120)
        self.tree.heading("Создан", text="Создан")
        self.tree.column("Создан", width=150)
        self.tree.heading("Изменен", text="Изменен")
        self.tree.column("Изменен", width=150)

        self.tree.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Скроллбар для таблицы
        scrollbar_y = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar_y.set)
        scrollbar_y.grid(row=4, column=4, sticky="ns")

        scrollbar_x = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscroll=scrollbar_x.set)
        scrollbar_x.grid(row=5, column=0, columnspan=4, sticky="ew")

        # Выбор статуса
        tk.Label(root, text="Новый статус:").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(root, textvariable=self.status_var,
                                         values=["новый", "в обработке", "готов", "завершен"],
                                         state="readonly", width=20)
        self.status_combo.grid(row=6, column=1, padx=10, pady=5, sticky="w")
        self.status_combo.set("в обработке")

        # Кнопка изменения статуса
        tk.Button(root, text="Изменить статус", command=self.change_status, bg="lightblue", width=20).grid(row=6,
                                                                                                           column=2,
                                                                                                           padx=10,
                                                                                                           pady=5,
                                                                                                           sticky="w")

        # Кнопка обновления списка
        tk.Button(root, text="Обновить", command=self.refresh_orders, bg="lightyellow", width=15).grid(row=6, column=3,
                                                                                                       padx=10, pady=5,
                                                                                                       sticky="w")

        # Настройка растягивания
        root.grid_rowconfigure(4, weight=1)
        root.grid_columnconfigure(1, weight=1)

        self.refresh_orders()

    def add_order(self):
        customer = self.customer_entry.get().strip()
        product = self.product_entry.get().strip()
        quantity_str = self.quantity_entry.get().strip()

        if not customer or not product or not quantity_str:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Количество должно быть положительным числом")
            return

        add_order(customer, product, quantity)
        self.refresh_orders()

        # Очистка полей
        self.customer_entry.delete(0, tk.END)
        self.product_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)

    def refresh_orders(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Загрузка заказов
        orders = get_all_orders()
        for order in orders:
            # Форматируем даты для лучшего отображения
            order_id, customer, product, quantity, status, created_at, updated_at = order
            # Убираем секунды для компактности
            created_formatted = created_at[:-3] if created_at else ""
            updated_formatted = updated_at[:-3] if updated_at else ""

            self.tree.insert("", tk.END, values=(
                order_id, customer, product, quantity, status,
                created_formatted, updated_formatted
            ))

    def change_status(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Ошибка", "Выберите заказ для изменения статуса")
            return

        order_id = self.tree.item(selected[0])['values'][0]
        new_status = self.status_var.get()

        if not new_status:
            messagebox.showerror("Ошибка", "Выберите новый статус")
            return

        update_order_status(order_id, new_status)
        self.refresh_orders()


if __name__ == "__main__":
    root = tk.Tk()
    app = OrderApp(root)
    root.mainloop()