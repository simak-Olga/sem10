import telebot
from telebot import types
import json

API_TOKEN='.....'
bot = telebot.TeleBot(API_TOKEN)

print('bot is start')

def save():
    with open("book.json","w",encoding="utf-8") as fh:
        fh.write(json.dumps(phone_book,ensure_ascii=False))
    print("Файл book.json обновлен.")

def load():
    global phone_book
    with open("book.json","r",encoding="utf-8") as fh:
        phone_book=json.load(fh)
    print("Телефонная книга успешно загружена")

def search_contact(phone_num: int):
    global phone_book
    with open("book.json","r",encoding="utf-8") as fh:
        for key,value in phone_book.items():
            for k in value:
                if k==phone_num:
                    return key


@bot.message_handler(commands=['start'])
def startMessage(message):
    load()
    key = {}
    keyboard_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    key[0] = types.KeyboardButton("Посмотреть все контакты")
    key[1] = types.KeyboardButton("Найти контакт")
    key[2] = types.KeyboardButton("Добавить контакт")
    key[3] = types.KeyboardButton("Удалить контакт")
    keyboard_1.row(key[0], key[1])
    keyboard_1.row(key[2], key[3])

    name = message.from_user.first_name
    bot.send_message(message.chat.id,f"Привет, {name}! Я Teлефонный бот, у меня сохранены все твои контакты. Чем тебе помочь?", parse_mode='html', reply_markup=keyboard_1)

@bot.message_handler(func=lambda message: True)
def menu(message):
    if message.chat.type == 'private':
        if message.text == "Посмотреть все контакты":
            bot.send_message(chat_id=message.chat.id, text="Вот все твои сохранённые контакты:")
            bot.send_message(message.chat.id, f'{phone_book}')
        elif message.text == "Найти контакт":
            markup_1 = types.InlineKeyboardMarkup(row_width=1)
            but1 = types.InlineKeyboardButton("Найти по фамилии", callback_data='text1')
            but2 = types.InlineKeyboardButton("Найти по номеру телефона", callback_data='text2')
            markup_1.add(but1,but2)
            bot.send_message(chat_id=message.chat.id, text="Выбери, каким способом искать:", reply_markup=markup_1)
        elif message.text == "Добавить контакт":
            markup_2 = types.InlineKeyboardMarkup(row_width=1)
            but1 = types.InlineKeyboardButton("Добавить данные", callback_data='new')
            markup_2.add(but1)
            bot.send_message(chat_id=message.chat.id, text="Введите данные нового контакта:", reply_markup=markup_2)
        elif message.text == "Удалить контакт":
            markup_3 = types.InlineKeyboardMarkup(row_width=1)
            but1 = types.InlineKeyboardButton("Удалить все данные контакта", callback_data='del')
            but2 = types.InlineKeyboardButton("Удалить номер телефона контакта", callback_data='del_num')
            markup_3.add(but1,but2)
            bot.send_message(chat_id=message.chat.id, text="Выберите какие данные нужно удалить:", reply_markup=markup_3)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
            if call.data == 'text1':
                msg = bot.send_message(call.message.chat.id, "Введите фамилию:")
                bot.register_next_step_handler(msg, show_name)
            elif call.data == 'text2':
                msg = bot.send_message(call.message.chat.id, "Введите номер телефона:")
                bot.register_next_step_handler(msg, show_number)
            elif call.data == 'new':
                msg = bot.send_message(call.message.chat.id, "Укажите фамилию и номера телефонов через пробел!")
                bot.register_next_step_handler(msg, add_new_contact)
            elif call.data == 'del':
                msg = bot.send_message(call.message.chat.id, "Укажите фамилию контакта:")
                bot.register_next_step_handler(msg, del_contact)
            elif call.data == 'del_num':
                msg = bot.send_message(call.message.chat.id, "Укажите номер контакта:")
                bot.register_next_step_handler(msg, del_num_contact)

def show_name(message):
    global phone_book
    quest = message.text
    bot.send_message(message.chat.id, f'{quest}: {phone_book.get(quest)}')
    if phone_book.get(quest)==None:
        bot.send_message(message.chat.id, 'Такого контакта нет в телефонном справочнике!')

def show_number(message):
    quest = int(message.text)
    key = search_contact(quest)
    bot.send_message(message.chat.id, f'{key}: {quest}')
    if key==None:
        bot.send_message(message.chat.id, 'Такого номера нет в телефонном справочнике!')

def add_new_contact(message):
    global phone_book
    quest = message.text.split()
    if quest == [] or len(quest) < 2:
        bot.send_message(message.chat.id, 'Информация введена не полностью. Попробуйте еще раз!')
    else:
        if len(quest) > 2:
            phone_book[quest[0]] = []
            for i in range(len(quest)):
                if i>0:
                    phone_book[quest[0]].append(int(quest[i]))
            save()
            bot.send_message(message.chat.id, 'Контакт добавлен в телефонную книгу!')

def del_contact(message):
    global phone_book
    quest = message.text
    del phone_book[quest]
    save()
    bot.send_message(message.chat.id, 'Запись удалена!')

def del_num_contact(message):
    global phone_book
    quest = int(message.text)
    for key, value in phone_book.items():
        for k in value:
            if k==quest:
                phone_book[key].remove(k)
    save()
    bot.send_message(message.chat.id, 'Номер телефона удалён!')
    
    
bot.polling()