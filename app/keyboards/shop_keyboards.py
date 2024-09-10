from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Food', callback_data='food_shop'),
     InlineKeyboardButton(text='Clothes', callback_data='clothes_shop')],
])


buy_food = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Buy Scooby Snack', callback_data='buy_scooby_snack'),
     InlineKeyboardButton(text='Buy 5 for 300', callback_data='buy_five')],
    [InlineKeyboardButton(text='Back', callback_data='back_shop')]
])


buy_clothes = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Buy latex suit', callback_data='buy_latex')],
    [InlineKeyboardButton(text='Back', callback_data='back_shop')]
])