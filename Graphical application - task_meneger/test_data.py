import pandas as pd
from datetime import datetime, timedelta
import random

def generate_random_tasks_and_responsibles(num_tasks=100, num_responsibles=50):
    # Списки для генерации ФИО
    male_names = ['Иван', 'Алексей', 'Петр', 'Андрей', 'Дмитрий', 'Сергей', 'Михаил', 'Николай', 'Владимир']
    female_names = ['Мария', 'Ольга', 'Анна', 'Елена', 'Наталья', 'Татьяна', 'Светлана', 'Екатерина']
    male_surnames = ['Иванов', 'Петров', 'Сидоров', 'Кузнецов', 'Смирнов', 'Попов', 'Васильев', 'Соколов']
    female_surnames = ['Иванова', 'Петрова', 'Сидорова', 'Кузнецова', 'Смирнова', 'Попова', 'Васильева']
    male_patronymics = ['Иванович', 'Алексеевич', 'Петрович', 'Андреевич', 'Дмитриевич', 'Сергеевич']
    female_patronymics = ['Ивановна', 'Алексеевна', 'Петровна', 'Андреевна', 'Дмитриевна', 'Сергеевна']
    positions = ['Программист', 'Менеджер', 'Дизайнер', 'Тестировщик', 'Аналитик', 'Руководитель проекта',
                'Системный администратор', 'Бизнес-аналитик', 'Технический писатель']

    # Генерация списка ответственных
    responsibles = []
    for _ in range(num_responsibles):
        if random.random() < 0.5:  # 50% шанс мужского или женского пола
            name = random.choice(male_names)
            surname = random.choice(male_surnames)
            patronymic = random.choice(male_patronymics)
        else:
            name = random.choice(female_names)
            surname = random.choice(female_surnames)
            patronymic = random.choice(female_patronymics)
        
        position = random.choice(positions)
        full_name = f"{surname} {name[0]}.{patronymic[0]}."
        responsibles.append((full_name, position))

    # Генерация задач
    tasks = []
    current_date = datetime.now()
    
    for i in range(num_tasks):
        task_id = f"TASK-{i+1:04d}"
        responsible, position = random.choice(responsibles)
        
        # Генерация случайных дат
        created_date = current_date - timedelta(days=random.randint(0, 30))
        start_date = created_date + timedelta(days=random.randint(1, 10))
        end_date = start_date + timedelta(days=random.randint(5, 30))
        
        task = {
            "ID задачи": task_id,
            "Задача": f"Тестовая задача {i+1}",
            "Ответственный": responsible,
            "Должность": position,
            "Дата создания": created_date.strftime("%Y-%m-%d %H:%M"),
            "Дата начала": start_date.strftime("%Y-%m-%d %H:%M"),
            "Дата окончания": end_date.strftime("%Y-%m-%d %H:%M"),
            "Последнее изменение": created_date.strftime("%Y-%m-%d %H:%M"),
            "Срочно": random.choice(["Да", "Нет"]),
            "Выполнено": random.choice(["Да", "Нет"])
        }
        tasks.append(task)

    # Создание DataFrame
    tasks_df = pd.DataFrame(tasks)
    responsibles_df = pd.DataFrame(responsibles, columns=["ФИО", "Должность"])

    # Сохранение в Excel
    with pd.ExcelWriter("tasks_and_responsibles.xlsx") as writer:
        tasks_df.to_excel(writer, sheet_name="Задачи", index=False)
        responsibles_df.to_excel(writer, sheet_name="Ответственные", index=False)

    return tasks_df, responsibles_df

# Генерация данных
tasks, responsibles = generate_random_tasks_and_responsibles(num_tasks=100, num_responsibles=50)
print("Тестовые данные успешно сгенерированы и сохранены в файл tasks_and_responsibles.xlsx")
print("Прочти readme.txt")