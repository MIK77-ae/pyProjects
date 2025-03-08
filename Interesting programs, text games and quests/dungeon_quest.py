import time

def introduction():
    print("Добро пожаловать в подземелье! Ты отважился войти в темные глубины, где могут произойти ужасные вещи.")
    time.sleep(1)
    print("Твоя задача - дойти до конца подземелья, преодолевая препятствия на своем пути.")
    time.sleep(1)
    print("Выбирай свои действия осторожно, и помни, что каждое решение влияет на твое приключение!\n")

def make_choice(question, options):
    print(question)
    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    while True:
        try:
            choice = int(input("Выбери номер действия: "))
            if 1 <= choice <= len(options):
                return choice
            else:
                print("Пожалуйста, введите число от 1 до", len(options))
        except ValueError:
            print("Пожалуйста, введите число.")

def dungeon_quest():
    introduction()
    inventory = []

    # Задание №1
    print("Задание 1: Ты стоишь перед развилкой. Куда идти?")
    choice_1 = make_choice("1. Пойти налево.", ["Продолжить влево", "Вернуться назад"])

    if choice_1 == 1:
        print("Ты идешь влево и видишь дверь.")
        choice_2 = make_choice("2. Открыть дверь или вернуться обратно?", ["Открыть дверь", "Вернуться назад"])

        if choice_2 == 1:
            print("Ты входишь в следующую комнату.")
            inventory.append("Ключ от следующей двери")
        else:
            print("Ты решаешь вернуться к развилке.")

    # Задание №2
    print("\nЗадание 2: Перед тобой мост через бездну. Что будешь делать?")
    choice_3 = make_choice("1. Перейти мост осторожно.", ["Перейти", "Вернуться обратно"])

    if choice_3 == 1:
        print("Ты успешно пересекаешь мост.")
    else:
        print("Ты решаешь вернуться к развилке.")

    # Задание №3
    print("\nЗадание 3: Ты видишь сундук. Открыть его?")
    choice_4 = make_choice("1. Открыть сундук.", ["Открыть сундук", "Пройти мимо"])

    if choice_4 == 1:
        print("Ты находишь меч!")
        inventory.append("Меч")

    # Задание №4
    print("\nЗадание 4: Ты стоишь перед последней дверью. Использовать ключ?")
    choice_5 = make_choice("1. Использовать ключ.", ["Использовать ключ", "Попробовать взломать дверь"])

    if choice_5 == 1 and "Ключ от следующей двери" in inventory:
        print("Ты открываешь дверь и выбираешься из подземелья. Поздравляю, ты победил!")
    else:
        print("Дверь не поддается. Тебе придется искать другой путь.")

if __name__ == "__main__":
    dungeon_quest()