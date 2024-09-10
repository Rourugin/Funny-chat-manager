from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


casino_main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Play', callback_data='play_casino'),
     InlineKeyboardButton(text='Refuse', callback_data='reject_casino')],
    [InlineKeyboardButton(text='Info', callback_data='info_casino')]
])