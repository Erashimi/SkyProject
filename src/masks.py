import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номера вида *7197 в формат **** **** **** 7197."""
    digits = "".join([c for c in card_number if c.isdigit()])[-4:]
    if len(digits) != 4:
        return "Некорректный номер"
    return f"**** **** **** {digits}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер счета"""
    try:
        account_number = account_number.replace(" ", "")
        masked_account = f"**{account_number[-4:]}"
        logger.info(f"Успешное маскирование счета: {masked_account}")
        return masked_account
    except Exception as e:
        logger.error(f"Ошибка маскирования счета: {e}", exc_info=True)
        raise
