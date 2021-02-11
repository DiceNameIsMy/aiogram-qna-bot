import logging

import database_connection as db_conn

import keyboard_buttons as kb

from token_file import API_TOKEN

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

main_text = {
    'ask': 'Задать вопрос', 'req': 'Запросить вопрос', 
    'my_q': 'Мои вопросы', 'back': 'Вернуться назад', 
    'cont': 'Продолжить',
    }

manage_text = {'add': 'Добавить вопрос', 'del': 'Удалить вопрос'}

temporary = {}

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class StateMachine(Helper):
    mode = HelperMode.snake_case

    ANSWER_STATE = ListItem()     # answer the question
    ASKQ_STATE = ListItem()       # ask question
    MYQ_STATE = ListItem()        # my questions
    Q_ANSWERED_STATE = ListItem() # the moment when question was answered


# commands
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # state = dp.current_state(user=message.from_user.id)
    await message.answer("Привестствую. Я Капито и я создан для предоставления возможности " +
                         "задавать и отвечать на различные вопросы",
                         reply_markup=kb.markupMain)

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.answer("Для начала воспользуйтесь кнопками в нижней части экрана. " +
                         "Если кнопки не видны нажмите на скругленный квадрат с 4 квадратиками внутри",
                         reply_markup=kb.markupMain)


# возврат в меню
@dp.message_handler(lambda message: message.text == main_text['back'], state=StateMachine.all())
async def go_back(message: main_text['back']):
    state = dp.current_state(user=message.from_user.id)
    try:
        question_id = temporary.pop(message.from_user.id)
    except KeyError:
        print('no question were in memory')
    await state.reset_state()
    await message.answer("Вы вернулись в меню.", reply_markup=kb.markupMain)


# задать вопрос
@dp.message_handler(lambda message: message.text == main_text['ask'])
async def ask_question(message: main_text['ask']):
    state = dp.current_state(user=message.from_user.id)
    await message.answer("Напишите свой вопрос:", reply_markup=kb.ReplyKeyboardRemove())
    print(StateMachine.all()[1])
    await state.set_state(StateMachine.all()[1])


# запросить вопрос
@dp.message_handler(lambda message: message.text == main_text['req'])
async def req_question(message: main_text['req']):
    state = dp.current_state(user=message.from_user.id)
    question = db_conn.ask_question()
    temporary[message.from_user.id] = question[0]

    await message.answer('Вопрос: ' + question[1],
                         reply_markup=kb.ReplyKeyboardRemove())
    await state.set_state(StateMachine.all()[0])
    print(StateMachine.all()[0])



# ввести ответ
@dp.message_handler(state=StateMachine.all()[0])
async def input_answer(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    question_id = temporary.pop(message.from_user.id)

    db_conn.insert_answer(author_id=message.from_user.id, question_id=question_id, answer=message.text)

    await message.answer('Ваш ответ получен.',
                         reply_markup=kb.markupGameInProcess)
    await state.set_state(StateMachine.all()[3])
    # нужно подключить к бд


@dp.message_handler(lambda message: message.text == main_text['cont'], state=StateMachine.all()[3])
async def next_question(message: main_text['cont']):
    state = dp.current_state(user=message.from_user.id)
    question = db_conn.ask_question()
    temporary[message.from_user.id] = question[0]

    await message.answer('Вопрос: ' + question[1],
                         reply_markup=kb.ReplyKeyboardRemove())
    await state.set_state(StateMachine.all()[0])

# мои вопросы
@dp.message_handler(lambda message: message.text == main_text['my_q'])
async def my_questions(message: main_text['my_q']):
    state = dp.current_state(user=message.from_user.id)
    data = db_conn.return_questions(user_id=message.from_user.id)

    await message.answer(data, reply_markup=kb.markupManageQ)
    await state.set_state(StateMachine.all()[2])
    print(StateMachine.all()[2])

# добавить в мои вопросы
@dp.message_handler(state=StateMachine.all()[2])
async def add_question(message: manage_text['add']):
    state = dp.current_state(user=message.from_user.id)
    await message.answer("Напишите свой вопрос:", reply_markup=kb.ReplyKeyboardRemove())
    print(StateMachine.all()[1])
    await state.set_state(StateMachine.all()[1])


# ввести вопрос
@dp.message_handler(state=StateMachine.all()[1])
async def input_question(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    db_conn.insert_question(user_id=message.from_user.id, text=message.text)

    await message.answer('Вопрос успешно задан.', reply_markup=kb.markupMain)
    await state.reset_state()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)


