from aiogram import Router, F
import keyboard as kb
from aiogram.filters import Command, CommandStart, StateFilter
import sqlite3
from const import ID as id
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton


class FSMFillForm(StatesGroup):
    fill_name = State()        
    fill_num = State()

       

data_base = sqlite3.connect("user_db")
c = data_base.cursor()
c.execute(""" CREATE TABLE user_data_base (
          user_id integer,
          basket list,
          num integer,
          name text
) """)
data_base.commit()


data_base2 = sqlite3.connect("katalog_db")
c2 = data_base.cursor()
c2.execute(""" CREATE TABLE user_katalog_db (
          kat text,
        phot text,
           op text
        price integer
) """)
data_base2.commit()


router = Router()

@router.message(Command(commands='регистрация'), StateFilter(default_state))
async def reg_one(message, state):
    await message.answer('Введите ваше имя')
    await state.set_state(FSMFillForm.fill_name)


@router.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
async def reg_two(message, state):
    await c.execute(f"UPDATE user_data_base SET name = {message.text} WHERE user_id = {message.from_user.id}")
    await message.answer('Введите номер телефона')
    await state.set_state(FSMFillForm.fill_num)

@router.message(StateFilter(FSMFillForm.fill_num))
async def two_three(message):
    num_user = message.text
    if num_user[0] == "+":
        num_user = int('8' + num_user[2:])
    await c.execute(f"UPDATE user_data_base SET num = {num_user} WHERE user_id = {message.from_user.id}")
    await message.answer(f"Спасибо, регистрация завершенна.")


@router.message(CommandStart(), StateFilter(default_state))
async def start(message):
    await message.answer('Добро пожаловать в магазин одежды Rinardik_shop! \n \
                         Выберайте вещи в каталоге, добовляйте в карзину и покупайте онлайн!', kb.start)


@router.message(Command(commands='id'))
async def cmd_id(message):
    await message.answer(message.from_user.id)


@router.message(F.text == 'Каталог', StateFilter(default_state))
async def catalog(message):
    c2.execute("SELECT * FROM user_katalog_db")
    for i in c.fetchall():
        catlist1 =  InlineKeyboardMarkup(
    inline_keyboard=[[KeyboardButton(text=F"Добавить в корзину{i}")],
              [InlineKeyboardButton(text='Футболки')],
            [InlineKeyboardButton(text="Шорты")],
            [InlineKeyboardButton(text="Кроссовки")]])
        await message.send_photo(message.chat.id, photo=i[2], caption=f'Товар под номером: {i[0]} \n{i[3]} \n цена:{i[4]}руб.', reply_markup= kb.catlist1)

@router.callback_query('Добавить в корзину' in F.text, StateFilter(default_state))
async def reg_one(callback):
    num_prod = F.text.split()[3]
    c2.execute(f"SELECT * FROM user_katalog_db WHERE rowid = {num_prod}")
    c2_tow = c2.fetchall()
    c.execute(f"UPDATE user_data_base SET basket = {c2_tow} WHERE user_id = {callback.from_user.id}")
    await callback.answer(f'Товар под номером {num_prod} добавлен в корзину')
    
    
@router.callback_query(F.text == 'Футболки', StateFilter(default_state))
async def catalog_t_shirt(message):
    c2.execute("SELECT * FROM user_katalog_db WHERE kat = 'Футболки'")
    for i in c2.fetchall():
        await message.send_photo(message.chat.id, photo=i[2], caption=f'Товар под номером: {i[0]} \n{i[3]} \n цена:{i[4]}руб.', reply_markup= kb.catalog_list)


@router.callback_query(F.text == 'Шорты', StateFilter(default_state))
async def catalog_shorts(message):
    c2.execute("SELECT * FROM user_katalog_db WHERE kat = 'Шорты'")
    for i in c2.fetchall():
        await message.send_photo(message.chat.id, photo=i[2], caption=f'Товар под номером: {i[0]} \n{i[3]} \n цена:{i[4]}руб.', reply_markup= kb.catalog_list)

@router.callback_query(F.text == 'Кроссовки', StateFilter(default_state))
async def catalog_sneakers(message):
    c2.execute("SELECT * FROM user_katalog_db WHERE kat = 'Кроссовки'")
    for i in c2.fetchall():
        await message.send_photo(message.chat.id, photo=i[2], caption=f'Товар под номером: {i[0]} \n{i[3]} \n цена:{i[4]}руб.', reply_markup= kb.catalog_list)


@router.message(F.text == 'Корзина', StateFilter(default_state))
async def cart(message):
    await c.execute(f"SELECT basket FROM user_data_base WHERE user_id = {message.from_user.id}")
    if c.fetchall():
        for i in c.fetchall():
            await message.send_photo(message.chat.id, photo=i[2], caption=f'Товар под номером: {i[0]} \n{i[3]} \n цена:{i[4]}руб.', reply_markup= kb.catalog_list)
    else:
        await message.answer('Корзина пуста')


@router.message(F.text == 'Контакты', StateFilter(default_state))
async def contacts(message):
    await message.answer('Покупать товар у него: https://github.com/Rinardik\nhttps://t.me/rinardahm')


@router.message(F.text == 'Админ-панель')
async def ad_panel(message):
    if message.from_user.id == id:
        await message.answer('Вы вошли в админ-панель', reply_markup=await kb.admin_panel)
    else:
        await message.answer('Я тебя не понимаю.')


@router.message(F.text == 'Добавить товар')
async def dop(message):
    if message.from_user.id == id:
        additional_list = message.text.split("###")
        if additional_list[1] in ["Футболки", "Шорты", "Кроссовки"] and additional_list[0] in "https:/":
            await message.answer("Товар добавлен!", reply_markup= kb.Dop_tow)
            c2.execute(f"INSERT INTO user_katalog_db VALUES ({additional_list[0]}, {additional_list[1]}, {additional_list[2]}, {additional_list[3]})")
        else:
            await message.answer("Делайте по инструкции...", reply_markup= kb.Dop_tow)
    else:
        await message.answer('Я тебя не понимаю.')


@router.callback_query(F.text == 'Инструкция по <<Добавить товар>>')
async def dop_i(message):
    if message.from_user.id == id:
        await message.answer('чтобы добавить товар нужно: категория, фото, описание, цена\n \
                             Например:\n \
                            Футболки###url###описание###1234')
    else:
        await message.answer('Я тебя не понимаю.')

@router.message('Удалить товар' in F.text)
async def yd(message):
    if message.from_user.id == id:
        yd_num = message.text.split()
        if yd_num[0:13] == 'Удалить товар ' and yd_num[14] == "[" and yd_num[-1] == "]":
            yd_num1 = list(yd_num[2])
            for i in yd_num1:
                c.execute(f"DELETE FROM user_katalog_db WHERE rowid = {i}")
            await message.answer('Товар(ы) удаленны')
        else:
            await message.answer('Используй инструкцию!', reply_markup= kb.Yd_tow)
    else:
        await message.answer('Я тебя не понимаю.')

@router.callback_query(F.text == 'Инструкция по <<Удалить товар>>')
async def yd_i(message):
    if message.from_user.id == id:
        await message.answer('чтобы удалить товар нужно написать <<Удалить товар>> и в [] перечислить номера товаров(номера можно найти в каталоге)')
    else:
        await message.answer('Я тебя не понимаю.')

@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command_state(message, state):
    await message.answer(
        text='Вам нечего отменять\n\n'
             'Чтобы перейти к заполнению анкеты - '
             'отправьте <<регистрация>> /'
    )

@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message, state):
    await message.answer(
        text='Вы вышли из регистрации\n\n'
             'Чтобы снова перейти к заполнению анкеты - '
             'отправьте <<регистрация>> /'
    )
    await state.clear()


@router.message()
async def all_not(message):
    await message.answer('Извините, моя твоя не понимать')
data_base.close()
data_base2.close()