# Телеграмм-бот для управления  записью на уроки и получения информации (Lesson_bot)

Этот бот предоставляет несколько полезных функций, таких как получение картинок с лисами, информации о погоде, управление записями на уроки и просмотр будущих записей.

Возможности бота
Основные команды
/start
Приветственное сообщение и меню с кнопками для взаимодействия с ботом.

/help
Список доступных команд и их описание.

/fox
Получение ссылки на картинку с лисой.

/погода
Получение информации о погоде в указанном городе (по умолчанию в Екатеринбурге).

/calendar
Запуск процесса записи на урок, включая выбор даты и времени.

Кнопки меню
Лиса
Получение картинки с лисой (аналогично команде /fox).

Погода
Получение информации о погоде (аналогично команде /погода).

Запись
Запуск процесса записи на урок (аналогично команде /calendar).

Мои уроки
Просмотр будущих записей на уроки.

Процесс записи на урок
Выбор даты:
При нажатии на кнопку "Запись" или команду /calendar, бот предложит выбрать дату из календаря.

Выбор времени:
После выбора даты, бот запросит ввести время в формате ЧЧ:ММ.

Подтверждение записи:
Бот предложит подтвердить запись с выбранной датой и временем. Можно подтвердить запись или вернуться к выбору даты.

Завершение записи:
После подтверждения записи, бот сохраняет информацию и сообщает о успешной записи.

Просмотр будущих записей
При использовании команды /my_lessons или нажатии на кнопку "Мои уроки", бот покажет все будущие записи на уроки для текущего пользователя.

Настройка и запуск
Установите зависимости:
Убедитесь, что у вас установлены библиотеки aiogram и другие необходимые зависимости.

bash
Копировать код
pip install aiogram
Настройте конфигурацию:
Создайте файл config.py и добавьте в него следующие переменные:

python
Копировать код
token_api = "ВАШ_API_ТОКЕН"
weather_api_key = "ВАШ_API_КЛЮЧ_ПОГОДЫ"
Запустите бота:
Запустите основной файл бота. Например:

bash
Копировать код
python bot.py
Примечания
Бот использует файловую систему для хранения записей о записях на уроки. Файл с записями называется appointments.json.
Для работы с ботом требуется настроить API токен и ключ погоды в конфигурационном файле.
