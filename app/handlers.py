from aiogram import Router, F
import os
import app.keyboard as kb
from aiogram.filters import Command, CommandStart
import sqlite3


router = Router()


@router.message(CommandStart())
async def cmd_id(message):
    await message.answer('Добро пожаловать в магазин одежды Rinardik_shop! \n Выберайте вещи в каталоге, добовляйте в карзину и покупайте онлайн!',
                         kb.start)


@router.message(Command(commands='id'))
async def cmd_id(message):
    await message.answer(message.from_user.id)


@router.message(F.text == 'Каталог')
async def catalog(message):
    await message.answer(reply_markup=await kb.catalog_list)


@router.message(F.text == 'Корзина')
async def cart(message):
    await message.answer(из таб)


@router.message(F.text == 'Контакты')
async def contacts(message):
    await message.answer('Покупать товар у него: {}')


@router.message(F.text == 'Админ-панель')
async def contacts(message):
    if message.from_user.id == id:
        await message.answer('Вы вошли в админ-панель', reply_markup=await kb.admin_panel)
    else:
        await message.answer('Я тебя не понимаю.')

@router.message(из таб)
async def reg_one(message, state):
    await state.set_state(Reg.name)
    await message.answer('Введите ваше имя')


@router.message(из таб)
async def reg_two(message, state):
    await state.update_data(name=message.text)
    await state.set_state(из таб)
    await message.answer('Введите номер телефона')

@router.message(из таб)
async def two_three(message, state):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f"Спасибо, регистрация завершенна. \nИмя: {data['name']}\n Номер: {data['number']}")
    await state.clear()
