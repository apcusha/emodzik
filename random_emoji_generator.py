"""
Модуль:
1. загружает данные из листа 'конструктор' из файла 'тейки.xlsx' (см load_emoji_parts_from_file)
2. генерирует случайный эмодзи из различных частей эмодзи (см generate_random_emoji)
"""

import random

import pyexcel_xlsx


# Список частей эмодзи, которые ВОЗМОЖНО будут пропускаться
PARTS_TO_SKIP = ["брови", "носы"]


def generate_random_emoji(emoji_parts: dict):
    """Генерирует случайный эмодзи из частей эмодзи"""
    result_emoji = ""

    # Проходим в цикле по словарю частей эмодзи
    for emoji_part_name, emoji_part_list in emoji_parts.items():
        # Случайно решаем пропускать определенные части эмодзи
        if not is_part_should_be_included(emoji_part_name):
            continue
        # получаем случайный символ, приводим его к строке, на случай если в таблице было число
        chosen_emoji_part = str(chose_random_char_for_part(emoji_part_list))
        # добавляем случайный символ в результирующую строку эмодзи
        result_emoji += chosen_emoji_part

    return result_emoji


def is_part_should_be_included(emoji_part_name: str):
    """Проверяет надо ли добавить часть эмодзи. Возвращает False если часть можно случайно пропустить, иначе True"""
    if emoji_part_name in PARTS_TO_SKIP:
        # Вероятность пропуска части эмодзи = 1/2.
        return random.choice([True, False])
    return True


def chose_random_char_for_part(part_list: list):
    """Выбирает случайный символ из списка возможных вариантов"""

    # Пробуем выбрать случайный элемент из набора
    # Если вдруг был передан пустой набор, то возвращаем пустую строку
    try:
        return random.choice(part_list)
    except IndexError:
        return ""


def load_emoji_parts_from_file(file_name: str, sheet_name: str):
    """Загружает данные из нужной страницы файла и возвращает их как словарь частей эмодзи"""

    # Загружаем данные, ограничиваясь 4 строками (иначе могут быть подгружены пустые строки)
    sheet = pyexcel_xlsx.get_data(file_name, row_limit=4)[sheet_name]
    # Составляем словарь, где ключ - название части эмодзи из первой колотки, а значение - список возможных вариантов из оставшихся колонок
    emoji_parts = {row[0]: row[1:] for row in sheet}

    return emoji_parts


# Для запуска скрипта напрямую
if __name__ == "__main__":
    test_emoji_parts = load_emoji_parts_from_file(
        file_name="database/тейки.xlsx", sheet_name="конструктор"
    )
    print(generate_random_emoji(test_emoji_parts))
