import re
import tkinter as tk
from tkinter import messagebox

def is_valid_date_segment(s):
    # Быстрая проверка формата DD.MM.YYYY
    if len(s) != 10:
        return False
    if s[2] != '.' or s[5] != '.':
        return False
    try:
        day = int(s[0:2])
        month = int(s[3:5])
        year = int(s[6:10])
    except ValueError:
        return False

    if month < 1 or month > 12 or day < 1:
        return False

    # Количество дней в каждом месяце, с учётом високосного февраля:
    month_days = [
        31,
        29 if (year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)) else 28,
        31, 30, 31, 30, 31, 31, 30, 31, 30, 31
    ]
    return day <= month_days[month - 1]


def highlight_matches(regex_pattern, description):
    text.tag_remove('match', '1.0', tk.END)
    content = text.get('1.0', tk.END)
    matches = list(re.finditer(regex_pattern, content, re.UNICODE))
    
    for match in matches:
        start_index = f"1.0 + {match.start()} chars"
        end_index = f"1.0 + {match.end()} chars"
        text.tag_add('match', start_index, end_index)
    
    text.tag_config('match', background='yellow')
    
    if matches:
        result = "\n".join([f"{description}: '{m.group()}' at pos {m.start()}" for m in matches])
    else:
        result = f"No matches found for: {description}"
    messagebox.showinfo("Results", result)

def find_integers():
    regex = r"[-+]?\d+"
    highlight_matches(regex, "Integer")

def find_coffee_words():
    regex = r"(?=\b\w{10}\b)\w*кофе\w*"
    highlight_matches(regex, "10-letter word with 'кофе'")

def find_dates():
    content = text.get('1.0', tk.END)
    positions = []

    # Перебираем все возможные десятисимвольные подстроки
    for i in range(len(content) - 9):
        sub = content[i:i+10]
        if is_valid_date_segment(sub):
            positions.append((i, i+10))

    # Снимаем старую подсветку
    text.tag_remove('match', '1.0', tk.END)

    # Подсвечиваем все найденные даты (фон lightblue)
    for start, end in positions:
        start_index = f"1.0 + {start} chars"
        end_index = f"1.0 + {end} chars"
        text.tag_add('match', start_index, end_index)
    text.tag_config('match', background='lightblue')

    # Выводим результат
    if positions:
        found = "\n".join([f"Дата: '{content[s:e]}' at pos {s}" for s, e in positions])
        messagebox.showinfo("Результаты", found)
    else:
        messagebox.showinfo("Результаты", "Ничего не найдено.")


def dfa_find_dates():
    content = text.get('1.0', tk.END)
    positions = []

    def is_valid_date_segment(s):
        # Быстрая проверка формата DD.MM.YYYY
        if len(s) != 10: return False
        if s[2] != '.' or s[5] != '.': return False
        try:
            day = int(s[:2])
            month = int(s[3:5])
            year = int(s[6:])
            if month < 1 or month > 12: return False
            if day < 1: return False

            # Кол-во дней в месяцах
            month_days = [31, 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28,
                          31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            return day <= month_days[month - 1]
        except:
            return False

    # Перебор всех подстрок длиной 10
    for i in range(len(content) - 9):
        sub = content[i:i+10]
        if is_valid_date_segment(sub):
            positions.append((i, i+10))

    # Подсветка
    text.tag_remove('match', '1.0', tk.END)
    for start, end in positions:
        start_index = f"1.0 + {start} chars"
        end_index = f"1.0 + {end} chars"
        text.tag_add('match', start_index, end_index)
    text.tag_config('match', background='lightblue')

    if positions:
        found = "\n".join([f"Дата: '{content[s:e]}' at pos {s}" for s, e in positions])
        messagebox.showinfo("Результаты (DFA)", found)
    else:
        messagebox.showinfo("Результаты (DFA)", "Ничего не найдено.")


# --- GUI ---
root = tk.Tk()
root.title("Регулярные выражения – ЛР6")

text = tk.Text(root, height=15, width=80)
text.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack()

btn1 = tk.Button(button_frame, text="Поиск целых чисел", command=find_integers)
btn2 = tk.Button(button_frame, text="Слова с 'кофе' (10 букв)", command=find_coffee_words)
btn3 = tk.Button(button_frame, text="Проверка даты", command=find_dates)
btn5 = tk.Button(button_frame, text="Поиск дат через автомат", command=dfa_find_dates)


btn1.grid(row=0, column=0, padx=5)
btn2.grid(row=0, column=1, padx=5)
btn3.grid(row=0, column=2, padx=5)
btn5.grid(row=0, column=3, pady=5)
root.mainloop()
 