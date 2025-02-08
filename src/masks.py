def get_mask_card_number(card_number: str) -> str:
    """
    Функция принимает номер карты в формате XXXX XXXX XXXX XXXX
    и возвращает его замаскированное значение XXXX XX** **** XXXX.
    """
    card_number = card_number.replace(" ", "")
    card_blocks = (
        card_number[:4],
        card_number[4:6] + "**",
        "****",
        card_number[-4:],
    )
    return " ".join(card_blocks)


def get_mask_account(account_number: str) -> str:
    """
    Функция принимает номер счета
    и возвращает его замаскированное значение **XXXX.
    """
    account_number = account_number.replace(" ", "")
    return f"**{account_number[-4:]}"
