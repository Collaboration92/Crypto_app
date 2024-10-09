import tkinter as tk
from tkinter import ttk
import requests
from tkinter import messagebox


# Функция для получения данных с CoinGecko API
def get_crypto_data():
    global data
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 20,
        'page': 1,
        'sparkline': False
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        print(type(data))
        return data
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось получить данные: {e}")
        return None


# Функция для обновления данных в интерфейсе
def update_crypto_data():
    global data
    data = get_crypto_data()
    try:
        for i,crypto in enumerate(data):
            xxx=str(i+1)
            crypto_name = crypto['name']
            crypto_price = f"${crypto['current_price']:,.2f}"
            crypto_change = f"{crypto['price_change_percentage_24h']:.2f}%"
            table.item(xxx, values=(crypto_name, crypto_price, crypto_change))
    except Exception:
        messagebox.showerror(title="ошибка",message='вы обновляете курс слишком часто, повторите позже')
# Функция конвертации криптовалют и валют
def convert_crypto():
    from_currency = from_combo.get()
    to_currency = to_combo.get()
    amount = amount_entry.get()

    try:
        _=float(amount)
    except Exception:
        messagebox.showerror("Ошибка", "Введите корректную сумму!")
        return

    #data = get_crypto_data()

    rates = {crypto['name']: crypto['current_price'] for crypto in data}
    rates['USD'] = 1  # Для конвертации в USD
    rates['RUB'] = 75  # Допустим текущий курс рубля к доллару 75 RUB = 1 USD

    try:
        amount = float(amount)
        from_rate = rates.get(from_currency, None)
        to_rate = rates.get(to_currency, None)

        if from_rate and to_rate:
            converted_amount = amount * (to_rate / from_rate)
            result_label.config(text=f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}")
        else:
            messagebox.showerror("Ошибка", "Выбрана неподдерживаемая криптовалюта или валюта")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка конвертации: {e}")


# Создание окна приложения
root = tk.Tk()
root.title("Курсы криптовалют и конвертер")
root.geometry("600x800")
data=[]
# Заголовок
header_label = tk.Label(root, text="Текущие курсы популярных криптовалют", font=("Arial", 16))
header_label.pack(pady=10)
change_currency = ttk.Combobox(root, values=['USD','RUB'])
change_currency.set("Выберите валюту")
change_currency.pack()
# Таблица для отображения данных
columns = ('Название', 'Цена (USD)', 'Изменение (24ч)')
table = ttk.Treeview(root, columns=columns, show='headings')
table.heading('Название', text='Название')
table.heading('Цена (USD)', text='Цена (USD)')
table.heading('Изменение (24ч)', text='Изменение (24ч)')
table.pack(pady=20, fill='both', expand=True)

# Добавление начальных данных
for i in range(21):
    table.insert("", "end", values=("", "", ""),iid=i)

# Область для конвертера криптовалют
converter_label = tk.Label(root, text="Конвертер криптовалют", font=("Arial", 14))
converter_label.pack(pady=10)

# Ввод суммы
amount_label = tk.Label(root, text="Сумма:")
amount_label.pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

# Выбор исходной криптовалюты
from_label = tk.Label(root, text="Из:")
from_label.pack()

# Используем выпадающие списки для выбора криптовалют и валют
available_currencies = ['Bitcoin', 'Ethereum', 'Tether', 'BNB', 'USD', 'RUB']

from_combo = ttk.Combobox(root, values=available_currencies)
from_combo.set("Выберите валюту")
from_combo.pack()

# Выбор целевой криптовалюты
to_label = tk.Label(root, text="В:")
to_label.pack()

to_combo = ttk.Combobox(root, values=available_currencies)
to_combo.set("Выберите валюту")
to_combo.pack()

# Кнопка для выполнения конвертации
convert_button = tk.Button(root, text="Конвертировать", command=convert_crypto)
convert_button.pack(pady=10)

# Метка для вывода результата конвертации
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)

# Кнопка для обновления данных вручную
update_button = tk.Button(root, text="Обновить курсы", command=update_crypto_data)
update_button.pack(pady=10)

# Первоначальное обновление данных
update_crypto_data()

# Запуск основного цикла интерфейса
root.mainloop()