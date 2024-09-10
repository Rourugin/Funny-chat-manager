from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


casino_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сыграть', callback_data='play_casino'),
     InlineKeyboardButton(text='Отказаться', callback_data='reject_casino')],
    [InlineKeyboardButton(text='Инфо', callback_data='info_casino')]
])