def draw_cat():
    print("""
 /\_/\  
( o.o ) 
 > ^ <
    """)

def draw_dog():
    print("""
 / \__
(     @\____
 /         O
 /   (______/
/_____/   U
    """)

def draw_bear():
    print("""
ʕ•ᴥ•ʔ
    """)

def draw_rabbit():
    print("""
 (\(\ 
 ( -.-)
 o_(")(")
    """)

def draw_owl():
    print("""
  ^__^
 (o,o)
 (  , )
  """""" 
    """)

def main():
    print("Привет! Я могу нарисовать для тебя разных забавных зверят.")
    print("Выбирай, кого ты хочешь увидеть:")
    print("1 - Котик")
    print("2 - Собачка")
    print("3 - Мишка")
    print("4 - Кролик")
    print("5 - Совушка")

    while True:
        choice = input("Введи номер зверя или 'q' для выхода: ")
        
        if choice == '1':
            draw_cat()
        elif choice == '2':
            draw_dog()
        elif choice == '3':
            draw_bear()
        elif choice == '4':
            draw_rabbit()
        elif choice == '5':
            draw_owl()
        elif choice.lower() == 'q':
            print("Пока! Надеюсь, тебе понравились зверята!")
            break
        else:
            print("Ой, такого зверька нет. Попробуй снова!")

# Запускаем программу
main()
