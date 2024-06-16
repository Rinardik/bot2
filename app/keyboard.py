from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Каталог'), KeyboardButton(text='Корзина')], 
    [KeyboardButton(text='Контакты')]])
admin_panel = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить товар'), KeyboardButton(text='Удалить товар')], 
    [KeyboardButton(text='Сделать рассылку')]], resize_keyboard=True)
url_button_1 = KeyboardButton(
    text='Футболки'
)
url_button_2 = KeyboardButton(
    text="Шорты"
)
url_button_3 = KeyboardButton(
    text="Кроссовки"
)
catalog_list = ReplyKeyboardMarkup(
    keyboard=[[url_button_1],
            [url_button_2],
            [url_button_3]]
)