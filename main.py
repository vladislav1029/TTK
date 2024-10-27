from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from keyboards import (
    kbuser,
    kbredactor,
    kbadmin,
    kbnewuser,
    ikbauthorization,
    ikbauthorizationadmin,
)
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import (
    import_bd,
    check_user_bd,
    check_admin_bd,
    check_tariff_bd,
    change_tarif_client,
    check_service_bd,
    change_service_client,
    import_redactor_bd,
    check_admin,
    delete_redactor_bd,
)
from config import TOKEN_API
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import re
import os
import speech_recognition as sr
import soundfile as sf

from servises import answer_delete
from servises.validator import validate_contract_number


class RegistrationStates(StatesGroup):  # Обработчики для регистрации
    WAITING_FOR_USERNAME = State()
    WAITING_FOR_PASSWORD = State()


class EntranceStates(StatesGroup):  # Обработчики для входа
    WAITING_FOR_PASSWORD = State()


class EntranceAdminStates(StatesGroup):  # Обработчики для входа админа
    WAITING_FOR_USERNAMEADMIN = State()
    WAITING_FOR_PASSWORDADMIN = State()


class SelectTariffStates(StatesGroup):  # Обработчики для тарифа
    WAITING_FOR_SELECTTARIFF = State()


class SelectServiceStates(StatesGroup):  # Обработчики для сервиса
    WAITING_FOR_SELECTSERVICE = State()


class CreateRedactorStates(StatesGroup):  # Обработчики для регистрации
    WAITING_FOR_USERNAME_REDACTOR = State()
    WAITING_FOR_PASSWORD_REDACTOR = State()
    WAITING_FOR_ACCESS_REDACTOR = State()


class DeleteRedactorStates(StatesGroup):  # Обработчики для входа
    WAITING_FOR_LOGIN_REDACTOR = State()


bot = Bot(token=TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    print("Я запустился")


@dp.message_handler(commands=["start"])  # обрабатываем команду start
async def start_command(message: types.Message):
    await message.answer(
        text="Здравствуйте, вас приветствует компания ТТК."
        " \n <b>Подскажите, являетесь ли вы нашим клиентом:</b>",
        parse_mode="HTML",
        reply_markup=ikbauthorization,
    )
    await message.delete()


@dp.message_handler(commands=["admin"])  # обрабатываем команду start
async def start_command(message: types.Message):
    await message.answer(
        text="Здравствуйте, вас приветствует компания ТТК."
        " \n <b>Для администрирования войдите в аккаунт :</b>",
        parse_mode="HTML",
        reply_markup=ikbauthorizationadmin,
    )
    await message.delete()


@dp.callback_query_handler(
    lambda c: c.data
    in [
        "registration",
        "entrance",
        "entranceadmin",
        "about",
        "selecttariff",
        "selectadditionalservice",
        "createaccount",
        "deleteaccount",
    ]
)
async def callback_authentication(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "registration":  # колбек для регистрации
        await callback.message.answer("Введите ваш контактный номер")
        await RegistrationStates.WAITING_FOR_USERNAME.set()

    elif callback.data == "entrance":  # колбек для входа
        await callback.message.answer("Введите номер договора")
        await EntranceStates.WAITING_FOR_PASSWORD.set()
    elif callback.data == "entranceadmin":  # колбек для входа админа
        await callback.message.answer("Введите логин")
        await EntranceAdminStates.WAITING_FOR_USERNAMEADMIN.set()
    elif callback.data == "about":  # колбек для входа админа
        await callback.message.answer(
            "Компания ТрансТелеКом - один из ведущих российских операторов связи. Компания является поставщиком магистральных услуг связи для операторов и крупнейших корпораций России, а также входит в число лидеров среди провайдеров услуг широкополосного доступа в Интернет, телевидения и телефонии для конечных пользователей в регионах."
        )

    elif callback.data == "selecttariff":  # колбек для выбора тарифа
        await callback.message.answer(
            text="<b>Список доступных тарифов :</b>"
            " \n •Максимальный-1000 Гбит 800р в месяц"
            " \n •Мощный-100 Мбит 400р в месяц"
            " \n •Честный-10 Мбит 100р в месяц"
            "\n<b>Для подключения введите название тарифа :</b>",
            parse_mode="HTML",
        )
        await SelectTariffStates.WAITING_FOR_SELECTTARIFF.set()

    elif (
        callback.data == "selectadditionalservice"
    ):  # колбек для выбора дополнительных услуг
        await callback.message.answer(
            text="<b>Список дополнительных услуг :</b>"
            " \n •АнтиВирус Касперский - 100р в месяц"
            " \n •Выделенный IP - 100р в месяц"
            " \n •Персональный менеджер - 100р в месяц"
            " \n •Фирменный роутер - 100р в месяц"
            "\n<b>Для подключения введите название услуги :</b>",
            parse_mode="HTML",
        )
        await SelectServiceStates.WAITING_FOR_SELECTSERVICE.set()
    elif callback.data == "createaccount":  # колбек для добавления редактора
        await callback.message.answer("Введите логин для редактора")
        await CreateRedactorStates.WAITING_FOR_USERNAME_REDACTOR.set()

    elif callback.data == "deleteaccount":  # колбек для добавления редактора
        await callback.message.answer(
            "Введите логин редактора, которого хотите удалить"
        )
        await DeleteRedactorStates.WAITING_FOR_LOGIN_REDACTOR.set()


# Обработчик логина при регистрации клиента
@dp.message_handler(state=RegistrationStates.WAITING_FOR_USERNAME)
async def registration_username(message: types.Message, state: FSMContext):
    global registration_username
    registration_username = message.text
    await state.update_data(username=message.text)
    await message.answer("Введите адрес для подключения услуги")
    await RegistrationStates.WAITING_FOR_PASSWORD.set()


# Обработчик пароля при регистрации клиента
@dp.message_handler(state=RegistrationStates.WAITING_FOR_PASSWORD)
async def registration_password(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    username = user_data.get("username")
    password = message.text

    await state.finish()
    await message.answer("Спасибо за регистрацию!", reply_markup=kbnewuser)
    import_bd(username, password)


# Обработчик договора при входе клиента
@dp.message_handler(state=EntranceStates.WAITING_FOR_PASSWORD)
async def entrance_password(message: types.Message, state: FSMContext):
    contract_number = message.text
    if validate_contract_number(contract_number):

        access_level = check_user_bd(contract_number)

        if access_level:
            await message.answer(
                f"Здравствуйте, пользователь с договором !", reply_markup=kbuser
            )
            await state.finish()
        elif not access_level:
            await message.answer(
                f"Здравствуйте, пользователь без договора !", reply_markup=kbnewuser
            )
            await state.finish()

        else:

            await answer_delete(message, text="Такого аккаунта не существует")
            await message.delete()
    else:
        await answer_delete(message, "Номер договора должен состоять из цифр")
        await message.delete()


# Обработчик логина при входе админа
@dp.message_handler(state=EntranceAdminStates.WAITING_FOR_USERNAMEADMIN)
async def entrance_username(message: types.Message):
    global entrance_username
    entrance_username = message.text

    await message.answer("Введите пароль")
    await EntranceAdminStates.WAITING_FOR_PASSWORDADMIN.set()


# Обработчик пароля при входе админа
@dp.message_handler(state=EntranceAdminStates.WAITING_FOR_PASSWORDADMIN)
async def entrance_password(message: types.Message, state: FSMContext):
    global entrance_password
    entrance_password = message.text

    access_level = check_admin_bd(entrance_username, entrance_password)
    if access_level:
        await message.answer(
            f"Здравствуйте, {entrance_username}!", reply_markup=kbadmin
        )
        await state.finish()
    elif not access_level:
        await message.answer(
            f"Здравствуйте, {entrance_username}!", reply_markup=kbredactor
        )
        await state.finish()
    else:
        await answer_delete(message=message, text="Такого аккаунта не существует")
        await message.delete()


# проверка тарифа
@dp.message_handler(state=SelectTariffStates.WAITING_FOR_SELECTTARIFF)
async def select_tariff(message: types.Message, state: FSMContext):
    tariff = message.text
    tarif = tariff.strip().lower()
    tariff_id = check_tariff_bd(tarif)

    if tariff_id == "max":
        await message.answer(f"Выбран тариф максимальный")
        change_tarif_client(tariff_id, registration_username)
        await state.finish()
    elif tariff_id == "norm":
        await message.answer(f"Выбран тариф мощный")
        change_tarif_client(tariff_id, registration_username)
        await state.finish()
    elif tariff_id == "min":
        await message.answer(f"Выбран тариф честный")
        change_tarif_client(tariff_id, registration_username)
        await state.finish()

    else:
        await answer_delete(message, "Такого тарифа не существует")
        await message.delete()


# проверка услуги
@dp.message_handler(state=SelectServiceStates.WAITING_FOR_SELECTSERVICE)
async def select_service(message: types.Message, state: FSMContext):
    service = message.text

    service_id = check_service_bd(service)

    if service_id == "antivirus":
        await message.answer(f"Выбрана услуга антивирус касперский")
        change_service_client(service_id, registration_username)
        await state.finish()
    elif service_id == "manager":
        await message.answer(f"Выбрана услуга персональный менеджер")
        change_service_client(service_id, registration_username)
        await state.finish()
    elif service_id == "ip":
        await message.answer(f"Выбрана услуга выделенный ip")
        change_service_client(service_id, registration_username)
        await state.finish()
    elif service_id == "router":
        await message.answer(f"Выбрана услуга фирменный роутер")
        change_service_client(service_id, registration_username)
        await state.finish()
    else:
        await answer_delete(message, "Такой услуги не существует")
        await message.delete()

    


# Обработчик логина при регистрации редактора
@dp.message_handler(state=CreateRedactorStates.WAITING_FOR_USERNAME_REDACTOR)
async def registration_username_redactor(message: types.Message, state: FSMContext):

    await state.update_data(username=message.text)
    await message.answer("Введите пароль для редактора")
    await CreateRedactorStates.WAITING_FOR_PASSWORD_REDACTOR.set()


# Обработчик пароля при регистрации редактора
@dp.message_handler(state=CreateRedactorStates.WAITING_FOR_PASSWORD_REDACTOR)
async def registration_password_redactor(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer("Введите уровень доступа (админ/редактор)")
    await CreateRedactorStates.WAITING_FOR_ACCESS_REDACTOR.set()


# Обработчик уровня доступа при регистрации редактора
@dp.message_handler(state=CreateRedactorStates.WAITING_FOR_ACCESS_REDACTOR)
async def registration_access_redactor(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    username = user_data.get("username")
    password = user_data.get("password")
    access = message.text.lower()

    if access == "админ":
        access_level = 1
    elif access == "редактор":
        access_level = 0
    else:
        await message.answer(
            'Неверный уровень доступа. Пожалуйста, введите "админ" или "редактор".'
        )
        return

    await state.finish()
    await message.answer("Пользователь успешно добавлен!")
    import_redactor_bd(username, password, access_level)


# Обработчик принимающий логин для удаления
@dp.message_handler(state=DeleteRedactorStates.WAITING_FOR_LOGIN_REDACTOR)
async def delete_redactor(message: types.Message, state: FSMContext):
    login = message.text
    redactor = check_admin(login)
    if redactor:
        delete_redactor_bd(login)
        await message.answer("Пользователь удален")
    else:
        await message.answer("Пользователь не найден")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
