from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
import sqlalchemy as sa
from custom_filters import PrivateChat
from common.lang_dicts import TEXTS, BUTTONS, get_lang
from common.keyboards import build_back_button, build_back_to_home_page_button
from common.back_to_home_page import back_to_user_home_page_handler
import models
from start import start_command


SEARCH_QUERY, USER_WALLET_ADDRESS, SUBSCRIBE_TO_AIRDROP = range(3)


async def check_airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["check_airdrop_instruction"],
            reply_markup=InlineKeyboardMarkup(
                build_back_to_home_page_button(lang=lang, is_admin=False)
            ),
        )
        return SEARCH_QUERY


async def get_search_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        if update.message:
            search_query = update.message.text
            context.user_data["search_query"] = search_query
        else:
            search_query = context.user_data["search_query"]

        with models.session_scope() as s:
            airdrop = (
                s.query(models.Airdrop)
                .filter(
                    sa.or_(
                        models.Airdrop.contract_address == search_query,
                        models.Airdrop.token_name == search_query,
                        models.Airdrop.token_code == search_query,
                    )
                )
                .first()
            )
            if not airdrop:
                await update.message.reply_text(text=TEXTS[lang]["airdrop_not_found"])
                return
            context.user_data["airdrop_id"] = airdrop.id
            keyboard = [
                [
                    InlineKeyboardButton(
                        text=BUTTONS[lang]["subscribe_to_airdrop"],
                        callback_data="subscribe_to_airdrop",
                    )
                ],
                build_back_button("back_to_get_search_query", lang=lang),
                build_back_to_home_page_button(lang=lang, is_admin=False)[0],
            ]
            await update.message.reply_photo(
                photo=airdrop.photo,
                caption=(
                    TEXTS[lang]["airdrop_found"]
                    + airdrop.stringify(lang)
                    + "\n\n"
                    + TEXTS[lang]["airdrop_time_remaining"].format(
                        time_remaining=airdrop.calculate_time_remaining(lang)
                    )
                ),
            )
            await update.message.reply_text(
                text=TEXTS[lang]["subscribe_to_airdrop"].format(
                    token_name=airdrop.token_name
                ),
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        return SUBSCRIBE_TO_AIRDROP


back_to_get_search_query = check_airdrop


async def subscribe_to_airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        airdrop_id = context.user_data["airdrop_id"]
        with models.session_scope() as s:
            airdrop = s.get(models.Airdrop, airdrop_id)
            back_buttons = [
                build_back_button("back_to_subscribe_to_airdrop", lang=lang),
                build_back_to_home_page_button(lang=lang, is_admin=False)[0],
            ]
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["send_user_wallet_address"].format(
                    token_name=airdrop.token_name
                ),
                reply_markup=InlineKeyboardMarkup(back_buttons),
            )
        return USER_WALLET_ADDRESS


back_to_subscribe_to_airdrop = get_search_query


async def get_user_wallet_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        airdrop_id = context.user_data["airdrop_id"]
        user_wallet_address = update.message.text.strip()
        with models.session_scope() as s:
            airdrop = s.get(models.Airdrop, airdrop_id)
            s.add(
                models.AirdropSubscription(
                    airdrop_id=airdrop_id,
                    user_id=update.effective_user.id,
                    wallet_address=user_wallet_address,
                )
            )
            s.commit()
            await update.message.reply_text(
                text=(
                    TEXTS[lang]["subscription_success"].format(
                        token_name=airdrop.token_name
                    )
                    + "\n\n"
                    + TEXTS[lang]["airdrop_time_remaining"].format(
                        time_remaining=airdrop.calculate_time_remaining(lang)
                    )
                    + "\n\n"
                    + TEXTS[lang]["continue_with_start_command"]
                ),
            )
        return ConversationHandler.END


check_airdrop_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            check_airdrop,
            "^check_airdrop$",
        )
    ],
    states={
        SEARCH_QUERY: [
            MessageHandler(
                filters=(filters.TEXT & ~filters.COMMAND),
                callback=get_search_query,
            )
        ],
        SUBSCRIBE_TO_AIRDROP: [
            CallbackQueryHandler(
                subscribe_to_airdrop,
                "^subscribe_to_airdrop$",
            )
        ],
        USER_WALLET_ADDRESS: [
            MessageHandler(
                filters=(filters.TEXT & ~filters.COMMAND),
                callback=get_user_wallet_address,
            )
        ],
    },
    fallbacks=[
        start_command,
        back_to_user_home_page_handler,
        CallbackQueryHandler(back_to_get_search_query, "^back_to_get_search_query$"),
        CallbackQueryHandler(
            back_to_subscribe_to_airdrop, "^back_to_subscribe_to_airdrop$"
        ),
    ],
    name="check_airdrop_handler",
    persistent=True,
)
