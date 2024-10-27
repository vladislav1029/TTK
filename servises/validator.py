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


def validate_password(password: str) -> str:
    """
    Валидация пароля. Пароль должен содержать:
    - хотя бы одну цифру
    - хотя бы одну букву верхнего регистра
    - хотя бы одну букву нижнего регистра
    - хотя бы один специальный символ
    - минимальную длину 8 символов

    :param password: Строка для валидации
    :return: Сообщение об ошибке или "Пароль успешно проверен!", если валидация прошла успешно
    """
    min_length = 8
    password_pattern = re.compile(
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )
    if len(password) < min_length:
        return "Пароль слишком короткий. Минимальная длина — 8 символов."
    if not password_pattern.match(password):
        return "Пароль должен содержать хотя бы одну цифру, одну букву верхнего и нижнего регистра, а также один специальный символ."
    return "Пароль успешно проверен!"


def validate_email(email: str) -> str:
    """
    Валидация email. Email должен соответствовать стандартному формату.

    :param email: Строка для валидации
    :return: Сообщение об ошибке или "Email успешно проверен!", если валидация прошла успешно
    """
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if re.match(email_pattern, email):
        return "Email успешно проверен!"
    else:
        return "Неверный формат email. Пожалуйста, попробуйте снова."
