from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
ikbauthorization=InlineKeyboardMarkup(row_width=2)
ibb1=InlineKeyboardButton('Войти как клиент ТТК',
                         callback_data='entrance')
ibb2=InlineKeyboardButton('Заключить новый договор',
                         callback_data='registration')
ikbauthorization.add(ibb1).add(ibb2)


ikbauthorizationadmin=InlineKeyboardMarkup(row_width=2)
ibb1=InlineKeyboardButton('Войти',
                         callback_data='entranceadmin')

ikbauthorizationadmin.add(ibb1)


kbuser = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
b1 = KeyboardButton('Изменить тариф')
b2 = KeyboardButton('Подключить дополнительную услугу')
kbuser.add(b1, b2)

kbnewuser = InlineKeyboardMarkup(row_width=2)
b1 = InlineKeyboardButton('Узнать о нас',
                          callback_data='about')
b2 = InlineKeyboardButton('Выбрать тариф',
                         callback_data='selecttariff')
b3 = InlineKeyboardButton('Выбрать дополнительную услугу',
                         callback_data='selectadditionalservice')
kbnewuser.add(b1,b2).add(b3)


kbredactor=ReplyKeyboardMarkup(resize_keyboard=True)
bp1=KeyboardButton('Намерения')
kbredactor.add(bp1)


kbadmin=InlineKeyboardMarkup(row_width=2)
bp1=InlineKeyboardButton('Создать аккаунт',
                          callback_data='createaccount')
bp2=InlineKeyboardButton('Удалить аккаунт',
                          callback_data='deleteaccount')
kbadmin.add(bp1, bp2)