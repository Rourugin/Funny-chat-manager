from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Еда', callback_data='food_shop'),
     InlineKeyboardButton(text='Одежда', callback_data='clothes_shop')],
])