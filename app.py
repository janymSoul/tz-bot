import telebot
from telebot import types
import datetime
from yookassa import Configuration, Payment
import config

# Объявляю бот через токен полученной от Бот Фазер. Кстати все токены хранятся в другом файле config.py
bot = telebot.TeleBot(config.BOT_TOKEN)

# Хэндлер команды старт
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # создаю маркап и добавляю кнопки, и отправляю на юзера
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('Кнопка 1')
    btn2 = types.KeyboardButton('Кнопка 2')
    btn3 = types.KeyboardButton('Кнопка 3')
    btn4 = types.KeyboardButton('Кнопка 4')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Выберите опцию:", reply_markup=markup)

# Хэндлер первой кнопки. Просто отправляю ссылку на Гете 1, в городе Астана
@bot.message_handler(func=lambda message: message.text == 'Кнопка 1')
def button1(message):
    bot.send_message(message.chat.id, "Вот ссылка на Яндекс карты: https://yandex.ru/maps/org/astana_1/231832282075/?ll=71.410073%2C51.195920&z=15.75")
# Хэндлер второй кнопки.
@bot.message_handler(func=lambda message: message.text == 'Кнопка 2')
def start_payment(message):
    chat_id = message.chat.id

    #добавляю идентификатор тест магазина и секретный ключ от Юкассы для авторизации во время платежа
    Configuration.account_id = config.YOOKASSA_SHOP_ID
    Configuration.secret_key = config.YOOKASSA_SECRET_KEY

    """
    Создаю платеж, правда не указал ссылку полсе завершение процесса, думаю не нужно.
    Возвращает JSON в котором хранится ссылка для оплаты
    """
    payment = Payment.create({
        "amount": {
            "value": "2.00",
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.example.com/return_url"
        },
        "capture": True,
        "description": "Заказ №37",
        "metadata": {
        "order_id": "37"
        }
    })
    try:
        # условие если оплата еще не завершена то отправляем юзеру ссылку на оплату который хранится в payment[confirmation][confirmation_url]
        if payment.status == 'pending':
            payment_url = payment.confirmation.confirmation_url
            bot.send_message(chat_id, f"Пожалуйста, оплатите по ссылке: {payment_url}   (5555 5555 5555 4477 для теста)")
        else:
            #если оплата не прошла, то сообщаем юзеру об этом. Принтил объект для тестирования
            print(payment.json())
            bot.send_message(chat_id, "Оплата не завершена. Пожалуйста, повторите позже")
    except Exception as e:
        bot.send_message(chat_id, f"Error: {str(e)}")

# Хэндлер третий кнопки, встречайте легенду
@bot.message_handler(func=lambda message: message.text == 'Кнопка 3')
def button3(message):
    with open('img1.jpg', 'rb') as img:
        bot.send_photo(message.chat.id, img, caption="Встречайте лучшего всех времен!!!!")

# Хэндлер последней кнопки
@bot.message_handler(func=lambda message: message.text == 'Кнопка 4')
def button4(message):
    #читаю ячейку по адресу А2
    cell_value = config.SHEET.acell('A2').value
    #добавляю содержимое ячейки на сообщение
    bot.send_message(message.chat.id, f"Значение A2: {cell_value}")

# Хэндлит все остальное
@bot.message_handler(content_types=['text'])
def handle_date(message):
    input_date = message.text
    try:
        # Проверяю формат даты на соответствие дд.мм.гггг
        date_format = "%d.%m.%Y"
        datetime.datetime.strptime(input_date, date_format)
        # Обращаемся к гугл табличке и добавляем строчку даты
        config.SHEET.append_row([input_date], table_range="B:B")
        bot.send_message(message.chat.id, "Дата верна")
    except ValueError:
        # сообщаем что неверная дата и ждем еще команды
        bot.send_message(message.chat.id, "Дата введена неверно")



# Ждем запросов
bot.polling()
