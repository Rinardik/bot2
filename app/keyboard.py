from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог'), KeyboardButton(text='Корзина')], 
    [KeyboardButton(text='Контакты')]])
admin_panel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Добавить товар'), KeyboardButton(text='Удалить товар')]], resize_keyboard=True)
catalog_list = InlineKeyboardMarkup(
    inline_keyboard=[[KeyboardButton(text="Добавить в корзину")],
              [InlineKeyboardButton(text='Футболки')],
            [InlineKeyboardButton(text="Шорты")],
            [InlineKeyboardButton(text="Кроссовки")]]
)
Dop_tow = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Инструкция по <<Добавить товар>>')]])
Yd_tow = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Инструкция по <<Удалить товар>>')]])