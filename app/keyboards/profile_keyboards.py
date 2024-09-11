from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Еда', callback_data='food_prof'),
    InlineKeyboardButton(text='Одежда', callback_data='clothes_prof')],
])


eat = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Скуби Снэк', callback_data='eat_scooby_snack'),
    InlineKeyboardButton(text='5 за 3', callback_data='eat_five_for_three')],
    [InlineKeyboardButton(text='Назад', callback_data='back_prof')]
])


latex = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Латексный костюм', callback_data='wear_latex')],
    [InlineKeyboardButton(text='Назад', callback_data='back_prof')]
])


crusader = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Костюм крестоносца', callback_data='wear_crusader')],
    [InlineKeyboardButton(text='Назад', callback_data='back_prof')]
])


clown = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Клоунский костюм', callback_data='wear_clown')],
    [InlineKeyboardButton(text='Назад', callback_data='back_prof')]
])


latex_crusader = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Латексный костюм', callback_data='wear_latex'),
    InlineKeyboardButton(text='Костюм крестоносца', callback_data='wear_crusader')],
    [InlineKeyboardButton(text='Назад', callback_data='back_prof')]
])


latex_clown = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Латексный костюм', callback_data='wear_latex'),
    InlineKeyboardButton(text='Клоунский костюм', callback_data='wear_clown')],
    [InlineKeyboardButton(text='Назад', callback_data='back_prof')]
])


crusader_clown = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Костюм крестоносца', callback_data='wear_crusader'),
    InlineKeyboardButton(text='Клоунский костюм', callback_data='wear_clown')],
    [InlineKeyboardButton(text='Назад', callback_data='back_prof')]
])


latex_crusader_clown = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Латексный костюм', callback_data='wear_latex'),
    InlineKeyboardButton(text='Костюм крестоносца', callback_data='wear_crusader')],
    [InlineKeyboardButton(text='Клоунский костюм', callback_data='wear_clown')],
    [InlineKeyboardButton(text='Назад', callback_data='back_prof')]
])


test_callback = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='push me', callback_data='callback_test')]
])