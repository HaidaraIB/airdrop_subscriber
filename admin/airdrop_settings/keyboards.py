from telegram import InlineKeyboardButton
from common.lang_dicts import BUTTONS
import models


def build_airdrop_settings_keyboard(lang: models.Language = models.Language.ARABIC):
    keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["add_airdrop"],
                callback_data="add_airdrop",
            ),
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["edit_airdrop"],
                callback_data="edit_airdrop",
            ),
            InlineKeyboardButton(
                text=BUTTONS[lang]["remove_airdrop"],
                callback_data="remove_airdrop",
            ),
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["show_airdrop"],
                callback_data="show_airdrop",
            ),
        ],
    ]
    return keyboard


def build_edit_airdrop_fields_keyboard(lang: models.Language = models.Language.ARABIC):
    keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["edit_airdrop_contract_address"],
                callback_data="edit_airdrop_contract_address",
            ),
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["edit_airdrop_token_name"],
                callback_data="edit_airdrop_token_name",
            ),
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["edit_airdrop_amount"],
                callback_data="edit_airdrop_amount",
            ),
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["edit_airdrop_distribution_date"],
                callback_data="edit_airdrop_distribution_date",
            ),
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS[lang]["edit_airdrop_photo"],
                callback_data="edit_airdrop_photo",
            ),
        ],
    ]
    return keyboard
