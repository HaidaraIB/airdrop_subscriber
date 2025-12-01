from telegram import InlineKeyboardButton
from common.lang_dicts import BUTTONS
import models


def build_airdrop_subscription_settings_keyboard(lang: models.Language):
    keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["edit_user_wallet_address"],
                callback_data="edit_user_wallet_address",
            ),
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["unsubscribe_from_airdrop"],
                callback_data="unsubscribe_from_airdrop",
            ),
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["show_airdrop_subscriptions"],
                callback_data="show_airdrop_subscriptions",
            ),
        ],
    ]
    return keyboard
