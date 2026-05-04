import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import json

# Файл для хранения истории
HISTORY_FILE = 'password_history.json'

# Функция загрузки истории из JSON
def load_history():
    try:
        with open(HISTORY_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Функция сохранения истории в JSON
def save_history(history):
    with open(HISTORY_FILE, 'w') as file:
        json.dump(history, file)

# Функция генерации пароля
def generate_password():
    # Получаем параметры с интерфейса
    length = int(scale_length.get())
    use_digits = var_digits.get()
    use_letters = var_letters.get()
    use_special = var_special.get()
    
    # Проверка минимальной длины (минимум 4 символа)
    if length < 4:
        messagebox.showwarning("Ошибка", "Минимальная длина пароля — 4 символа!")
        return

    # Формируем набор символов для пароля
    chars = ''
    if use_digits: chars += string.digits          # 0-9
    if use_letters: chars += string.ascii_letters  # a-zA-Z
    if use_special: chars += string.punctuation    # !"#$%&'()*+,-./:;<=>?@[$$^_`{|}~
    
    # Проверка, что выбран хотя бы один тип символов
    if not chars:
        messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
        return

    # Генерация пароля (самый простой способ)
    password = ''.join(random.choice(chars) for _ in range(length))
    
    # Отображаем пароль в поле ввода
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    
    # Сохраняем в историю и обновляем таблицу
    history = load_history()
    history.append(password)
    save_history(history)
    update_history_table()

# Функция обновления таблицы истории
def update_history_table():
    for i in tree_history.get_children():
        tree_history.delete(i)
    for password in load_history():
        tree_history.insert('', tk.END, values=(password,))

# Функция очистки истории
def clear_history():
    if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
        save_history([])  # Сохраняем пустой список
        update_history_table()

# Создание главного окна
root = tk.Tk()
root.title("Генератор случайных паролей")
root.geometry("600x450")

# --- Блок настроек ---
frame_settings = tk.LabelFrame(root, text="Настройки пароля", padx=10, pady=10)
frame_settings.pack(pady=10, fill=tk.X)

# Длина пароля (ползунок)
tk.Label(frame_settings, text="Длина пароля:").grid(row=0, column=0, sticky=tk.W)
scale_length = tk.Scale(frame_settings, from_=4, to=32, orient=tk.HORIZONTAL)
scale_length.set(12)  # Значение по умолчанию
scale_length.grid(row=0, column=1, columnspan=2, sticky=tk.W)

# Чекбоксы для выбора символов
var_digits = tk.IntVar(value=1)   # По умолчанию включены цифры
var_letters = tk.IntVar(value=1)  # По умолчанию включены буквы
var_special = tk.IntVar(value=0)  # По умолчанию спецсимволы выключены

tk.Checkbutton(frame_settings, text="Цифры", variable=var_digits).grid(row=1, column=0, sticky=tk.W)
tk.Checkbutton(frame_settings, text="Буквы", variable=var_letters).grid(row=1, column=1, sticky=tk.W)
tk.Checkbutton(frame_settings, text="Спецсимволы", variable=var_special).grid(row=1, column=2, sticky=tk.W)

# --- Блок генерации ---
frame_generate = tk.Frame(root)
frame_generate.pack(pady=10)

btn_generate = tk.Button(frame_generate, text="Сгенерировать пароль", command=generate_password)
btn_generate.pack(side=tk.LEFT, padx=5)

entry_password = tk.Entry(frame_generate, width=40)
entry_password.pack(side=tk.LEFT, padx=5)
entry_password.insert(0, "Ваш пароль появится здесь")

# --- Блок истории ---
frame_history = tk.LabelFrame(root, text="История паролей", padx=5, pady=5)
frame_history.pack(pady=10, fill=tk.BOTH, expand=True)

# Таблица (Treeview) для истории
tree_history = ttk.Treeview(frame_history, columns=("password",), show="headings")
tree_history.heading("password", text="Пароль")
tree_history.column("password", width=500)
tree_history.pack(fill=tk.BOTH, expand=True)

btn_clear = tk.Button(frame_history, text="Очистить историю", command=clear_history)
btn_clear.pack(pady=5)

# Загружаем историю при запуске приложения
update_history_table()

# Запуск окна
root.mainloop()