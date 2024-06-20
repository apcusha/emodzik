"""
Модуль:
1. загружает данные об эмодзи и их тегах из листа 'теги' из файла 'тейки.xlsx' (см load_emoji_database_from_file)
2. поиск эмодзи по совпадениям с тегами (см find_emoji_by_keyword)
"""

import pyexcel_xlsx


def find_emoji_by_keyword(query_keyword: str, emoji_database: dict):
    """
    Поиск эмодзи в базе данных по совпадениям с тегами.
    Возвращает список подходящих эмодзи.
    Если не найдено, то возвращает пустой список
    """

    # Список подходящих эмодзи
    emoji_result_list = []

    # Переводим строку в нижний регистр
    query_keyword = query_keyword.lower()

    # Проходим в цикле по словарю (базе данных) эмодзи-теги
    for emoji, tags in emoji_database.items():
        # Добавляем в список подходящие эмодзи
        if is_keyword_in_tags(query_keyword, tags):
            emoji_result_list.append(emoji)

    return emoji_result_list


def is_keyword_in_tags(query_keyword: str, tags: list):
    """Проверяет содержится ли поисковое слово в наборе тегов"""

    for tag in tags:
        # Если в списке тегов есть совпадения с поисковым словом, то возвращаем True
        if query_keyword in tag.lower():
            return True

    return False


def load_emoji_database_from_file(file_name: str, sheet_name: str = "теги"):
    """Загружает данные из нужной страницы файла и возвращает их как словарь эмодзи-теги"""
    sheet = pyexcel_xlsx.get_data(file_name)[sheet_name]
    emoji_database = {row[0]: row[1].split(",") for row in sheet}
    return emoji_database


# Для запуска скрипта напрямую
if __name__ == "__main__":
    emoji_db = load_emoji_database_from_file(
        file_name="database/тейки.xlsx", sheet_name="теги"
    )
    query_word = input("Поиск эмодзи по слову: ")
    emoji_result = find_emoji_by_keyword(query_word, emoji_db)
    print(f"Найдено эмодзи: {emoji_result.__len__()}")
    for emoji in emoji_result:
        print(emoji)
