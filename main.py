from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from keyboards import kbuser, kbredactor, kbadmin, kbnewuser, ikbauthorization, ikbauthorizationadmin,ikmytarif,ikservice,iktarif
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database import import_bd, check_user_bd, check_admin_bd, check_tariff_bd, change_tarif_client, check_service_bd, change_service_client, import_redactor_bd, check_admin, delete_redactor_bd, get_user_tariff_and_services,find_category,add_category,edit_category,delete_category
from config import TOKEN_API
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from validate import validate_contract_number,validate_email,validate_phone_number

from servises import *
import re
import os
import speech_recognition as sr
import soundfile as sf

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

class SelectServiceStates(StatesGroup):  # Обработчики для тарифа
    WAITING_FOR_SELECTSERVICE = State()

class CreateRedactorStates(StatesGroup):  # Обработчики для регистрации
    WAITING_FOR_USERNAME_REDACTOR = State()
    WAITING_FOR_PASSWORD_REDACTOR = State()
    WAITING_FOR_ACCESS_REDACTOR = State()


class CreateCategoryStates(StatesGroup):  # Обработчики для создания категорий
    WAITING_FOR_NAME = State()
    WAITING_FOR_WORD = State()

class EditCategoryStates(StatesGroup):  # Обработчики для создания категорий
    WAITING_FOR_NAME = State()
    WAITING_FOR_WORD = State()

class DeleteCategoryStates(StatesGroup):  # Обработчики для создания категорий
    WAITING_FOR_NAME = State()


class DeleteRedactorStates(StatesGroup):  # Обработчики для входа
    WAITING_FOR_LOGIN_REDACTOR = State()

bot = Bot(token=TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def on_startup(_):
    print('Я запустился')

@dp.message_handler(commands=['start'])  # обрабатываем команду start
async def start_command(message: types.Message):
    await message.answer(text='Здравствуйте, вас приветствует компания ТТК.'
                              ' \n <b>Подскажите, являетесь ли вы нашим клиентом:</b>', parse_mode='HTML', reply_markup=ikbauthorization)
    await message.delete()

@dp.message_handler(commands=['admin'])  # обрабатываем команду start
async def start_command(message: types.Message):
    await message.answer(text='Здравствуйте, вас приветствует компания ТТК.'
                              ' \n <b>Для администрирования войдите в аккаунт :</b>', parse_mode='HTML', reply_markup=ikbauthorizationadmin)
    await message.delete()


@dp.message_handler(content_types=types.ContentType.VOICE)
async def process_voice_message(message: types.Message):
    if message.voice:
        # Получаем объект File из сообщения пользователя
        voice_file = await bot.get_file(message.voice.file_id)
        voice_path = voice_file.file_path
        # Генерируем путь для сохранения файла
        file_name = f'{message.voice.file_id}.ogg'
        file_path = os.path.join('C:\\Users\\anast\\PycharmProjects\\TTK', file_name)
        # Скачиваем голосовое сообщение
        await bot.download_file(voice_path, file_path)
        # Конвертируем аудиофайл в формат WAV
        ogg_file_path = f'{message.voice.file_id}.ogg'
        wav_file_path = os.path.join('C:\\Users\\anast\\PycharmProjects\\TTK', ogg_file_path)
        # Чтение аудиофайла в формате OGG
        audio_data, sample_rate = sf.read(ogg_file_path)
        # Запись аудиофайла в формате WAV
        sf.write(wav_file_path, audio_data, sample_rate, format='WAV')
        # Распознаём речь из аудиофайла
        r = sr.Recognizer()
        with sr.AudioFile(wav_file_path) as source:
            audio_data = r.record(source)
        text = r.recognize_google(audio_data, language='ru')  # Можно указать другой язык, если необходимо
        print(text)

        # Определяем категорию по распознанному тексту
        category = find_category(text.lower())

        if category:
            if category == '1':
                await message.answer("Категория вашего запроса: Мой тариф", reply_markup=ikmytarif)
            elif category == '2':
                await message.answer("Категория вашего запроса: Подключить услугу", reply_markup=ikservice)
            elif category == '3':
                await message.answer("Категория вашего запроса: Подключить тариф", reply_markup=iktarif)
            else:
                await message.answer(f"Категория вашего запроса: {category}")
        else:
            await message.answer("К сожалению, я не смог определить категорию вашего запроса.")
    else:
        # Если сообщение не содержит голосового, отправляем пользователю сообщение об ошибке
        await message.reply("Что-то пошло не так, повторите ввод")

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
    message_text = message.text.lower()  # Приводим текст к нижнему регистру
    category = find_category(message_text)

    if category:
        if category == '1':
            await message.answer("Категория вашего запроса: Мой тариф", reply_markup=ikmytarif)
        elif category == '2':
            await message.answer("Категория вашего запроса: Подключить услугу", reply_markup=ikservice)
        elif category == '3':
            await message.answer("Категория вашего запроса: Подключить тариф", reply_markup=iktarif)
        else:
            await message.answer(f"Категория вашего запроса: {category}")
    else:
        await message.answer("К сожалению, я не смог определить категорию вашего запроса.")

@dp.callback_query_handler(lambda c: c.data in ['registration', 'entrance', 'entranceadmin', 'about', 'selecttariff', 'selectadditionalservice', 'createaccount', 'deleteaccount', 'mytariff' , 'createintention', 'editintention', 'deleteintention'])
async def callback_authentication(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'registration':  # колбек для регистрации
        await callback.message.answer('Введите ваш контактный номер')
        await RegistrationStates.WAITING_FOR_USERNAME.set()

    elif callback.data == 'entrance':  # колбек для входа
        await callback.message.answer('Введите номер договора')
        await EntranceStates.WAITING_FOR_PASSWORD.set()
    elif callback.data == 'entranceadmin':  # колбек для входа админа
        await callback.message.answer('Введите логин')
        await EntranceAdminStates.WAITING_FOR_USERNAMEADMIN.set()
    elif callback.data == 'about':  # колбек для входа админа
        await callback.message.answer('Компания ТрансТелеКом - один из ведущих российских операторов связи. Компания является поставщиком магистральных услуг связи для операторов и крупнейших корпораций России, а также входит в число лидеров среди провайдеров услуг широкополосного доступа в Интернет, телевидения и телефонии для конечных пользователей в регионах.')

    elif callback.data == 'selecttariff':  # колбек для выбора тарифа
        await callback.message.answer(text='<b>Список доступных тарифов :</b>'
                                  ' \n Максимальный-1000 Гбит 800р в месяц'
                                  ' \n Мощный-100 Мбит 400р в месяц'
                                  ' \n Честный-10 Мбит 100р в месяц'
                                  '<b>Для подключения введите название тарифа :</b>'
                             , parse_mode='HTML')
        await SelectTariffStates.WAITING_FOR_SELECTTARIFF.set()

    elif callback.data == 'selectadditionalservice':  # колбек для выбора дополнительных услуг
        await callback.message.answer(text='<b>Список дополнительных услуг :</b>'
                                  ' \n АнтиВирус Касперский-100р в месяц'
                                  ' \n Выделенный IP-100р в месяц'
                                  ' \n Персональный менеджер-100р в месяц'
                                  ' \n Фирменный роутер-100р в месяц'
                                  '<b>Для подключения введите название услуги :</b>'
                             , parse_mode='HTML')
        await SelectServiceStates.WAITING_FOR_SELECTSERVICE.set()
    elif callback.data == 'createaccount':  # колбек для добавления редактора
        await callback.message.answer('Введите логин для редактора')
        await CreateRedactorStates.WAITING_FOR_USERNAME_REDACTOR.set()

    elif callback.data == 'deleteaccount':  # колбек для добавления редактора
        await callback.message.answer('Введите логин редактора, которого хотите удалить')
        await DeleteRedactorStates.WAITING_FOR_LOGIN_REDACTOR.set()


    elif callback.data == 'createintention':  # колбек для создания категории

        await callback.message.answer('Введите название категории')
        await CreateCategoryStates.WAITING_FOR_NAME.set()


    elif callback.data == 'editintention':  # колбек для изменения категории

        await callback.message.answer('Введите название категории')
        await EditCategoryStates.WAITING_FOR_NAME.set()


    elif callback.data == 'deleteintention':  # колбек для удаления категории

        await callback.message.answer('Введите название категории')
        await DeleteCategoryStates.WAITING_FOR_NAME.set()

    elif callback.data == 'mytariff':  # колбек для просмотра текущего тарифа и услуг
        user_data = await state.get_data()
        username = user_data.get('username')
        print(f"Username from state: {username}")  # Отладочное сообщение

        if username:
            tariff, services = get_user_tariff_and_services(username)
            await callback.message.answer(f"Ваш тариф: {tariff}\nВаши подключенные услуги: {', '.join(services)}")

        else:
            await callback.message.answer("Информация о вашем тарифе недоступна.")

# Обработчик логина при регистрации клиента
@dp.message_handler(state=RegistrationStates.WAITING_FOR_USERNAME)
async def registration_username(message: types.Message, state: FSMContext):
    global registration_username
    registration_username = message.text
    if not validate_phone_number(registration_username):
        await answer_delete(message,'Неверный формат номера телефона. Пожалуйста, введите номер в правильном формате.')
        await message.delete()
        return
    await state.update_data(username=message.text)
    await message.answer('Введите почту для подключения услуги')
    await RegistrationStates.WAITING_FOR_PASSWORD.set()

@dp.message_handler(state=RegistrationStates.WAITING_FOR_PASSWORD)
async def registration_password(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    username = user_data.get('username')
    password = message.text
    if not validate_email(password):
        await answer_delete(message,'Неверный формат почты. Пожалуйста, введите почту в правильном формате.')
        await message.delete()
        return

    # Предположим, что access = 0 для новых пользователей
    access = 0
    temp_doc = import_bd(username, password, access)

    await state.finish()

    await message.answer(f"Спасибо за регистрацию! Ваш временный код: {temp_doc}", reply_markup=kbnewuser)

# Обработчик пароля при входе клиента
@dp.message_handler(state=EntranceStates.WAITING_FOR_PASSWORD)
async def entrance_password(message: types.Message, state: FSMContext):
    password = message.text
    if not validate_contract_number(password):
        await answer_delete(message,'Неверный формат номера договора. Пожалуйста, введите номер в правильном формате.')
        await message.delete()
        return

    access_level = check_user_bd(password)

    if access_level:
        await message.answer(f"Здравствуйте, пользователь с договором !", reply_markup=kbuser)
        await state.update_data(username=password)  # Сохраняем username в состоянии state
    elif not access_level:
        await message.answer(f"Здравствуйте, пользователь без договора !", reply_markup=kbnewuser)
        await state.update_data(username=password)  # Сохраняем username в состоянии state
    else:
        await message.answer("Такого аккаунта не существует")

    await state.finish()

# Обработчик логина при входе админа
@dp.message_handler(state=EntranceAdminStates.WAITING_FOR_USERNAMEADMIN)
async def entrance_username(message: types.Message):
    global entrance_username
    entrance_username = message.text

    await message.answer('Введите пароль')
    await EntranceAdminStates.WAITING_FOR_PASSWORDADMIN.set()

# Обработчик пароля при входе админа
@dp.message_handler(state=EntranceAdminStates.WAITING_FOR_PASSWORDADMIN)
async def entrance_password(message: types.Message, state: FSMContext):
    global entrance_password
    entrance_password = message.text

    access_level = check_admin_bd(entrance_username, entrance_password)

    if access_level :
        await message.answer(f"Здравствуйте, {entrance_username}!", reply_markup=kbadmin)
        await state.finish()
    elif not access_level :
        await message.answer(f"Здравствуйте, {entrance_username}!", reply_markup=kbredactor)
        await state.finish()
    else:
        await answer_delete(message,"Такого аккаунта не существует")
        await message.delete()



# Проверка тарифа
@dp.message_handler(state=SelectTariffStates.WAITING_FOR_SELECTTARIFF)
async def select_tariff(message: types.Message, state: FSMContext):
    tariff = message.text.strip().lower()

    tariff_id = check_tariff_bd(tariff)

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
        await answer_delete(message , "Такого тарифа не существует")
        await  message.delete()


# Проверка услуги
@dp.message_handler(state=SelectServiceStates.WAITING_FOR_SELECTSERVICE)
async def select_service(message: types.Message, state: FSMContext):
    service = message.text.strip().lower()

    service_id = check_service_bd(service)

    if service_id:
        await message.answer(f"Выбрана услуга {service_id}")
        change_service_client(service_id, registration_username)
        await state.finish()
    else:
        await answer_delete(message,"Такой услуги не существует")
        await message.delete()



# Обработчик логина при регистрации редактора
@dp.message_handler(state=CreateRedactorStates.WAITING_FOR_USERNAME_REDACTOR)
async def registration_username_redactor(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer('Введите пароль для редактора')
    await CreateRedactorStates.WAITING_FOR_PASSWORD_REDACTOR.set()

# Обработчик пароля при регистрации редактора
@dp.message_handler(state=CreateRedactorStates.WAITING_FOR_PASSWORD_REDACTOR)
async def registration_password_redactor(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer('Введите уровень доступа (админ/редактор)')
    await CreateRedactorStates.WAITING_FOR_ACCESS_REDACTOR.set()

# Обработчик уровня доступа при регистрации редактора
@dp.message_handler(state=CreateRedactorStates.WAITING_FOR_ACCESS_REDACTOR)
async def registration_access_redactor(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    username = user_data.get('username')
    password = user_data.get('password')
    access = message.text.lower()

    if access == 'админ':
        access_level = 1
    elif access == 'редактор':
        access_level = 0
    else:
        await answer_delete(message,'Неверный уровень доступа. Пожалуйста, введите "админ" или "редактор".')
        return

    await state.finish()
    await message.answer('Пользователь успешно добавлен!')
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

@dp.message_handler(state=CreateCategoryStates.WAITING_FOR_NAME)
async def create_category_name(message: types.Message, state: FSMContext):
    category_name = message.text
    await state.update_data(category_name=category_name)
    await message.answer('Введите список ключевых слов через запятую')
    await CreateCategoryStates.WAITING_FOR_WORD.set()

@dp.message_handler(state=CreateCategoryStates.WAITING_FOR_WORD)
async def create_category_word(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    category_name = user_data.get('category_name')
    words = message.text.split(',')
    add_category(category_name, words)
    await message.answer(f'Категория "{category_name}" создана с ключевыми словами: {", ".join(words)}')
    await state.finish()

@dp.message_handler(state=EditCategoryStates.WAITING_FOR_NAME)
async def edit_category_name(message: types.Message, state: FSMContext):
    category_name = message.text
    await state.update_data(category_name=category_name)
    await message.answer('Введите новый список ключевых слов через запятую')
    await EditCategoryStates.WAITING_FOR_WORD.set()

@dp.message_handler(state=EditCategoryStates.WAITING_FOR_WORD)
async def edit_category_word(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    category_name = user_data.get('category_name')
    words = message.text.split(',')
    edit_category(category_name, words)
    await message.answer(f'Категория "{category_name}" обновлена с ключевыми словами: {", ".join(words)}')
    await state.finish()

@dp.message_handler(state=DeleteCategoryStates.WAITING_FOR_NAME)
async def delete_category_name(message: types.Message, state: FSMContext):
    category_name = message.text
    delete_category(category_name)
    await message.answer(f'Категория "{category_name}" удалена')
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
