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


kbuser = InlineKeyboardMarkup(row_width=2)
b1 = InlineKeyboardButton('Изменить тариф',
                         callback_data='selecttariff')
b2 = InlineKeyboardButton('Подключить дополнительную услугу',
                         callback_data='selectadditionalservice')
b3 = InlineKeyboardButton('Мой тариф',
                         callback_data='mytariff')

kbuser.add(b1, b2).add(b3)

kbnewuser = InlineKeyboardMarkup(row_width=2)
b1 = InlineKeyboardButton('Узнать о нас',
                          callback_data='about')
b2 = InlineKeyboardButton('Выбрать тариф',
                         callback_data='selecttariff')
b3 = InlineKeyboardButton('Выбрать дополнительную услугу',
                         callback_data='selectadditionalservice')
b4 = InlineKeyboardButton('Мой тариф',
                         callback_data='mytariff')
kbnewuser.add(b1,b2).add(b3).add(b4)


kbredactor=InlineKeyboardMarkup(row_width=2)
bp1=InlineKeyboardButton('Добавить намерение',
                          callback_data='createintention')
bp2=InlineKeyboardButton('Редактировать намерение',
                          callback_data='editintention')
bp3=InlineKeyboardButton('Удалить намерение',
                          callback_data='deleteintention')
kbredactor.add(bp1,bp2).add(bp3)


kbadmin=InlineKeyboardMarkup(row_width=2)
bp1=InlineKeyboardButton('Создать аккаунт',
                          callback_data='createaccount')
bp2=InlineKeyboardButton('Удалить аккаунт',
                          callback_data='deleteaccount')
kbadmin.add(bp1, bp2)

ikmytarif=InlineKeyboardMarkup(row_width=2)
ik1=InlineKeyboardButton('Мой тариф',
                          callback_data='mytariff')
ikmytarif.add(ik1)

ikservice=InlineKeyboardMarkup(row_width=2)
ik12=InlineKeyboardButton('Подключить услугу',
                          callback_data='selectadditionalservice')
ikservice.add(ik12)

iktarif=InlineKeyboardMarkup(row_width=2)
ik13=InlineKeyboardButton('Подключить тариф',
                          callback_data='selecttariff')
iktarif.add(ik13)
