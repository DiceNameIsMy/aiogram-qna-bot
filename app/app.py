import logging

import database_connection

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