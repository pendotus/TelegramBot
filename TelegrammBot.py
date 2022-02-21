import telebot #подлючение библиотеки
from telebot import types

bot = telebot.TeleBot('1577168190:AAESD5oTCl01Dv15TRTsBSA6wBSlkiXuA3w') #подключение токена

name = "incognito";    #данные пользователя

KeyboardStart = types.ReplyKeyboardMarkup(True) #клава старта
KeyboardStart.row('Меню','Адресс', 'Рассписание')
KeyboardStart.row('Забронировать стол')

KeyboardHelp = types.ReplyKeyboardMarkup(True)  #клава помощи
KeyboardHelp.row('/menu','/adress','/reg')
KeyboardHelp.row('/back')

@bot.message_handler(commands=['start'])  #стартуем! Я сказала стартуем!
def start(message):
    bot.send_message(message.from_user.id, 'Здраствуйте! Я чат-бот, работаю в молодежном антикафе "старика тут не место". Чем могу ыбыть полезен? ', reply_markup = KeyboardStart)


@bot.message_handler(commands=['help', 'info']) #хЕеЕеЕелллппп 0 помощи
def help(message):
    bot.send_message(message.from_user.id,"А вот и помощь! Список команд: /reg - забронировать стол, /menu - показать меню, /adress - показать адресс, /back - закрыть помощь", reply_markup = KeyboardHelp) #список команд

@bot.message_handler(commands=['close','back']) #возвращает начальную клавиутуру после вкладки с хелпой
def back(message):
    bot.send_message(message.from_user.id, 'Один момент!', reply_markup = KeyboardStart)

@bot.message_handler(commands=['share']) #спам функция (отправляет дркгому челу репост группы, типо есть, просто чтобы была)
def share(message):
    keyboard = types.InlineKeyboardMarkup() 
    switch_button = types.InlineKeyboardButton(text="Тык для распространения", switch_inline_query="Telegram")
    keyboard.add(switch_button)
    bot.send_message(message.chat.id, "Заспамь меня полностью", reply_markup=keyboard)

@bot.message_handler(commands=['reg']) #рег челика
def reg(message):
    bot.send_message(message.from_user.id, "Введите Ваше имя, дату брони, а так же ваш номер телефона") 
    bot.register_next_step_handler(message, get_you) #переходим на функциюю get_you

@bot.message_handler(command=['test'])
def get_you(message): #получаем данный от пользователя (продолжение def reg) (разбите нужно, чтобы команда  повторялась на сулчай варианта нет)
    global name
    name = message.text
    keyboard = types.InlineKeyboardMarkup() #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes') #кнопка «Да»
    keyboard.add(key_yes) #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no') #кнопка нет
    keyboard.add(key_no) #добавляем кнопку нет в клавиатуру
    question = 'Информация верна: '+name+'?' #текст в вопросе
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard) #хз зачем это, в интернете так написано
    @bot.callback_query_handler(func=lambda call: True) #реакция на кнопки
    def callback_worker(call):
        if call.data == "yes":   #да
            bot.send_message(call.message.chat.id, 'Понял, ожидайте звонка');
            f = open("clients.txt", 'a') # открывает файл с данными
            f.write(name) #записывает переменную
            f.close()  # закрывает файл
        elif call.data == "no": # нет
            bot.send_message(call.message.chat.id, 'Введите Ваше имя еще раз');
            bot.register_next_step_handler(message, get_you) #выполняет get_you еще раз


@bot.message_handler(content_types=['text']) #реакция бота на текст
def get_text_messages(message):
    if message.text  == "Меню" or message.text == "меню" : 
        bot.send_photo(message.chat.id, open('menu.jpg','rb')) 
    elif message.text == "Рассписание":
        bot.send_message(message.from_user.id, "каждый день с 10.00-2.00")
    elif message.text == "Адресс":
        bot.send_location(message.from_user.id, 59.938924, 30.315311)
    elif message.text =="Забронировать стол":
        bot.register_next_step_handler(message, reg)
    else:
        bot.send_message(message.from_user.id, "Не понимаю, введите комманду еще раз") #не вкуривыет че бубнеть то


bot.polling(none_stop=True)

