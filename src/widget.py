from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(data: str) -> str:
    """
    Функция принимает строку, содержащую тип и номер карты или счета
    и возвращает строку с замаскированным номером.
    """
    try:
        name, number = data.rsplit(" ", maxsplit=1)
    except ValueError:
        raise ValueError(f"Некорректный формат данных: '{data}'")

    if name == "Счет":
        return f"{name} {get_mask_account(number)}"
    else:
        return f"{name} {get_mask_card_number(number)}"


def get_date(date_str: str) -> str:
    """
    Преобразует строку даты в формат "ДД.ММ.ГГГГ".
    """
    try:
        year = date_str[:4]
        month = date_str[5:7]
        day = date_str[8:10]

        result = f"{day}.{month}.{year}"
        return result
    except IndexError as e:
        raise ValueError(f"Невозможно преобразовать дату: {date_str}") from e
