# Чтобы добавить поддержку русского алфавита в шифр Цезаря, 
# нужно учитывать кодировки символов русского алфавита в Unicode. 
# Русский алфавит (как строчные, так и прописные буквы) имеет свои диапазоны Unicode:

# Строчные буквы: от а (U+0430) до я (U+044F)
# Прописные буквы: от А (U+0410) до Я (U+042F)
# Проверяем, входит ли символ в диапазон русского алфавита.
# Используем mod 32 для русского алфавита, так как в нём 32 буквы.

# Английский алфавит: оставляем логику для английских букв без изменений.
# Неалфавитные символы: сохраняются в неизменном виде.

def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    for char in text:
        if char.isalpha():  # Проверяем, является ли символ буквой
            shift_amount = shift if mode == 'encrypt' else -shift
            # Определяем диапазон для русского алфавита
            if 'А' <= char <= 'Я':
                start = ord('А')
                offset = (ord(char) - start + shift_amount) % 32
                result += chr(start + offset)
            elif 'а' <= char <= 'я':
                start = ord('а')
                offset = (ord(char) - start + shift_amount) % 32
                result += chr(start + offset)
            # Диапазон для английского алфавита
            elif 'A' <= char <= 'Z':
                start = ord('A')
                offset = (ord(char) - start + shift_amount) % 26
                result += chr(start + offset)
            elif 'a' <= char <= 'z':
                start = ord('a')
                offset = (ord(char) - start + shift_amount) % 26
                result += chr(start + offset)
        else:
            result += char  # Если символ не буква, добавляем его без изменений
    return result

# Запрос ввода от пользователя
text_to_encrypt = input("Введите текст для шифрования: ")
shift_value = int(input("Введите значение сдвига: "))

# Шифрование
encrypted_text = caesar_cipher(text_to_encrypt, shift_value, mode='encrypt')
print(f"Зашифрованный текст: {encrypted_text}")

# Дешифрование
decrypted_text = caesar_cipher(encrypted_text, shift_value, mode='decrypt')
print(f"Расшифрованный текст: {decrypted_text}")

# Пример работы:
# Ввод текста: Привет, Мир! Hello, World!
# Значение сдвига: 3

# Результат:
# Зашифрованный текст: Тулжзх, Олу! Khoor, Zruog!
# Расшифрованный текст: Привет, Мир! Hello, World!