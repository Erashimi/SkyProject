import logging
import os

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер карты"""
    try:
        card_number = card_number.replace(" ", "")
        card_blocks = (
            card_number[:4],
            card_number[4:6] + "**",
            "****",
            card_number[-4:],
        )
        masked_number = " ".join(card_blocks)
        logger.info(f"Успешное маскирование карты: {masked_number}")
        return masked_number
    except Exception as e:
        logger.error(f"Ошибка маскирования карты: {e}", exc_info=True)
        raise

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
