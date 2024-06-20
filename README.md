# emoji-search-engine
Создавайте и ищите эмодзи с помощью telegram-бота

### Требования
1. Тестировалось на версии python3.12, но вполне возможно запустится и на более старых версиях
2. В проекте используются внешние зависимости, подробнее в [requirements.txt](requirements.txt)

### Настройка окружения приложения
1. Открыть терминал в каталоге проекта.
2. Создать виртуальное окружение `python3 -m venv venv`
2. Активировать окружение
	1. Windows: <code>venv\Scripts\activate.bat</code>
	2. Linux/MacOS: `source venv/bin/activate`
3. Установить зависимости `pip install -r requirements.txt`

### Запуск приложения
1. Указать API-ключ бота в файле .env
2. Запустить телеграм-бота `python3 telegram_bot.py`

*Отдельно в терминале можно побаловаться запуская модули emoji_search_engine.py и random_emoji_generator.py*
