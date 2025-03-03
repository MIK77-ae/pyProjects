import telebot
from telebot import types as tg_types
from datetime import datetime, timedelta
import pytz
import threading
import time
import json
from collections import defaultdict
import calendar
import requests
import random

# --- Константы ---
BOT_TOKEN = 'вставьте токен своего бота (Вы можете получить его через @BotFather в Телеграм)'
WEATHER_API_KEY = 'вставьте токен своего API (Вы можете получить его на сайте api.openweathermap.org)'
EXCHANGE_API_KEY = 'вставьте токен своего API (Вы можете получить его на сайте exchangerate-api.com)('

# Основные валюты и города
CURRENCIES = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'RUB', 'AUD', 'CAD']
RUSSIAN_CITIES = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань"]
WORLD_CAPITALS = ["Вашингтон", "Пекин", "Лондон", "Токио", "Берлин", "Париж", "Сеул", "Рим", "Оттава", "Нью-Дели"]

# --- База данных ---
DATA_FILE = "C:/PythonProjects/pythonProject/Telegram bot organizer/reminders.json"

bot = telebot.TeleBot(BOT_TOKEN)

# --- Класс для системы напоминаний ---
class ReminderSystem:
    def __init__(self):
        self.reminders = defaultdict(list)
        self.load_reminders()

    def load_reminders(self):
        """Загрузка напоминаний из файла."""
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                self.reminders = defaultdict(list, json.load(file))
            print("Данные напоминаний загружены.")
        except FileNotFoundError:
            print("Файл с напоминаниями отсутствует, создается новый.")
        except Exception as e:
            print(f"Ошибка загрузки напоминаний: {e}")

    def save_reminders(self):
        """Сохранение напоминаний в файл."""
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(self.reminders, file, ensure_ascii=False, indent=4)
            print("Данные напоминаний сохранены.")
        except Exception as e:
            print(f"Ошибка сохранения напоминаний: {e}")

    def add_reminder(self, user_id, text, event_time):
        """Добавление нового напоминания."""
        self.reminders[user_id].append({"text": text, "time": event_time.isoformat()})
        self.save_reminders()

    def get_reminders(self, user_id):
        """Получение всех напоминаний пользователя."""
        return self.reminders.get(user_id, [])

    def delete_reminder(self, user_id, index):
        """Удаление напоминания по индексу."""
        if user_id in self.reminders and 0 <= index < len(self.reminders[user_id]):
            del self.reminders[user_id][index]
            self.save_reminders()

    def notify_reminders(self):
        """Проверка и отправка уведомлений о событиях."""
        while True:
            now = datetime.now(pytz.timezone("Europe/Moscow"))
            for user_id, reminders in list(self.reminders.items()):
                for reminder in reminders:
                    reminder_time = datetime.fromisoformat(reminder['time'])
                    if reminder_time.tzinfo is None:
                        reminder_time = pytz.timezone("Europe/Moscow").localize(reminder_time)
                    time_to_event = reminder_time - now

                    if timedelta(minutes=0) <= time_to_event <= timedelta(minutes=30):
                        bot.send_message(user_id, f"🔔 Напоминание о событии: {reminder['text']} в {reminder_time.strftime('%H:%M')}!")
                        self.delete_reminder(user_id, reminders.index(reminder))

            time.sleep(30)

# Создание экземпляра системы напоминаний
reminder_system = ReminderSystem()

# --- Научные факты ---
SCIENTIFIC_FACTS = [
    "🧬 99% ДНК человека совпадает с ДНК шимпанзе",
    "🌍 Земля совершает полный оборот вокруг своей оси за 23 часа 56 минут и 4 секунды",
    "⚡ Молния нагревает воздух до температуре, в пять раз превышающей температуре поверхности Солнца",
    "🧠 Мозг человека генерирует достаточно электричества, чтобы зажечь маленькую лампочку",
    "🦈 Акулы существовали на Земле раньше, чем деревья",
    "🌊 Океаны содержат 99% жизненного пространства на Земле",
    "🦕 Тираннозавр Рекс жил ближе к нашему времени, чем к времени стегозавра",
    "💫 В нашей галактике Млечный Путь около 400 миллиардов звезд",
    "🧪 Один грамм ДНК может хранить 215 петабайт информации",
    "🔬 В одной капле воды содержится больше атомов, чем звезд во всей нашей галактике"
]

# Текст справки
HELP_TEXT = """
👋 Добро пожаловать в бот-органайзер!

📅 **Управление встречами**:
• Создать встречу - кнопка "📅 Запланировать встречу"
• Просмотр встреч - кнопка "📋 Мои встречи"
• Редактировать встречи - команда /edit

💱 **Обмен валют**:
• Поддерживаемые валюты: USD, EUR, GBP, JPY, CNY, RUB, AUD, CAD
• Актуальные курсы в реальном времени
• Точные расчеты с поддержкой копеек

🌡 **Погода**:
• Погода в любом городе мира
• Температура, влажность, описание
• Популярные города в быстром доступе

⚡️ **Дополнительно**:
• Точное время и дата (MSK)
• Интересные научные факты
• Автоматические уведомления

🆘 **Нужна помощь?**
• Telegram: @OrganizerSupportBot
• Email: support@organizerbot.ru
• Время работы: 24/7

Команды:
/start - Перезапуск бота
/help - Это сообщение
/edit - Редактирование встреч
"""

# --- Команды и обработчики ---
@bot.message_handler(commands=['start', 'help'])
def send_help(message):
    """Вывод приветствия и основного меню."""
    if message.text == '/start':
        welcome_text = (
            "👋 Добро пожаловать в бот-органайзер!\n\n"
            "🔹 Используйте кнопки меню для работы с ботом\n"
            "🔹 Команда /help для подробной справки\n"
            "🔹 Служба поддержки: @OrganizerSupportBot\n"
        )
        markup = tg_types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📅 Запланировать встречу", "📋 Мои встречи")
        markup.add("🌡 Погода", "💱 Обмен валют")
        markup.add("⏰ Дата и время", "🧠 Интересный факт")
        bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
    elif message.text == '/help':
        bot.send_message(message.chat.id, HELP_TEXT, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "⏰ Дата и время")
def send_time(message):
    """Отправка текущего времени и даты."""
    now = datetime.now(pytz.timezone("Europe/Moscow"))
    bot.send_message(message.chat.id, f"📅 {now.strftime('%d.%m.%Y')} 🕒 {now.strftime('%H:%M:%S')} (по Москве)")

@bot.message_handler(func=lambda message: message.text == "🌡 Погода")
def weather_start(message):
    """Начало диалога о погоде."""
    markup = tg_types.InlineKeyboardMarkup(row_width=2)
    
    for city in RUSSIAN_CITIES + WORLD_CAPITALS:
        markup.add(tg_types.InlineKeyboardButton(city, callback_data=f"weather_{city}"))
    markup.add(tg_types.InlineKeyboardButton("Введите город вручную", callback_data="weather_manual"))
    bot.send_message(message.chat.id, "Выберите город или введите вручную:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('weather_'))
def weather_callback(call):
    """Обработчик выбора города для погоды."""
    if call.data == "weather_manual":
        bot.send_message(call.message.chat.id, "Введите название города:")
        bot.register_next_step_handler(call.message, process_weather_input)
    else:
        city = call.data.split('_')[1]
        send_weather(call.message, city)

def process_weather_input(message):
    """Обработка ввода города вручную."""
    send_weather(message, message.text.strip())

def send_weather(message, city):
    """Получение и отправка данных о погоде."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url).json()
        weather_data = (
            f"🌡️ Погода в {city}:\n"
            f"Температура: {response['main']['temp']}°C\n"
            f"Ощущается как: {response['main']['feels_like']}°C\n"
            f"Влажность: {response['main']['humidity']}%\n"
            f"Описание: {response['weather'][0]['description'].capitalize()}"
        )
        bot.send_message(message.chat.id, weather_data)
    except KeyError:
        bot.send_message(message.chat.id, "Город не найден.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {str(e)}")

@bot.message_handler(func=lambda message: message.text == "📅 Запланировать встречу")
def plan_meeting(message):
    """Начало планирования встречи."""
    now = datetime.now(pytz.timezone("Europe/Moscow"))
    send_calendar(message.chat.id, now.year, now.month)

def send_calendar(chat_id, year, month):
    """Отправка календаря."""
    markup = tg_types.InlineKeyboardMarkup(row_width=7)
    
    # Заголовок с месяцем и годом
    markup.row(tg_types.InlineKeyboardButton(
        f'{calendar.month_name[month]} {year}',
        callback_data='ignore'
    ))
    
    # Дни недели
    days_of_week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    week_row = [tg_types.InlineKeyboardButton(day, callback_data='ignore') for day in days_of_week]
    markup.row(*week_row)
    
    # Календарная сетка
    month_calendar = calendar.monthcalendar(year, month)
    for week in month_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(tg_types.InlineKeyboardButton(" ", callback_data='ignore'))
            else:
                row.append(tg_types.InlineKeyboardButton(
                    str(day),
                    callback_data=f'calendar_{year}_{month}_{day}'
                ))
        markup.row(*row)
    
    # Кнопки навигации
    nav_row = []
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    nav_row.append(tg_types.InlineKeyboardButton(
        "<<",
        callback_data=f'nav_{prev_year}_{prev_month}'
    ))
    nav_row.append(tg_types.InlineKeyboardButton(
        ">>",
        callback_data=f'nav_{next_year}_{next_month}'
    ))
    markup.row(*nav_row)
    
    bot.send_message(chat_id, "Выберите дату:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith(('calendar_', 'nav_')))
def calendar_callback(call):
    """Обработчик нажатий на календарь."""
    try:
        # Проверяем, редактируется ли существующая встреча
        editing_meeting = getattr(calendar_callback, 'editing_meeting', None)
        
        prefix, *data = call.data.split('_')
        if prefix == 'nav':
            year, month = map(int, data)
            send_calendar(call.message.chat.id, year, month)
        elif prefix == 'calendar':
            year, month, day = map(int, data)
            selected_date = datetime(year, month, day)
            
            if editing_meeting is not None:
                # Если редактируем встречу, передаем индекс
                send_time_picker(call.message.chat.id, selected_date, editing_meeting)
                # Сбрасываем флаг редактирования
                calendar_callback.editing_meeting = None
            else:
                # Если создаем новую встречу
                send_time_picker(call.message.chat.id, selected_date)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка: {str(e)}")

def send_time_picker(chat_id, date, editing_meeting=None):
    """Отправка выбора времени."""
    markup = tg_types.InlineKeyboardMarkup(row_width=4)
    hours = []
    for hour in range(0, 24):
        callback_data = (f'time_{date.strftime("%Y-%m-%d")}_{hour}'
                        f'_{editing_meeting if editing_meeting is not None else "new"}')
        hours.append(tg_types.InlineKeyboardButton(
            f"{hour:02d}:00",
            callback_data=callback_data
        ))
    for i in range(0, len(hours), 4):
        markup.row(*hours[i:i+4])
    bot.send_message(chat_id, "Выберите время:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('time_'))
def time_callback(call):
    """Обработчик выбора времени."""
    try:
        _, date_str, hour, meeting_status = call.data.split('_')
        selected_datetime = datetime.strptime(f"{date_str} {hour}", "%Y-%m-%d %H")
        
        if meeting_status == "new":
            # Создание новой встречи
            bot.send_message(call.message.chat.id, "Введите описание встречи:")
            bot.register_next_step_handler(call.message, save_meeting, selected_datetime)
        else:
            # Обновление существующей встречи
            meeting_index = int(meeting_status)
            reminders = reminder_system.get_reminders(str(call.message.chat.id))
            if 0 <= meeting_index < len(reminders):
                reminder = reminders[meeting_index]
                reminder['time'] = selected_datetime.isoformat()
                reminder_system.save_reminders()
                bot.send_message(
                    call.message.chat.id,
                    f"✅ Время встречи обновлено на {selected_datetime.strftime('%d.%m.%Y %H:%M')}"
                )
            else:
                bot.send_message(call.message.chat.id, "❌ Ошибка: встреча не найдена.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка: {str(e)}")

def save_meeting(message, selected_datetime):
    """Сохранение встречи."""
    reminder_system.add_reminder(str(message.chat.id), message.text, selected_datetime)
    bot.send_message(
        message.chat.id,
        f"✅ Встреча запланирована на {selected_datetime.strftime('%d.%m.%Y %H:%M')}\n"
        f"📝 Описание: {message.text}"
    )

@bot.message_handler(func=lambda message: message.text == "📋 Мои встречи")
def show_meetings(message):
    """Показ списка встреч."""
    chat_id = str(message.chat.id)
    print(f"Текущий ID чата: {chat_id}")
    print(f"Все напоминания: {reminder_system.reminders}")
    
    reminders = reminder_system.get_reminders(chat_id)
    if not reminders:
        bot.send_message(message.chat.id, "У вас нет запланированных встреч.")
        return
    
    response = "📋 Ваши встречи:\n\n"
    for i, reminder in enumerate(reminders, 1):
        event_time = datetime.fromisoformat(reminder['time'])
        response += f"{i}. {event_time.strftime('%d.%m.%Y %H:%M')} - {reminder['text']}\n"
    
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: message.text == "🧠 Интересный факт")
def send_fact(message):
    """Отправка случайного научного факта."""
    fact = random.choice(SCIENTIFIC_FACTS)
    bot.send_message(message.chat.id, fact)

@bot.message_handler(func=lambda message: message.text == "💱 Обмен валют")
def exchange_start(message):
    """Начало обмена валют."""
    markup = tg_types.InlineKeyboardMarkup(row_width=2)
    for currency in CURRENCIES:
        markup.add(tg_types.InlineKeyboardButton(
            currency,
            callback_data=f'from_{currency}'
        ))
    bot.send_message(message.chat.id, "Выберите исходную валюту:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('from_'))
def select_from_currency(call):
    """Выбор исходной валюты."""
    from_currency = call.data.split('_')[1]
    markup = tg_types.InlineKeyboardMarkup(row_width=2)
    for currency in CURRENCIES:
        if currency != from_currency:
            markup.add(tg_types.InlineKeyboardButton(
                currency,
                callback_data=f'to_{from_currency}_{currency}'
            ))
    bot.edit_message_text(
        "Выберите целевую валюту:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('to_'))
def select_to_currency(call):
    """Выбор целевой валюты."""
    _, from_currency, to_currency = call.data.split('_')
    bot.edit_message_text(
        f"Введите сумму в {from_currency}:",
        call.message.chat.id,
        call.message.message_id
    )
    bot.register_next_step_handler(
        call.message,
        process_conversion,
        from_currency,
        to_currency
    )

def process_conversion(message, from_currency, to_currency):
    """Обработка конвертации валют."""
    try:
        amount = float(message.text.replace(',', '.'))
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/pair/{from_currency}/{to_currency}/{amount}"
        response = requests.get(url).json()
        
        if response.get('result') == 'success':
            result = response['conversion_result']
            rate = response['conversion_rate']
            bot.send_message(
                message.chat.id,
                f"💱 Конвертация:\n"
                f"{amount:.2f} {from_currency} = {result:.2f} {to_currency}\n"
                f"Курс: 1 {from_currency} = {rate:.4f} {to_currency}"
            )
        else:
            bot.send_message(message.chat.id, "Ошибка при получении курса валют.")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

@bot.message_handler(commands=['edit'])
def edit_meetings(message):
    """Редактирование встреч."""
    reminders = reminder_system.get_reminders(str(message.chat.id))
    if not reminders:
        bot.send_message(message.chat.id, "У вас нет запланированных встреч для редактирования.")
        return
    
    markup = tg_types.InlineKeyboardMarkup(row_width=1)
    for i, reminder in enumerate(reminders):
        event_time = datetime.fromisoformat(reminder['time'])
        button_text = f"{event_time.strftime('%d.%m.%Y %H:%M')} - {reminder['text'][:30]}"
        markup.add(tg_types.InlineKeyboardButton(
            button_text,
            callback_data=f'edit_{i}'
        ))
    
    bot.send_message(
        message.chat.id,
        "Выберите встречу для редактирования:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('edit_'))
def edit_meeting_options(call):
    """Выбор действия для редактирования встречи."""
    meeting_index = int(call.data.split('_')[1])
    markup = tg_types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        tg_types.InlineKeyboardButton("Изменить время", callback_data=f'change_time_{meeting_index}'),
        tg_types.InlineKeyboardButton("Изменить описание", callback_data=f'change_desc_{meeting_index}'),
        tg_types.InlineKeyboardButton("Удалить", callback_data=f'delete_{meeting_index}')
    )
    
    reminders = reminder_system.get_reminders(str(call.message.chat.id))
    if 0 <= meeting_index < len(reminders):
        reminder = reminders[meeting_index]
        event_time = datetime.fromisoformat(reminder['time'])
        bot.edit_message_text(
            f"Встреча: {event_time.strftime('%d.%m.%Y %H:%M')}\n"
            f"Описание: {reminder['text']}\n\n"
            "Выберите действие:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=markup
        )

@bot.callback_query_handler(func=lambda call: call.data.startswith(('change_time_', 'change_desc_', 'delete_')))
def process_meeting_edit(call):
    """Обработка редактирования встречи."""
    action = call.data.split('_')[0]
    meeting_index = int(call.data.split('_')[-1])
    
    if action == 'delete':
        reminder_system.delete_reminder(str(call.message.chat.id), meeting_index)
        bot.edit_message_text(
            "✅ Встреча удалена!",
            call.message.chat.id,
            call.message.message_id
        )
    elif action == 'change':
        what = call.data.split('_')[1]
        if what == 'time':
            # Устанавливаем флаг редактирования с индексом встречи
            calendar_callback.editing_meeting = meeting_index
            now = datetime.now(pytz.timezone("Europe/Moscow"))
            send_calendar(call.message.chat.id, now.year, now.month)
        elif what == 'desc':
            bot.send_message(call.message.chat.id, "Введите новое описание встречи:")
            bot.register_next_step_handler(
                call.message,
                save_new_description,
                meeting_index
            )

def save_new_description(message, meeting_index):
    """Сохранение нового описания встречи."""
    reminders = reminder_system.get_reminders(str(message.chat.id))
    if 0 <= meeting_index < len(reminders):
        reminder = reminders[meeting_index]
        reminder['text'] = message.text
        reminder_system.save_reminders()
        bot.send_message(
            message.chat.id,
            "✅ Описание встречи обновлено!"
        )
    else:
        bot.send_message(message.chat.id, "❌ Ошибка: встреча не найдена.")

# Запуск потока уведомлений
reminder_thread = threading.Thread(target=reminder_system.notify_reminders, daemon=True)
reminder_thread.start()

# Запуск бота
if __name__ == "__main__":
    try:
        print("Инициализация бота...")
        bot.delete_webhook(drop_pending_updates=True)
        time.sleep(1)
        print("Бот запущен!")
        bot.infinity_polling()
    except Exception as e:
        print(f"Ошибка: {e}")
