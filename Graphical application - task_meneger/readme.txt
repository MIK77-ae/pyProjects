Файл test_data.py генерирует тестовые данные для работы приложения task_meneger.py
и сохраняет их в файл tasks_and_responsibles.xlsx.
До запуска приложения надо запустить файл test_data.py (проверить верный путь до файла tasks_and_responsibles.xlsx в коде),
а затем запустить task_meneger.py (проверить путь до файла tasks_and_responsibles.xlsx в коде).

=========================================================
Находясь в ide копируем нужный path папки и переключаемся на нужную папку командой cd в PowerShell.
Безконсольная сборка в файл .exe для task_meneger:
cd C:\PythonProjects\pythonProject\Graphical application - task_meneger

pyinstaller --noconsole --onefile --name task_meneger --add-data "C:\PythonProjects\pythonProject\Graphical application - task_meneger\tasks_and_responsibles.xlsx;." "C:\PythonProjects\pythonProject\Graphical application - task_meneger\task_meneger.py"

Пояснение:
1.	--noconsole: Отключает консольное окно при запуске.
2.	--onefile: Создает единый .exe файл для каждого скрипта.
3.	--name: Устанавливает имя выходного .exe файла (например, test_data.exe и task_meneger.exe).
4.	--add-data: Добавляет файл tasks_and_responsibles.xlsx в сборку.

•	Исполняемый файл task_meneger.exe появятся в папке dist.
•	Убедитесь, что путь к файлу tasks_and_responsibles.xlsx в коде обоих скриптов указан как относительный (tasks_and_responsibles.xlsx) или что путь корректно настраивается при работе с PyInstaller.
Пример запуска из PowerShell:
Запустите task_meneger.exe для работы приложения:
.\dist\task_meneger.exe

=========================================================

Функции open_email_client, create_email_file, open_telegram, open_whatsapp, которые осуществляют связь с разработчиками
при нажатии на соответствующую кнопку в разделе "Связь с разработчиками" не определены:

# Функции, которые вызываются при нажатии кнопок
def open_email_client():
    print("Открывается почтовый клиент")  # Здесь можно добавить код для открытия почтовой программы

def create_email_file():
    print("Создается почтовый файл")  # Здесь можно добавить код для создания почтового файла

def open_telegram():
    webbrowser.open("https://web.telegram.org/")  # Открывает веб-версию Telegram

def open_whatsapp():
    webbrowser.open("https://web.whatsapp.com/")  # Открывает веб-версию WhatsApp

