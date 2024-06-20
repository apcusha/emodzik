import os

from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    CallbackContext,
    ConversationHandler,
)

import emoji_search_engine
import random_emoji_generator

XLSX_FILE = "database/тейки.xlsx"
TAGS_SHEET_NAME = "теги"
CONSTRUCTOR_SHEET_NAME = "конструктор"

GREETING_TEXT = (
    "Привет! Я бот, который поможет тебе создать идеальный смайлик по твоему запросу. Просто опиши, "
    "какой смайлик ты хочешь видеть, и я с удовольствием сгенерирую его для тебя! (ﾉ>ω<)ﾉ :｡･:*:･ﾟ’★"
    "\n\nВсё, что нужно, — это немного воображения и пару слов, чтобы описать желаемый смайлик. Давайте "
    "начнем! ᕕ( ᐛ )ᕗ"
)
GREETING_SHORT_TEXT = (
    "Давай попробуем еще раз! Какой смайлик ты бы хотел получить?٩(◕‿◕)۶"
)
SEARCH_EMOJI_TEXT = "Отлично! Введи слово и я его засмайлю ԅ(≖‿≖ԅ)"
EMOJI_NOT_FOUND_TEXT = "Ой… пока такого слова или смайлика нет в моей базе данных.\nПопробуй ввести другое слово или придумай новый запрос! (*_ _)人"

# Загружаем переменные окружения с секретными данными из файла .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Загружаем данные из таблицы 'теги' из файла 'тейки.xlsx'
emoji_database = emoji_search_engine.load_emoji_database_from_file(
    file_name=XLSX_FILE, sheet_name=TAGS_SHEET_NAME
)
# Загружаем данные из таблицы 'конструктор' из файла 'тейки.xlsx'
emoji_parts = random_emoji_generator.load_emoji_parts_from_file(
    file_name=XLSX_FILE, sheet_name=CONSTRUCTOR_SHEET_NAME
)

# Константы и переменные для перехода между состояниями бота
MAIN_MENU, RANDOM_EMOJI, SEARCH_EMOJI, SEARCH_RESULT = range(4)
current_search_results = []
current_search_index = 0


async def start(
    update: Update, context: CallbackContext, short_greeting: bool = False
) -> int:
    """
    Точка входа в бота.
    Отображает преветствие (короткое или полное), клавиатуру и переводит приложение в состояние MAIN_MENU.
    """
    if short_greeting:
        greeting_text = GREETING_SHORT_TEXT
    else:
        greeting_text = GREETING_TEXT
    main_menu_keyboard = [
        [KeyboardButton("Случайный смайлик"), KeyboardButton("Создать по запросу")]
    ]
    reply_markup = ReplyKeyboardMarkup(main_menu_keyboard, resize_keyboard=True)
    await update.message.reply_text(greeting_text, reply_markup=reply_markup)
    return MAIN_MENU


async def random_emoji(update: Update, context: CallbackContext) -> int:
    """
    Обработчик кнопки "Случайный смайлик".
    Получает Случайный смайлик из модуля random_emoji_generator, отображает его, клавиатуру другой-Назад и переводит приложение в состояние RANDOM_EMOJI
    """

    emoji = random_emoji_generator.generate_random_emoji(emoji_parts)
    random_emoji_keyboard = [[KeyboardButton("Другой"), KeyboardButton("Назад")]]
    reply_markup = ReplyKeyboardMarkup(random_emoji_keyboard, resize_keyboard=True)
    await update.message.reply_text(f"{emoji}", reply_markup=reply_markup)
    return RANDOM_EMOJI


async def handle_random_emoji_buttons(update: Update, context: CallbackContext) -> int:
    """
    Обработчик кнопок "Другой" и "Назад" в состоянии RANDOM_EMOJI.
    Переключает в обработчик random_emoji или в обработчик start.
    """

    if update.message.text == "Другой":
        return await random_emoji(update, context)
    elif update.message.text == "Назад":
        return await start(update, context, short_greeting=True)
    else:
        # Передан некорректный текст кнопки
        return MAIN_MENU


async def search_emoji(update: Update, context: CallbackContext) -> int:
    """
    Обработчик кнопки "Создать по запросу".
    Запрашивает слово для поиска, отображает клавиатуру "Назад" и переводит приложение в состояние SEARCH_EMOJI
    """

    back_keyboard = [[KeyboardButton("Назад")]]
    reply_markup = ReplyKeyboardMarkup(back_keyboard, resize_keyboard=True)
    await update.message.reply_text(
        SEARCH_EMOJI_TEXT,
        reply_markup=reply_markup,
    )
    return SEARCH_EMOJI


async def handle_search_query(update: Update, context: CallbackContext) -> int:
    """
    Обработчик текста в состоянии SEARCH_EMOJI.
    Поиск эмодзи по ключевому слову и вызов обработчика show_search_result в случае успеха.
    Если поиск не дал результатов, отображается соответствующее сообщение
    Если нажата кнопка "Назад", возвращается в обработчик start.
    """

    global current_search_results, current_search_index
    query_word = update.message.text
    if query_word == "Назад":
        return await start(update, context, short_greeting=True)

    current_search_results = emoji_search_engine.find_emoji_by_keyword(
        query_word, emoji_database
    )
    current_search_index = 0

    if not current_search_results:
        await update.message.reply_text(EMOJI_NOT_FOUND_TEXT)
        return SEARCH_EMOJI

    return await show_search_result(update, context)


async def show_search_result(update: Update, context: CallbackContext) -> int:
    """
    Обработчик отображения текущего эмодзи в состоянии SEARCH_RESULT
    Отображает эмодзи из списка current_search_results по индексу current_search_index
    Отображает клавиатуру "Далее" и "Назад в меню"
    """

    global current_search_results, current_search_index
    emoji = current_search_results[current_search_index]
    search_emoji_keyboard = [[KeyboardButton("Далее"), KeyboardButton("Назад в меню")]]
    reply_markup = ReplyKeyboardMarkup(search_emoji_keyboard, resize_keyboard=True)
    await update.message.reply_text(f"{emoji}", reply_markup=reply_markup)
    return SEARCH_RESULT


async def handle_search_result_buttons(update: Update, context: CallbackContext) -> int:
    """
    Обработчик кнопок "Далее" и "Назад в меню" в состоянии SEARCH_RESULT
    Переключает в обработчик show_search_result или в обработчик start
    """

    global current_search_results, current_search_index
    if update.message.text == "Далее":
        # Изменение индекса отображаемого эмодзи. Если эмодзи закончились, переход снова к первому
        current_search_index = (current_search_index + 1) % len(current_search_results)
        return await show_search_result(update, context)
    elif update.message.text == "Назад в меню":
        return await start(update, context, short_greeting=True)
    else:
        # Передан некорректный текст кнопки
        return SEARCH_RESULT


def main() -> None:
    """Основная функция бота"""

    # Инициализация экземпляра приложения
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Инициализация обработчиков последовательного разговора
    # Точка входа (entry_points) может быть /start или любое сообщение (для непредвиденного зависания отображаемой клавиатуры)
    # Для каждого состояния сопоставляется ожидаемое сообщение (через регулярные выражения) и функции обработчика для него
    # Так же определяется fallbacks на случай если пользователь в данный момент ведет диалог, но состояние не имеет связанного обработчика
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.TEXT, start),
        ],
        states={
            MAIN_MENU: [
                MessageHandler(filters.Regex("^(Случайный смайлик)$"), random_emoji),
                MessageHandler(filters.Regex("^(Создать по запросу)$"), search_emoji),
            ],
            RANDOM_EMOJI: [
                MessageHandler(
                    filters.Regex("^(Другой|Назад)$"), handle_random_emoji_buttons
                )
            ],
            SEARCH_EMOJI: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_search_query)
            ],
            SEARCH_RESULT: [
                MessageHandler(
                    filters.Regex("^(Далее|Назад в меню)$"),
                    handle_search_result_buttons,
                )
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Добавляем обработчик последовательного разговора в приложение
    application.add_handler(conv_handler)

    # Запускаем приложение
    application.run_polling()


# Для запуска скрипта напрямую
if __name__ == "__main__":
    main()
