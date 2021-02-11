from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

btn_goback = KeyboardButton('Вернуться назад')

btn_ask = KeyboardButton('Задать вопрос')
btn_request_q = KeyboardButton('Запросить вопрос')
btn_my_q = KeyboardButton('Мои вопросы')

btn_next = KeyboardButton('Следующий вопрос')
btn_text = KeyboardButton('Some text')
btn_continue = KeyboardButton('Продолжить')

btn_add_q = KeyboardButton('Добавить вопрос')
btn_delete_q = KeyboardButton('Удалить вопрос')

btn_send_phone = KeyboardButton('Send my contacts', request_contact=True)
btn_send_geo = KeyboardButton('Send my geolocation', request_location=True)

markupMain = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_ask).add(btn_request_q).add(btn_my_q)
markup2 = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_send_geo, btn_send_phone)
markupManageQ = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_add_q).add(btn_delete_q).add(btn_goback)
markupGameInProcess = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_continue).add(btn_goback)
