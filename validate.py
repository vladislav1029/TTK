import re
def validate_contract_number(contract_number: str, len_number: int = 9) -> bool:
    """
    Валидация номера договора. Длина сообщения должна составлять 9 символов,
    и все символы должны быть цифрами от 0 до 9.

    :param contract_number: Строка для валидации
    :return: True, если валидация прошла успешно, иначе False
    """
    # Проверяем, что длина сообщения составляет 9 символов
    if len(contract_number) != len_number:
        return False
    # Проверяем, что все символы являются цифрами от 0 до 9
    if not contract_number.isdigit():
        return False
    return True


def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None
def validate_phone_number(phone_number):
    pattern = r'^\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
    return re.match(pattern, phone_number) is not None
