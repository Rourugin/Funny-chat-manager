from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


casino_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Играть', callback_data='play_casino'),
     InlineKeyboardButton(text='Отказаться', callback_data='reject_casino')],
    [InlineKeyboardButton(text='Инфо', callback_data='info_casino')]
])


roulette_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Играть', callback_data='play_roulette'),
     InlineKeyboardButton(text='Отказаться', callback_data='reject_roulette')],
    [InlineKeyboardButton(text='Инфо', callback_data='info_roulette')]
])