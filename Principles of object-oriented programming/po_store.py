# Программное обеспечение для сети магазинов: Каждый магазин в этой сети имеет свои особенности,
# но также существуют общие характеристики, такие как адрес, название и ассортимент товаров.
# Задача — создать класс Store, который можно будет использовать для создания различных магазинов.

# 1. Класс Store
class Store:
    def __init__(self, name, address):
        """Инициализация магазина с названием и адресом."""
        self.name = name
        self.address = address
        self.items = {}

    def add_item(self, item_name, price):
        """Добавление товара в ассортимент магазина."""
        self.items[item_name] = price

    def remove_item(self, item_name):
        """Удаление товара из ассортимента магазина."""
        if item_name in self.items:
            del self.items[item_name]
        else:
            print(f"Товар {item_name} не найден в ассортименте.")

    def get_price(self, item_name):
        """Получить цену товара по его названию."""
        return self.items.get(item_name, None)

    def update_price(self, item_name, new_price):
        """Обновить цену товара."""
        if item_name in self.items:
            self.items[item_name] = new_price
        else:
            print(f"Товар {item_name} не найден в ассортименте.")

# 2. Создание объектов класса Store
# Теперь создадим несколько магазинов с разными данными и добавим товары в их ассортимент.

# Создание нескольких магазинов
store1 = Store("SuperMart", "123 Main St")
store2 = Store("GroceryHub", "456 Oak Ave")
store3 = Store("FoodMarket", "789 Pine Rd")

# Добавление товаров в ассортимент магазинов
store1.add_item("apples", 0.5)
store1.add_item("bananas", 0.75)
store2.add_item("oranges", 0.8)
store2.add_item("grapes", 1.2)
store3.add_item("watermelon", 3.0)
store3.add_item("pineapple", 2.5)

# 3. Протестировать методы
# Теперь протестируем методы:
# - добавления товара;
# - обновления цены;
# - удаления товара;
# - получения цены в одном из магазинов.

# Пример использования магазина store1

print(f"Ассортимент магазина {store1.name} ({store1.address}):")
print(store1.items)  # Показываем ассортимент на данный момент

# Добавляем новый товар
store1.add_item("pears", 1.0)
print("\nПосле добавления товара 'pears':")
print(store1.items)

# Обновляем цену товара
store1.update_price("apples", 0.55)
print("\nПосле обновления цены товара 'apples':")
print(store1.items)

# Удаляем товар
store1.remove_item("bananas")
print("\nПосле удаления товара 'bananas':")
print(store1.items)

# Получаем цену товара
price = store1.get_price("apples")
print(f"\nЦена товара 'apples': {price}")

# Пытаемся получить цену товара, которого нет
price = store1.get_price("bananas")
print(f"Цена товара 'bananas': {price}")

# 4. Результат выполнения программы
# В результате выполнения программы, вы получите:
# Ассортимент магазина SuperMart (123 Main St):
# {'apples': 0.5, 'bananas': 0.75}

# После добавления товара 'pears':
# {'apples': 0.5, 'bananas': 0.75, 'pears': 1.0}

# После обновления цены товара 'apples':
# {'apples': 0.55, 'bananas': 0.75, 'pears': 1.0}

# После удаления товара 'bananas':
# {'apples': 0.55, 'pears': 1.0}

# Цена товара 'apples': 0.55
# Цена товара 'bananas': None

# Объяснение:

# add_item — добавляет новый товар в ассортимент магазина.
# update_price — обновляет цену товара, если он есть в ассортименте.
# remove_item — удаляет товар из ассортимента.
# get_price — возвращает цену товара по его названию, если товара нет, возвращает None.
# Таким образом, мы успешно создали класс Store, который можно использовать для создания различных магазинов
# с разными характеристиками.
# Мы протестировали все необходимые методы для добавления, удаления, обновления
# и получения цены товара.