# Задача: Напишите свою собственную игру - камень ножницы бумага
# Игра должна идти до 3-х побед, и выводить кто победил

print("Игра - камень ножницы бумага")
import random

# Возможные варианты игры
options = ["камень", "ножницы", "бумага"]
user_score = 0
computer_score = 0

# Игра идет до 3 побед
while user_score < 3 and computer_score < 3:
    user_choice = input("Выберите: камень, ножницы или бумага: ").lower() # .lower() делает ввод независимым от регистра
    computer_choice = random.choice(options)  # random.choice(options) — функция из модуля random, которая выбирает и возвращает случайный элемент из указанной последовательности (списка, кортежа, строки). options — это список (или другая последовательность), из которого будет выбран случайный элемент.
    print("Компьютер выбрал:", computer_choice)

    if user_choice == computer_choice:
        print("Ничья!")
    elif (user_choice == "камень" and computer_choice == "ножницы") or \
         (user_choice == "ножницы" and computer_choice == "бумага") or \
         (user_choice == "бумага" and computer_choice == "камень"):
        print("Вы выиграли этот раунд!")
        user_score += 1
    elif user_choice in options: # Оператор in в выражении elif user_choice in options проверяет, содержится ли значение user_choice в списке options. Если user_choice есть в options, выражение вернёт True; если нет — False.
        print("Компьютер выиграл этот раунд!")
        computer_score += 1
    else:
        print("Неверный ввод. Попробуйте снова.")

    print(f"Счет: Вы {user_score} - {computer_score} Компьютер")

# Определение победителя
if user_score == 3:
    print("Поздравляем! Вы выиграли игру.")
else:
    print("Компьютер выиграл игру.")