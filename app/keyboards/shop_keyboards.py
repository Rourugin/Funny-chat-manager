from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Еда', callback_data='food_shop'),
     InlineKeyboardButton(text='Одежда', callback_data='clothes_shop')],
])


buy_food = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Купить скуби снэк', callback_data='buy_scooby_snack'),
     InlineKeyboardButton(text='Купить 5 за 300', callback_data='buy_five')],
    [InlineKeyboardButton(text='Назад', callback_data='back_shop')]
])


buy_clothes = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Купить латексный костюм', callback_data='buy_latex')],
    [InlineKeyboardButton(text='Назад', callback_data='back_shop')]
])