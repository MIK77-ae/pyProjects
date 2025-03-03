# Система управления учетными записями пользователей для небольшой компании:
# Компания разделяет сотрудников на обычных работников и администраторов.
# У каждого сотрудника есть уникальный идентификатор (ID), имя и уровень доступа.
# Администраторы, помимо обычных данных пользователей, имеют дополнительный уровень доступа
# и могут добавлять или удалять пользователя из системы.

class User:
    # Класс User предназначен для представления обычного пользователя.
    def __init__(self, user_id: int, name: str, access_level: str = 'user'):
        # Инициализация экземпляра с ID пользователя, именем и уровнем доступа (по умолчанию 'user').
        self._user_id = user_id
        self._name = name
        self._access_level = access_level

    def get_user_id(self) -> int:
        # Возвращает ID пользователя.
        return self._user_id

    def get_name(self) -> str:
        # Возвращает имя пользователя.
        return self._name

    def set_name(self, name: str):
        # Устанавливает новое имя для пользователя.
        self._name = name

    def get_access_level(self) -> str:
        # Возвращает уровень доступа пользователя.
        return self._access_level

    def __str__(self):
        # Возвращает строковое представление пользователя для удобного отображения.
        return f"User(ID: {self._user_id}, Name: {self._name}, Access Level: {self._access_level})"


class Admin(User):
    # Класс Admin наследуется от User и добавляет функциональность администратора.
    def __init__(self, user_id: int, name: str, admin_level: str):
        # Инициализация экземпляра администратора с дополнительным уровнем доступа.
        super().__init__(user_id, name, access_level='admin')
        self._admin_level = admin_level

    def get_admin_level(self) -> str:
        # Возвращает уровень доступа администратора.
        return self._admin_level

    def set_admin_level(self, admin_level: str):
        # Устанавливает новый уровень доступа для администратора.
        self._admin_level = admin_level

    def add_user(self, user_list: list, user: User):
        # Метод добавляет нового пользователя в список.
        user_list.append(user)
        print(f"Пользователь {user.get_name()} (ID: {user.get_user_id()}) добавлен.")

    def remove_user(self, user_list: list, user_id: int):
        # Метод удаляет пользователя из списка по его ID.
        for user in user_list:
            if user.get_user_id() == user_id:
                user_list.remove(user)
                print(f"Пользователь {user.get_name()} (ID: {user_id}) удален.")
                return
        # Если пользователь с указанным ID не найден, выводится сообщение об ошибке.
        print(f"Пользователь с ID {user_id} не найден.")

    def __str__(self):
        # Возвращает строковое представление администратора для удобного отображения.
        return f"Admin(ID: {self._user_id}, Name: {self._name}, Admin Level: {self._admin_level})"


# Пример использования
if __name__ == "__main__":
    # Список для хранения пользователей.
    users = []

    # Создание администратора.
    admin = Admin(user_id=1, name="Света", admin_level="Super")

    # Создание обычных пользователей.
    user1 = User(user_id=2, name="Вася")
    user2 = User(user_id=3, name="Петя")

    # Добавление пользователей в систему через администратора.
    admin.add_user(users, user1)  # Добавляет пользователя Вася.
    admin.add_user(users, user2)  # Добавляет пользователя Петя.

    # Вывод текущего списка пользователей.
    print("\nТекущий список пользователей:")
    for user in users:
        print(user)

    # Удаление пользователя из системы через администратора.
    admin.remove_user(users, user_id=2)  # Удаляет пользователя с ID 2 (Вася).

    # Вывод списка пользователей после удаления.
    print("\nСписок пользователей после удаления:")
    for user in users:
        print(user)

# Пояснения по работе программы:
# 1. Создаются экземпляры класса User для обычных сотрудников и Admin для администратора.
# 2. Экземпляры пользователей добавляются в общий список через методы администратора (add_user).
# 3. Пользователь может быть удален из списка с помощью метода remove_user.
# 4. Программа демонстрирует обработку данных с использованием инкапсуляции (закрытые (защищенные) атрибуты и методы доступа).
# 5. В случае ошибок (например, попытки удалить несуществующего пользователя) выводятся соответствующие сообщения.
