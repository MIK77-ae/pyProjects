import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
from tkcalendar import Calendar, DateEntry
import json
import webbrowser # Библиотека для открытия ссылок в браузере
from urllib.parse import quote
import winsound
import os
import pandas as pd

# Глобальные переменные
task_data = {}
responsible_list = {
    "Иванов И.И.": "Менеджер",
    "Петров П.П.": "Разработчик",
    "Сидоров С.С.": "Дизайнер",
    "Козлов К.А.": "Тестировщик"
}

# Путь к файлу с данными
DATA_FILE = os.path.join(os.path.dirname(__file__), "tasks_and_responsibles.xlsx")
SOUND_ENABLED = True  # Глобальная переменная для управления звуком

def play_sound():
    """Воспроизводит системный звук"""
    if SOUND_ENABLED:
        try:
            winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
        except:
            pass

def toggle_sound():
    """Функция переключения звука"""
    global SOUND_ENABLED
    SOUND_ENABLED = not SOUND_ENABLED
    if SOUND_ENABLED:
        sound_button.config(text="🔊 Звук Вкл", bg="lightblue")
        show_message("Звук", "Звук включен")
    else:
        sound_button.config(text="🔇 Звук Выкл", bg="gray")
        show_message("Звук", "Звук выключен")

def generate_new_task_id():
    if not task_data:
        return "TASK-0001"
    try:
        # Извлекаем числовую часть из ID задачи
        max_id = max(int(task_id.split('-')[1]) if '-' in task_id else int(task_id) 
                    for task_id in task_data.keys())
        return f"TASK-{max_id + 1:04d}"
    except ValueError:
        # Если возникла ошибка при обработке ID, начинаем с TASK-0001
        return "TASK-0001"

def update_position(event=None):
    responsible = responsible_combo.get()
    if responsible in responsible_list:
        position_entry.delete(0, tk.END)
        position_entry.insert(0, responsible_list[responsible])

def update_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=current_time)
    root.after(1000, update_time)

def select_date(date_var):
    def set_date():
        date_var.set(cal.selection_get().strftime("%Y-%m-%d"))
        top.destroy()

    top = tk.Toplevel(root)
    top.title("Выберите дату")
    cal = Calendar(top, selectmode='day', date_pattern='y-mm-dd')
    cal.pack(padx=10, pady=10)
    ttk.Button(top, text="Выбрать", command=set_date).pack(pady=5)

def show_instructions():
    instruction_window = tk.Toplevel(root)
    instruction_window.title("Инструкция по работе с программой")
    instruction_window.geometry("800x600")
    instruction_window.configure(background="lightgreen")

    instruction_text = """Инструкция по работе с Task Manager

1. Основные функции:
   • Добавление задачи (кнопка "Добавить задачу")
   • Редактирование задачи (кнопка "Редактировать")
   • Удаление задачи (кнопка "Удалить")
   • Отметка о выполнении (кнопка "Отметить выполненной")
   • Поиск задач (поле "Поиск" и кнопка "Найти")
   • Поиск по дате (поле "Дата" и кнопка "Поиск по дате")
   • Поиск по ответственному (кнопка "Поиск по ответственному")
   • Связь с разработчиками (кнопка "Связь с разработчиками")

2. Отображение задач:
   • В списке задач отображается полная информация:
   • Специальные символы статуса:
     - ✓ - задача выполнена
     - ▲ - задача в работе
     - ❗ - срочная задача
   • Информация о задаче:
     - ID задачи
     - Название задачи
     - ФИО ответственного
     - Должность
     - Дата создания
     - Дата начала
     - Дата окончания
     - Дата последнего изменения

3. Цветовая индикация:
   • Светло-зеленый фон - выполненные задачи
   • Светло-розовый фон - срочные задачи

4. Добавление/Редактирование задачи:
   • Заполните название задачи
   • Выберите ответственного из списка (должность обновится автоматически)
   • Укажите даты начала и окончания
   • При необходимости отметьте "Срочная задача"

5. Поиск задач:
   • По тексту: введите текст в поле поиска (ищет по названию и ответственному)
   • По ID: введите ID задачи в поле поиска
   • По дате: выберите дату и нажмите "Поиск по дате"
   • По ответственному: нажмите "Поиск по ответственному"

6. Связь с разработчиками:
   • Email: a@yandex.ru
   • Время работы поддержки: Пн-Пт с 9:00 до 18:00 (МСК)
   • Способы связи:
     - Почтовый клиент
     - Проводник (создание файла)
     - Telegram
     - WhatsApp

7. Дополнительно:
   • Все изменения автоматически сохраняются
   • Звуковые уведомления можно включить/отключить
   • Задачи можно сортировать по разным параметрам"""

    instruction_text_widget = scrolledtext.ScrolledText(instruction_window, wrap=tk.WORD, 
                                                      width=80, height=30, bg="white")
    instruction_text_widget.pack(padx=10, pady=10)
    instruction_text_widget.insert(tk.END, instruction_text)
    instruction_text_widget.configure(state='disabled')

    tk.Button(instruction_window, text="Закрыть", command=instruction_window.destroy,
              bg="pink", width=20).pack(pady=10)

def show_message(title, message, message_type="info", parent=None):
    """Показывает сообщение с учетом настроек звука"""
    # Воспроизводим звук для всех типов сообщений, кроме подтверждений
    if message_type != "confirm":
        play_sound()
    
    dialog = tk.Toplevel(parent or root)
    dialog.title(title)
    dialog.geometry("300x150")
    dialog.configure(background="lightgreen")
    
    # Делаем окно модальным
    dialog.transient(parent or root)
    dialog.grab_set()
    
    # Добавляем сообщение
    msg_label = tk.Label(dialog, text=message, 
                       wraplength=250,
                       bg="lightgreen",
                       font=("Arial", 10))
    msg_label.pack(pady=20, padx=20)
    
    # Кнопка закрытия
    close_button = tk.Button(dialog, 
                           text="OK",
                           command=dialog.destroy,
                           bg="lightblue")
    close_button.pack(pady=10)
    
    # Ждем закрытия окна если это окно подтверждения
    if message_type == "confirm":
        dialog.result = False
        def on_yes():
            dialog.result = True
            dialog.destroy()
        
        def on_no():
            dialog.result = False
            dialog.destroy()
        
        close_button.pack_forget()
        tk.Button(dialog, text="Да", command=on_yes, bg="lightblue").pack(side=tk.LEFT, padx=20, pady=10)
        tk.Button(dialog, text="Нет", command=on_no, bg="pink").pack(side=tk.RIGHT, padx=20, pady=10)
        
        dialog.wait_window()
        return dialog.result
    
    return None

def sort_tasks(sort_type):
    """Сортирует задачи по выбранному критерию"""
    tasks_list = list(task_data.items())
    
    if sort_type == "По ID":
        return sorted(tasks_list, key=lambda x: x[0])
    elif sort_type == "По дате создания":
        return sorted(tasks_list, key=lambda x: x[1].get('created_date', datetime.now()))
    elif sort_type == "По дате начала":
        return sorted(tasks_list, key=lambda x: x[1]['start_date'])
    elif sort_type == "По дате окончания":
        return sorted(tasks_list, key=lambda x: x[1]['end_date'])
    elif sort_type == "По ответственному":
        return sorted(tasks_list, key=lambda x: x[1]['responsible'])
    elif sort_type == "По просроченности":
        current_date = datetime.now().date()
        def get_overdue_priority(task):
            if task[1].get('completed', False):
                return 3  # Выполненные задачи в конце
            days_left = (task[1]['end_date'].date() - current_date).days
            if days_left < 0:
                return 1  # Просроченные задачи вначале
            return 2  # Активные задачи посередине
        return sorted(tasks_list, key=get_overdue_priority)
    return tasks_list

def refresh_task_list():
    task_listBox.delete(0, tk.END)
    sorted_tasks = sort_tasks(sort_var.get())
    current_date = datetime.now().date()

    for task_id, task_info in sorted_tasks:
        # Определяем статус задачи
        status_symbol = ""
        if task_info.get('urgent', False):
            status_symbol += "❗"
        if task_info.get('completed', False):
            status_symbol += "✓"
        else:
            status_symbol += "▲"

        # Форматируем основную информацию о задаче
        display_text = (
            f"{status_symbol} ID: {task_id} | "
            f"Задача: {task_info['task']} | "
            f"Ответственный: {task_info['responsible']} | "
            f"Должность: {task_info['position']} | "
            f"Создано: {task_info.get('created_date', datetime.now()).strftime('%d.%m.%Y %H:%M')} | "
            f"Начало: {task_info['start_date'].strftime('%d.%m.%Y')} | "
            f"Окончание: {task_info['end_date'].strftime('%d.%m.%Y')} | "
            f"Изменено: {task_info['last_modified'].strftime('%d.%m.%Y %H:%M')}"
        )

        # Добавляем информацию о сроках
        if task_info.get('completed', False):
            display_text += " (Выполнено)"
        else:
            days_diff = (task_info['end_date'].date() - current_date).days
            if days_diff < 0:
                display_text += f" (просрочено на: {abs(days_diff)} дн.)"
            else:
                display_text += f" (осталось: {days_diff} дн.)"

        # Добавляем задачу в список
        task_listBox.insert(tk.END, display_text)

        # Устанавливаем цвет фона в зависимости от статуса
        if task_info.get('completed', False):
            task_listBox.itemconfig(tk.END, {'bg': 'light green'})
        elif task_info.get('urgent', False):
            task_listBox.itemconfig(tk.END, {'bg': 'light pink'})

def show_task_tooltip(event, info):
    """Показывает всплывающую подсказку с полной информацией о задаче"""
    try:
        index = task_listBox.nearest(event.y)
        if task_listBox.selection_includes(index):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=info, justify=tk.LEFT,
                           background="lightyellow", relief='solid', borderwidth=1,
                           font=("Arial", 10))
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
            
            tooltip.bind('<Leave>', lambda e: hide_tooltip())
            task_listBox.bind('<Leave>', lambda e: hide_tooltip())
    except:
        pass

def update_id_combobox():
    sorted_ids = sorted(task_data.keys())
    search_id_combo['values'] = sorted_ids

def update_employee_combobox():
    global employee_search_combo
    employee_search_combo['values'] = list(responsible_list.keys())

def clear_fields():
    task_entry.delete(0, tk.END)
    start_date_var.set("")
    end_date_var.set("")
    responsible_combo.set("")
    position_entry.delete(0, tk.END)
    urgent_var.set(False)

    task_id_entry.configure(state="normal")
    task_id_entry.delete(0, tk.END)
    task_id_entry.insert(0, generate_new_task_id())
    task_id_entry.configure(state="readonly")

def save_tasks_to_file(show_message_flag=True):
    try:
        # Создаем DataFrame для задач
        tasks_df = pd.DataFrame([
            {
                "ID задачи": task_id,
                "Задача": task["task"],
                "Дата начала": task["start_date"],
                "Дата окончания": task["end_date"],
                "Ответственный": task["responsible"],
                "Должность": task["position"],
                "Срочно": "Да" if task.get("urgent", False) else "Нет",
                "Выполнено": "Да" if task.get("completed", False) else "Нет",
                "Последнее изменение": task["last_modified"],
                "Дата создания": task.get("created_date", datetime.now())
            }
            for task_id, task in task_data.items()
        ])

        # Создаем DataFrame для ответственных
        responsibles_df = pd.DataFrame([
            {"ФИО": name, "Должность": position}
            for name, position in responsible_list.items()
        ])

        # Сохраняем в Excel с двумя листами
        with pd.ExcelWriter(DATA_FILE, engine='openpyxl', mode='w') as writer:
            tasks_df.to_excel(writer, sheet_name="Задачи", index=False)
            responsibles_df.to_excel(writer, sheet_name="Ответственные", index=False)

        if show_message_flag:
            show_message("Сохранение", "Данные успешно сохранены в файл")
            play_sound()
            
    except Exception as e:
        if show_message_flag:
            show_message("Ошибка", f"Ошибка при сохранении файла: {str(e)}", "error")

def load_tasks_from_file(show_message_flag=True):
    try:
        if os.path.exists(DATA_FILE):
            data = pd.read_excel(DATA_FILE, sheet_name="Задачи")
            responsibles_data = pd.read_excel(DATA_FILE, sheet_name="Ответственные")

            if not {"ID задачи", "Задача", "Дата начала", "Дата окончания",
                    "Ответственный", "Должность", "Срочно", "Выполнено",
                    "Последнее изменение", "Дата создания"}.issubset(data.columns):
                raise ValueError("Файл не содержит всех необходимых столбцов")

            task_data.clear()
            responsible_list.clear()

            for _, row in responsibles_data.iterrows():
                responsible_list[row["ФИО"]] = row["Должность"]

            for _, row in data.iterrows():
                task_id = str(row["ID задачи"])
                if not task_id.startswith("TASK-"):
                    task_id = f"TASK-{int(task_id):04d}"
                    
                task_data[task_id] = {
                    "task": row["Задача"],
                    "start_date": pd.to_datetime(row["Дата начала"]),
                    "end_date": pd.to_datetime(row["Дата окончания"]),
                    "responsible": row["Ответственный"],
                    "position": row["Должность"],
                    "completed": row["Выполнено"] == "Да",
                    "urgent": row["Срочно"] == "Да",
                    "last_modified": pd.to_datetime(row["Последнее изменение"]),
                    "created_date": pd.to_datetime(row.get("Дата создания", datetime.now()))
                }

            responsible_combo["values"] = list(responsible_list.keys())
            update_id_combobox()
            update_employee_combobox()
            refresh_task_list()

            task_id_entry.configure(state="normal")
            task_id_entry.delete(0, tk.END)
            task_id_entry.insert(0, generate_new_task_id())
            task_id_entry.configure(state="readonly")

            if show_message_flag:
                show_message("Загрузка", "Задачи и ответственные успешно загружены из файла")
                play_sound()
        else:
            if show_message_flag:
                show_message("Предупреждение", f"Файл {DATA_FILE} не найден", "warning")
    except Exception as e:
        if show_message_flag:
            show_message("Ошибка", f"Ошибка при загрузке файла: {str(e)}", "error")

def add_task():
    task = task_entry.get()
    responsible = responsible_combo.get()
    position = position_entry.get()

    if not task or not responsible or not position:
        show_message("Ошибка", "Заполните все поля!")
        return

    if not start_date_var.get() or not end_date_var.get():
        show_message("Ошибка", "Выберите даты начала и окончания!")
        return

    try:
        start_date_obj = datetime.strptime(start_date_var.get(), "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date_var.get(), "%Y-%m-%d")

        if end_date_obj <= start_date_obj:
            raise ValueError("Дата окончания должна быть позже даты начала.")

        current_time = datetime.now()
        task_id = task_id_entry.get()
        task_data[task_id] = {
            "task": task,
            "start_date": start_date_obj,
            "end_date": end_date_obj,
            "responsible": responsible,
            "position": position,
            "completed": False,
            "urgent": urgent_var.get(),
            "created_date": current_time,
            "last_modified": current_time
        }

        refresh_task_list()
        save_tasks_to_file(show_message_flag=False)
        update_id_combobox()
        clear_fields()
        show_message("Успех", "Задача добавлена!")
        play_sound()
    except ValueError as e:
        show_message("Ошибка", f"Ошибка даты: {e}")

def edit_task():
    selected_indices = task_listBox.curselection()
    if not selected_indices:
        show_message("Ошибка", "Выберите задачу для редактирования")
        return

    sorted_tasks = sort_tasks(sort_var.get())
    task_id = sorted_tasks[selected_indices[0]][0]
    task_info = task_data[task_id]

    edit_window = tk.Toplevel(root)
    edit_window.title("Редактирование задачи")
    edit_window.geometry("500x400")
    edit_window.configure(background="lightgreen")

    # Делаем окно модальным
    edit_window.transient(root)
    edit_window.grab_set()

    # Создаем и размещаем элементы управления
    tk.Label(edit_window, text="Задача:", bg="lightgreen").grid(row=0, column=0, pady=5, padx=5)
    task_edit = tk.Entry(edit_window, width=50)
    task_edit.insert(0, task_info['task'])
    task_edit.grid(row=0, column=1, columnspan=2, pady=5, padx=5)

    tk.Label(edit_window, text="Ответственный:", bg="lightgreen").grid(row=1, column=0, pady=5, padx=5)
    responsible_edit = ttk.Combobox(edit_window, values=list(responsible_list.keys()), width=47)
    responsible_edit.set(task_info['responsible'])
    responsible_edit.grid(row=1, column=1, columnspan=2, pady=5, padx=5)

    tk.Label(edit_window, text="Должность:", bg="lightgreen").grid(row=2, column=0, pady=5, padx=5)
    position_var = tk.StringVar(value=task_info['position'])
    position_edit = tk.Entry(edit_window, width=50, textvariable=position_var, state='readonly')
    position_edit.grid(row=2, column=1, columnspan=2, pady=5, padx=5)

    # Функция обновления должности при выборе сотрудника
    def update_position(*args):
        selected_employee = responsible_edit.get()
        if selected_employee in responsible_list:
            position_var.set(responsible_list[selected_employee])

    # Привязываем обновление должности к изменению выбранного сотрудника
    responsible_edit.bind('<<ComboboxSelected>>', update_position)

    tk.Label(edit_window, text="Дата начала:", bg="lightgreen").grid(row=3, column=0, pady=5, padx=5)
    start_date_edit = DateEntry(edit_window, width=12, background='darkblue',
                             foreground='white', borderwidth=2)
    start_date_edit.set_date(task_info['start_date'].date())
    start_date_edit.grid(row=3, column=1, pady=5, padx=5)

    tk.Label(edit_window, text="Дата окончания:", bg="lightgreen").grid(row=4, column=0, pady=5, padx=5)
    end_date_edit = DateEntry(edit_window, width=12, background='darkblue',
                           foreground='white', borderwidth=2)
    end_date_edit.set_date(task_info['end_date'].date())
    end_date_edit.grid(row=4, column=1, pady=5, padx=5)

    urgent_edit = tk.BooleanVar(value=task_info.get('urgent', False))
    urgent_checkbox = tk.Checkbutton(edit_window, text="Срочная задача",
                                 variable=urgent_edit, bg="lightgreen")
    urgent_checkbox.grid(row=5, column=1, pady=5, padx=5)

    def save_edit():
        try:
            # Получаем значения из полей ввода
            new_task = task_edit.get().strip()
            new_responsible = responsible_edit.get().strip()
            new_position = position_var.get()
            new_start_date = datetime.combine(start_date_edit.get_date(), datetime.min.time())
            new_end_date = datetime.combine(end_date_edit.get_date(), datetime.min.time())
            new_urgent = urgent_edit.get()

            if not all([new_task, new_responsible, new_position]):
                show_message("Ошибка", "Пожалуйста, заполните все поля")
                return

            if new_start_date > new_end_date:
                show_message("Ошибка", "Дата начала не может быть позже даты окончания")
                return

            # Обновляем данные задачи
            task_data[task_id].update({
                'task': new_task,
                'responsible': new_responsible,
                'position': new_position,
                'start_date': new_start_date,
                'end_date': new_end_date,
                'urgent': new_urgent,
                'last_modified': datetime.now()
            })

            refresh_task_list()
            save_tasks_to_file()
            edit_window.destroy()
            show_message("Успех", "Изменения сохранены!")
            play_sound()
        except Exception as e:
            show_message("Ошибка", f"Ошибка при сохранении: {str(e)}")

    tk.Button(edit_window, text="Сохранить изменения", command=save_edit,
              bg="orange", width=20).grid(row=6, column=1, pady=20, padx=5)

    tk.Button(edit_window, text="Отмена", command=edit_window.destroy,
              bg="pink", width=20).grid(row=6, column=0, pady=20, padx=5)

    # Обновляем должность при открытии окна
    update_position()

def delete_task():
    selected_indices = task_listBox.curselection()
    if not selected_indices:
        show_message("Ошибка", "Выберите задачу для удаления")
        return

    # Создаем окно подтверждения
    confirm_dialog = tk.Toplevel(root)
    confirm_dialog.title("Подтверждение")
    confirm_dialog.geometry("300x150")
    confirm_dialog.configure(background="lightgreen")
    
    # Делаем окно модальным
    confirm_dialog.transient(root)
    confirm_dialog.grab_set()
    
    # Добавляем сообщение
    msg_label = tk.Label(confirm_dialog, 
                       text="Вы уверены, что хотите удалить выбранную задачу?",
                       wraplength=250,
                       bg="lightgreen",
                       font=("Arial", 10))
    msg_label.pack(pady=20, padx=20)
    
    # Создаем фрейм для кнопок
    button_frame = tk.Frame(confirm_dialog, bg="lightgreen")
    button_frame.pack(pady=10)
    
    def on_yes():
        sorted_tasks = sort_tasks(sort_var.get())
        task_id = sorted_tasks[selected_indices[0]][0]
        del task_data[task_id]
        refresh_task_list()
        save_tasks_to_file(show_message_flag=False)
        update_id_combobox()
        show_message("Успех", "Задача удалена!")
        play_sound()
        confirm_dialog.destroy()
    
    def on_no():
        confirm_dialog.destroy()
    
    # Добавляем кнопки
    tk.Button(button_frame, 
             text="Да",
             command=on_yes,
             bg="lightblue").pack(side=tk.LEFT, padx=20)
             
    tk.Button(button_frame,
             text="Нет",
             command=on_no,
             bg="pink").pack(side=tk.LEFT, padx=20)

def mark_task_completed():
    selected_indices = task_listBox.curselection()
    if not selected_indices:
        show_message("Ошибка", "Выберите задачу")
        return

    sorted_tasks = sort_tasks(sort_var.get())
    task_id = sorted_tasks[selected_indices[0]][0]
    
    if task_data[task_id]["completed"]:
        show_message("Информация", "Задача уже отмечена как выполненная")
        return
        
    task_data[task_id]["completed"] = True
    task_data[task_id]["last_modified"] = datetime.now()
    
    refresh_task_list()
    save_tasks_to_file()
    show_message("Успех", "Задача отмечена как выполненная!")
    play_sound()

def search_task_by_id():
    task_id = search_id_var.get()
    if task_id in task_data:
        info = task_data[task_id]
        status = "✓ Выполнена" if info["completed"] else "▲ В работе"
        urgent = "❗ Да" if info.get("urgent", False) else "Нет"
        
        # Создаем отдельное окно для отображения информации
        info_window = tk.Toplevel(root)
        info_window.title(f"Информация о задаче {task_id}")
        info_window.geometry("600x400")
        info_window.configure(background="lightblue")
        
        # Создаем текстовый виджет с прокруткой
        text_widget = scrolledtext.ScrolledText(info_window, wrap=tk.WORD, 
                                              width=70, height=20,
                                              font=("Arial", 10))
        text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Форматируем информацию о задаче
        task_info = f"""
╔══ Основная информация ══╗
  ID задачи: {task_id}
  Название: {info['task']}
  
╠══ Статус ══╣
  Состояние: {status}
  Срочность: {urgent}
  
╠══ Ответственный ══╣
  ФИО: {info['responsible']}
  Должность: {info['position']}
  
╠══ Даты ══╣
  Создано: {info.get('created_date', datetime.now()).strftime('%d.%m.%Y %H:%M')}
  Начало: {info['start_date'].strftime('%d.%m.%Y')}
  Окончание: {info['end_date'].strftime('%d.%m.%Y')}
  Последнее изменение: {info['last_modified'].strftime('%d.%m.%Y %H:%M')}
  
╠══ Сроки ══╣"""

        # Добавляем информацию о сроках
        current_date = datetime.now().date()
        if info["completed"]:
            task_info += "\n  Задача выполнена"
        else:
            days_diff = (info['end_date'].date() - current_date).days
            if days_diff < 0:
                task_info += f"\n  ⚠ Просрочено на {abs(days_diff)} дней"
            else:
                task_info += f"\n  ✓ Осталось {days_diff} дней"
        
        task_info += "\n╚════════════════════╝"
        
        # Вставляем информацию в текстовый виджет
        text_widget.insert(tk.END, task_info)
        text_widget.configure(state='disabled')  # Делаем текст только для чтения
        
        # Добавляем кнопку закрытия
        tk.Button(info_window, text="Закрыть",
                 command=info_window.destroy,
                 bg="pink", width=20).pack(pady=10)
        
        play_sound()
    else:
        show_message("Ошибка", "Задача с указанным ID не найдена.", "error")

def search_by_responsible():
    search_window = tk.Toplevel(root)
    search_window.title("Поиск по ответственному")
    search_window.geometry("800x400")
    search_window.configure(background="lightblue")

    tk.Label(search_window, text="Выберите сотрудника:", bg="lightblue").pack(pady=5)
    
    global employee_search_combo
    employee_search_combo = ttk.Combobox(search_window, values=list(responsible_list.keys()), width=80)
    employee_search_combo.pack(pady=5)

    def search():
        selected_responsible = employee_search_combo.get()
        if not selected_responsible:
            show_message("Ошибка", "Выберите сотрудника")
            return

        filtered_tasks = []
        for task_id, task in task_data.items():
            if task['responsible'] == selected_responsible:
                filtered_tasks.append((task_id, task))
        
        if not filtered_tasks:
            show_message("Результат", f"Задачи для {selected_responsible} не найдены")
            return
        
        result_window = tk.Toplevel(search_window)
        result_window.title(f"Задачи для {selected_responsible}")
        result_window.geometry("1200x600")
        result_window.configure(background="lightblue")

        result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, 
                                              width=120, height=30, bg="white")
        result_text.pack(padx=10, pady=10)
        
        current_date = datetime.now().date()
        for task_id, task in filtered_tasks:
            # Определяем статус задачи
            status_symbol = ""
            if task.get('urgent', False):
                status_symbol += "❗"
            if task.get('completed', False):
                status_symbol += "✓"
            else:
                status_symbol += "▲"

            # Форматируем основную информацию о задаче
            task_info = (
                f"{status_symbol} ID: {task_id} | "
                f"Задача: {task['task']} | "
                f"Ответственный: {task['responsible']} | "
                f"Должность: {task['position']} | "
                f"Создано: {task.get('created_date', datetime.now()).strftime('%d.%m.%Y %H:%M')} | "
                f"Начало: {task['start_date'].strftime('%d.%m.%Y')} | "
                f"Окончание: {task['end_date'].strftime('%d.%m.%Y')} | "
                f"Изменено: {task['last_modified'].strftime('%d.%m.%Y %H:%M')}"
            )

            # Добавляем информацию о сроках
            if task.get('completed', False):
                task_info += " (Выполнено)"
            else:
                days_diff = (task['end_date'].date() - current_date).days
                if days_diff < 0:
                    task_info += f" (просрочено на: {abs(days_diff)} дн.)"
                else:
                    task_info += f" (осталось: {days_diff} дн.)"

            result_text.insert(tk.END, f"{task_info}\n{'-' * 100}\n\n")
        
        result_text.configure(state='disabled')
        
        tk.Button(result_window, text="Закрыть", command=result_window.destroy,
                 bg="pink", width=20).pack(pady=10)
        
        play_sound()

    tk.Button(search_window, text="Найти", command=search,
              bg="orange", width=20).pack(pady=10)
    tk.Button(search_window, text="Закрыть", command=search_window.destroy,
              bg="pink", width=20).pack(pady=5)

def search_by_end_date():
    search_date = end_date_search_var.get()
    if not search_date:
        show_message("Ошибка", "Выберите дату для поиска")
        return

    try:
        search_date_obj = datetime.strptime(search_date, "%Y-%m-%d").date()
        filtered_tasks = []
        
        for task_id, task in task_data.items():
            task_end_date = task['end_date'].date()
            if task_end_date == search_date_obj:
                filtered_tasks.append((task_id, task))
        
        if not filtered_tasks:
            show_message("Результат", f"Задачи на {search_date} не найдены")
            return
        
        result_window = tk.Toplevel(root)
        result_window.title(f"Задачи на {search_date}")
        result_window.geometry("1200x600")
        result_window.configure(background="lightblue")

        result_text = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, 
                                              width=120, height=30, bg="white")
        result_text.pack(padx=10, pady=10)
        
        current_date = datetime.now().date()
        for task_id, task in filtered_tasks:
            # Определяем статус задачи
            status_symbol = ""
            if task.get('urgent', False):
                status_symbol += "❗"
            if task.get('completed', False):
                status_symbol += "✓"
            else:
                status_symbol += "▲"

            # Форматируем основную информацию о задаче
            task_info = (
                f"{status_symbol} ID: {task_id} | "
                f"Задача: {task['task']} | "
                f"Ответственный: {task['responsible']} | "
                f"Должность: {task['position']} | "
                f"Создано: {task.get('created_date', datetime.now()).strftime('%d.%m.%Y %H:%M')} | "
                f"Начало: {task['start_date'].strftime('%d.%m.%Y')} | "
                f"Окончание: {task['end_date'].strftime('%d.%m.%Y')} | "
                f"Изменено: {task['last_modified'].strftime('%d.%m.%Y %H:%M')}"
            )

            # Добавляем информацию о сроках
            if task.get('completed', False):
                task_info += " (Выполнено)"
            else:
                days_diff = (task['end_date'].date() - current_date).days
                if days_diff < 0:
                    task_info += f" (просрочено на: {abs(days_diff)} дн.)"
                else:
                    task_info += f" (осталось: {days_diff} дн.)"

            result_text.insert(tk.END, f"{task_info}\n{'-' * 100}\n\n")
        
        result_text.configure(state='disabled')
        
        tk.Button(result_window, text="Закрыть", command=result_window.destroy,
                 bg="pink", width=20).pack(pady=10)
        
        play_sound()
    except ValueError:
        show_message("Ошибка", "Неверный формат даты")

def contact_developers():
    contact_window = tk.Toplevel(root)
    contact_window.title("Связь с разработчиками")
    contact_window.geometry("400x400")
    contact_window.configure(background="lightblue")
    
    # Информационная секция
    info_frame = tk.LabelFrame(contact_window, text="Информация", bg="lightblue", padx=10, pady=5)
    info_frame.pack(fill="x", padx=10, pady=5)
    
    info_text = """Email: a@yandex.ru

Время работы поддержки:
Пн-Пт: 9:00 - 18:00 (МСК)"""
    
    info_label = tk.Label(info_frame, text=info_text, bg="lightblue", justify=tk.LEFT)
    info_label.pack(pady=5, padx=5)
    
    # Email секция
    email_frame = tk.LabelFrame(contact_window, text="Отправить Email", bg="lightblue", padx=10, pady=5)
    email_frame.pack(fill="x", padx=10, pady=5)
    
    tk.Button(email_frame, text="Почтовый клиент", command=lambda: open_email_client(),
              bg="lightgreen", width=20).pack(side=tk.LEFT, padx=5, pady=5)
    
    tk.Button(email_frame, text="Проводник", command=lambda: create_email_file(),
              bg="lightgreen", width=20).pack(side=tk.LEFT, padx=5, pady=5)
    
    # Мессенджеры секция
    messenger_frame = tk.LabelFrame(contact_window, text="Написать в мессенджер", bg="lightblue", padx=10, pady=5)
    messenger_frame.pack(fill="x", padx=10, pady=5)
    
    telegram_button = tk.Button(messenger_frame, text="Telegram", command=lambda: open_telegram(),
                               bg="lightblue", width=20)
    telegram_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    whatsapp_button = tk.Button(messenger_frame, text="WhatsApp", command=lambda: open_whatsapp(),
                               bg="lightgreen", width=20)
    whatsapp_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Кнопка закрытия
    tk.Button(contact_window, text="Закрыть", command=contact_window.destroy,
             bg="pink", width=20).pack(pady=10)

def format_task_info(task_id, task):
    # Форматируем информацию о задаче с добавлением информации о сроках
    current_date = datetime.now().date()
    end_date = task['end_date'].date()
    days_diff = (end_date - current_date).days
    
    status_symbol = ""
    if task.get('urgent', False):
        status_symbol += "❗"
    if task.get('completed', False):
        status_symbol += "✓"
    else:
        status_symbol += "▲"

    task_info = (
        f"{status_symbol} ID: {task_id} | "
        f"Задача: {task['task']} | "
        f"Ответственный: {task['responsible']} | "
        f"Должность: {task['position']} | "
        f"Создано: {task.get('created_date', datetime.now()).strftime('%d.%m.%Y %H:%M')} | "
        f"Начало: {task['start_date'].strftime('%d.%m.%Y')} | "
        f"Окончание: {task['end_date'].strftime('%d.%m.%Y')} | "
        f"Изменено: {task['last_modified'].strftime('%d.%m.%Y %H:%M')}"
    )
    
    # Добавляем информацию о сроках
    if task.get('completed', False):
        task_info += "\nСтатус: Выполнено"
    elif days_diff < 0:
        task_info += f"\nСтатус: Просрочено на {abs(days_diff)} дней"
    else:
        task_info += f"\nСтатус: До завершения осталось {days_diff} дней"
    
    return task_info

# Создание главного окна и настройка интерфейса
root = tk.Tk()
root.title("Task Manager")
root.geometry("1200x800")
root.configure(background="lightgreen")

# Инициализация переменных
start_date_var = tk.StringVar(root)
end_date_var = tk.StringVar(root)
urgent_var = tk.BooleanVar()
sort_var = tk.StringVar(root)
sort_var.set("По дате окончания")
employee_search_var = tk.StringVar(root)
end_date_search_var = tk.StringVar(root)
search_id_var = tk.StringVar(root)

# Создание employee_search_combo до его использования
employee_search_combo = ttk.Combobox(root, width=47)
employee_search_combo['values'] = list(responsible_list.keys())

# Создание меню и элементов интерфейса
menu_frame = tk.Frame(root, bg="lightgreen")
menu_frame.grid(row=0, column=0, columnspan=3, pady=5, padx=5, sticky="ew")

# Левая часть меню
left_menu = tk.Frame(menu_frame, bg="lightgreen")
left_menu.pack(side=tk.LEFT)

# Кнопки для работы с файлами
tk.Button(left_menu, text=" Загрузить из файла", 
         command=lambda: load_tasks_from_file(True), 
         bg="#90EE90", 
         width=20).pack(side=tk.LEFT, padx=5)

tk.Button(left_menu, text=" Сохранить изменения", 
         command=lambda: save_tasks_to_file(), 
         bg="#90EE90", 
         width=20).pack(side=tk.LEFT, padx=5)

tk.Button(left_menu, text="Инструкция", 
         command=show_instructions, 
         bg="lightblue", 
         width=20).pack(side=tk.LEFT, padx=5)

tk.Button(left_menu, text="Связь с разработчиками", 
         command=contact_developers, 
         bg="lightblue", 
         width=20).pack(side=tk.LEFT, padx=5)

# Правая часть меню (для времени)
right_menu = tk.Frame(menu_frame, bg="lightgreen")
right_menu.pack(side=tk.RIGHT)

# Кнопка управления звуком
sound_button = tk.Button(right_menu, 
                        text=" Звук Вкл",
                        command=toggle_sound,
                        bg="lightblue", 
                        width=12)
sound_button.pack(side=tk.LEFT, padx=5)

time_label = tk.Label(right_menu, text="", bg="lightgreen", font=("Arial", 12))
time_label.pack(side=tk.RIGHT, padx=5)

# Фрейм для сортировки и поиска
search_frame = tk.Frame(root, bg="lightgreen")
search_frame.grid(row=14, column=0, columnspan=4, pady=5)

# Сортировка
tk.Label(search_frame, text="Сортировать по:", bg="lightgreen").pack(side=tk.LEFT, padx=5)
sort_combo = ttk.Combobox(search_frame, textvariable=sort_var, 
                         values=["По ID", "По дате создания", "По дате начала", 
                                "По дате окончания", "По просроченности", "По ответственному"])
sort_combo.pack(side=tk.LEFT, padx=5)
sort_combo.bind("<<ComboboxSelected>>", lambda e: refresh_task_list())

# Поиск по ID
tk.Button(search_frame, text="Найти по ID", command=search_task_by_id,
         bg="orange", width=15).pack(side=tk.LEFT, padx=5)

# Поиск по ответственному
tk.Button(search_frame, text="Поиск по ответственному", command=search_by_responsible,
         bg="orange", width=20).pack(side=tk.LEFT, padx=5)

# Поиск по дате
tk.Label(search_frame, text="Дата:", bg="lightgreen").pack(side=tk.LEFT, padx=5)
end_date_search_var = tk.StringVar()
end_date_search_entry = DateEntry(search_frame, width=12, textvariable=end_date_search_var,
                                date_pattern='yyyy-mm-dd')
end_date_search_entry.pack(side=tk.LEFT, padx=5)
tk.Button(search_frame, text="Поиск по дате", command=search_by_end_date,
         bg="orange", width=15).pack(side=tk.LEFT, padx=5)

# Время и поиск по ID
tk.Label(root, text="Поиск задачи по ID:", bg="lightgreen").grid(row=3, column=0, pady=5, padx=5)
search_id_combo = ttk.Combobox(root, textvariable=search_id_var, width=47)
search_id_combo.grid(row=3, column=1, pady=5, padx=5)
tk.Button(root, text="Найти по ID", command=search_task_by_id, 
         bg="lightblue", width=20).grid(row=3, column=2, pady=5, padx=5)

# Основные поля ввода
tk.Label(root, text="ID задачи:", bg="lightgreen").grid(row=4, column=0, pady=5, padx=5)
task_id_entry = tk.Entry(root, width=50)
task_id_entry.grid(row=4, column=1, pady=5, padx=5)
task_id_entry.configure(state="readonly")

tk.Label(root, text="Задача:", bg="lightgreen").grid(row=5, column=0, pady=5, padx=5)
task_entry = tk.Entry(root, width=50)
task_entry.grid(row=5, column=1, pady=5, padx=5)

# Даты
tk.Label(root, text="Дата начала:", bg="lightgreen").grid(row=6, column=0, pady=5, padx=5)
start_date_entry = tk.Entry(root, textvariable=start_date_var, width=50)
start_date_entry.grid(row=6, column=1, pady=5, padx=5)
tk.Button(root, text="Выбрать", command=lambda: select_date(start_date_var),
         bg="lightblue").grid(row=6, column=2, pady=5, padx=5)

tk.Label(root, text="Дата окончания:", bg="lightgreen").grid(row=7, column=0, pady=5, padx=5)
end_date_entry = tk.Entry(root, textvariable=end_date_var, width=50)
end_date_entry.grid(row=7, column=1, pady=5, padx=5)
tk.Button(root, text="Выбрать", command=lambda: select_date(end_date_var),
         bg="lightblue").grid(row=7, column=2, pady=5, padx=5)

# Ответственный и должность
tk.Label(root, text="Ответственный:", bg="lightgreen").grid(row=8, column=0, pady=5, padx=5)
responsible_combo = ttk.Combobox(root, width=47)
responsible_combo.grid(row=8, column=1, pady=5, padx=5)
responsible_combo.bind("<<ComboboxSelected>>", update_position)

tk.Label(root, text="Должность:", bg="lightgreen").grid(row=9, column=0, pady=5, padx=5)
position_entry = tk.Entry(root, width=50)
position_entry.grid(row=9, column=1, pady=5, padx=5)

# Чекбокс для срочных задач
urgent_checkbox = tk.Checkbutton(root, text="Срочная задача", variable=urgent_var, bg="lightgreen")
urgent_checkbox.grid(row=9, column=2, pady=5, padx=5)

# Список задач с полосой прокрутки
task_frame = tk.Frame(root)
task_frame.grid(row=10, column=0, columnspan=3, pady=10, padx=5, sticky="nsew")

# Вертикальный скролл
v_scrollbar = tk.Scrollbar(task_frame)
v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Горизонтальный скролл
h_scrollbar = tk.Scrollbar(task_frame, orient=tk.HORIZONTAL)
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

# Список задач с поддержкой обоих скроллов
task_listBox = tk.Listbox(task_frame, 
                         width=150, 
                         height=20,
                         xscrollcommand=h_scrollbar.set,
                         yscrollcommand=v_scrollbar.set)
task_listBox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Привязка скроллов к списку
v_scrollbar.config(command=task_listBox.yview)
h_scrollbar.config(command=task_listBox.xview)

# Фрейм для кнопок управления
button_frame = tk.Frame(root, bg="lightgreen")
button_frame.grid(row=11, column=0, columnspan=3, pady=10)

# Первый ряд кнопок
tk.Button(button_frame, text="Добавить задачу", 
         command=add_task, 
         bg="lightblue", width=35).grid(row=0, column=0, pady=5, padx=5)

tk.Button(button_frame, text="Удалить задачу", 
         command=delete_task, 
         bg="pink", width=35).grid(row=0, column=1, pady=5, padx=5)

tk.Button(button_frame, text="Редактировать задачу", 
         command=edit_task, 
         bg="lightyellow", width=35).grid(row=0, column=2, pady=5, padx=5)

# Второй ряд кнопок
tk.Button(button_frame, text="Отметить как выполненную", 
         command=mark_task_completed, 
         bg="lightgreen", width=35).grid(row=1, column=0, columnspan=3, pady=5, padx=5)

# Настройка расширения окна
root.grid_rowconfigure(10, weight=1)
for i in range(3):
    root.grid_columnconfigure(i, weight=1)

# Запуск приложения
if __name__ == "__main__":
    update_time()
    load_tasks_from_file(show_message_flag=False)
    root.mainloop() 