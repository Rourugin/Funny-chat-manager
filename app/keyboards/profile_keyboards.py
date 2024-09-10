from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Food', callback_data='food_prof'),
    InlineKeyboardButton(text='Cloths', callback_data='clothes_prof')],
])


eat = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Scooby Snack', callback_data='eat_scooby_snack'),
    InlineKeyboardButton(text='5 for 3', callback_data='eat_five_for_three')],
    [InlineKeyboardButton(text='Back', callback_data='back_prof')]
])


latex = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Latex suit', callback_data='wear_latex')],
    [InlineKeyboardButton(text='Back', callback_data='back_prof')]
])


crusader = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Crusader suit', callback_data='wear_crusader')],
    [InlineKeyboardButton(text='Back', callback_data='back_prof')]
])


clown = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Clown suit', callback_data='wear_clown')],
    [InlineKeyboardButton(text='Back', callback_data='back_prof')]
])


latex_crusader = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Latex suit', callback_data='wear_latex'),
    InlineKeyboardButton(text='Crusader suit', callback_data='wear_crusader')],
    [InlineKeyboardButton(text='Back', callback_data='back_prof')]
])


latex_clown = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Latex suit', callback_data='wear_latex'),
    InlineKeyboardButton(text='Clown suit', callback_data='wear_clown')],
    [InlineKeyboardButton(text='Back', callback_data='back_prof')]
])


crusader_clown = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Crusader suit', callback_data='wear_crusader'),
    InlineKeyboardButton(text='Clown suit', callback_data='wear_clown')],
    [InlineKeyboardButton(text='Back', callback_data='back_prof')]
])


latex_crusader_clown = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Latex suit', callback_data='wear_latex'),
    InlineKeyboardButton(text='Crusader suit', callback_data='wear_crusader')],
    [InlineKeyboardButton(text='Clown suit', callback_data='wear_clown')],
    [InlineKeyboardButton(text='Back', callback_data='back_prof')]
])