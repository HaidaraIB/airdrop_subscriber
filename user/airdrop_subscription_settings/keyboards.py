from telegram import InlineKeyboardButton
from common.lang_dicts import BUTTONS
import models


def build_airdrop_subscription_settings_keyboard(lang: models.Language):
    keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["add_wallet_address"],
                callback_data=f"add_wallet_address",
            )
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["remove_wallet_address"],
                callback_data=f"remove_wallet_address",
            )
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["unsubscribe_from_airdrop"],
                callback_data=f"unsubscribe_from_airdrop",
            )
        ],
    ]
    return keyboard
