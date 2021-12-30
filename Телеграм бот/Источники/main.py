import telebot
from telebot import types
import functions, config

bot = telebot.TeleBot(config.token, parse_mode='MARKDOWN')


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = config.buttons['start_menu']
    keyboard.add(*buttons)
    bot.send_message(message.chat.id, 'Здравствуйте. Я подскажу расписание.\n'
                                      'Чтобы узнать всё что я умею напиши /help', reply_markup=keyboard)


@bot.message_handler(commands=['mtuci'])
def handle_mtuci(message):
    bot.send_message(message.chat.id, 'Сайт МТУСИ - https://mtuci.ru/')

@bot.message_handler(commands=['week'])
def handle_mtuci(message):
    if (functions.odd_date_check()) % 2 != 0:
        bot.send_message(message.chat.id, 'Сейчас идёт чётная (нижняя) неделя')
    else:
        bot.send_message(message.chat.id, 'Сейчас идёт нечётная (верхняя) неделя')

@bot.message_handler(commands=['help'])
def handle_start_help(message):
    bot.send_message(message.chat.id, 'Что я умею:\n'
                                      '/help - вывод списка доступных комманд\n'
                                      '/start - начать работу со мной\n'
                                      '/mtuci - получить ссылку на официальный сайт МТУСИ\n'
                                      '/week - узнать чётность недели \n'
                                      'Ну и конечно же, я могу подсказать с расписанием')


@bot.message_handler(content_types='text')
def message_reply(message):
    dataset = {'day': None, 'odd': None}
    if message.text == "Сегодня":
        bot.send_message(message.chat.id, functions.get_rasp(*functions.now_data()))
    elif message.text == "Завтра":
        bot.send_message(message.chat.id, functions.get_rasp(*functions.now_data(1)))
    elif message.text == "Полное расписание":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = config.buttons['odd_menu']
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, 'Выберите неделю', reply_markup=keyboard)
        m = bot.register_next_step_handler(message, lambda m: select_day(m, dataset))


def select_day(message, dataset):
    result = functions.odd_date_check()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = config.buttons['start_menu']
    keyboard.add(*buttons)
    if message.text == "Расписание на текущую неделю":
        for i in range(0, 5):
            bot.send_message(message.chat.id, functions.get_rasp(result, i), reply_markup=keyboard)
    elif message.text == "Расписание на следующую неделю":
        for i in range(0, 5):
            bot.send_message(message.chat.id, functions.get_rasp(not result, i), reply_markup=keyboard)


if __name__ == "__main__":
    bot.infinity_polling()