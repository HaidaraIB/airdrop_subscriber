from telegram import Update, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from common.keyboards import (
    build_back_to_home_page_button,
    build_back_button,
    build_keyboard,
    build_user_keyboard,
)
from common.lang_dicts import TEXTS, get_lang
from custom_filters import PrivateChat
from user.airdrop_subscription_settings.keyboards import (
    build_airdrop_subscription_settings_keyboard,
)
from common.back_to_home_page import back_to_admin_home_page_handler
from start import start_command
import models


async def airdrop_subscription_settings(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        keyboard = build_airdrop_subscription_settings_keyboard(lang=lang)
        keyboard.append(build_back_to_home_page_button(lang=lang, is_admin=False)[0])
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["airdrop_subscription_settings"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return ConversationHandler.END


airdrop_subscription_settings_handler = CallbackQueryHandler(
    airdrop_subscription_settings,
    "^airdrop_subscription_settings$|^back_to_airdrop_subscription_settings$",
)


AIRDROP_SUBSCRIPTION, NEW_USER_WALLET_ADDRESS = range(2)


async def edit_user_wallet_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        with models.session_scope() as s:
            airdrop_subscriptions = (
                s.query(models.AirdropSubscription)
                .filter_by(user_id=update.effective_user.id)
                .all()
            )
            if not airdrop_subscriptions:
                await update.callback_query.answer(
                    text=TEXTS[lang]["no_airdrop_subscriptions"],
                    show_alert=True,
                )
                return ConversationHandler.END
            keyboard = build_keyboard(
                columns=1,
                texts=[
                    airdrop_subscription.airdrop.token_name
                    for airdrop_subscription in airdrop_subscriptions
                ],
                buttons_data=[
                    str(airdrop_subscription.id)
                    for airdrop_subscription in airdrop_subscriptions
                ],
            )
            keyboard.append(
                build_back_button(
                    data="back_to_airdrop_subscription_settings", lang=lang
                )
            )
            keyboard.append(
                build_back_to_home_page_button(lang=lang, is_admin=False)[0]
            )
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["choose_airdrop_subscription"],
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        return AIRDROP_SUBSCRIPTION


async def choose_airdrop_subscription(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        if not update.callback_query.data.startswith("back"):
            airdrop_subscription_id = int(update.callback_query.data)
            context.user_data["airdrop_subscription_id"] = airdrop_subscription_id
        else:
            airdrop_subscription_id = context.user_data["airdrop_subscription_id"]
        with models.session_scope() as s:
            airdrop_subscription = s.get(
                models.AirdropSubscription, airdrop_subscription_id
            )
            back_buttons = [
                build_back_button(
                    data="back_to_choose_airdrop_subscription", lang=lang
                ),
                build_back_to_home_page_button(lang=lang, is_admin=False)[0],
            ]
            await update.callback_query.edit_message_text(
                text=(
                    TEXTS[lang]["send_user_wallet_address"].format(
                        token_name=airdrop_subscription.airdrop.token_name,
                    )
                    + "\n\n"
                    + TEXTS[lang]["current_wallet_address"].format(
                        wallet_address=airdrop_subscription.wallet_address
                    )
                ),
                reply_markup=InlineKeyboardMarkup(back_buttons),
            )
        return NEW_USER_WALLET_ADDRESS


back_to_choose_airdrop_subscription = edit_user_wallet_address


async def new_user_wallet_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        airdrop_subscription_id = context.user_data["airdrop_subscription_id"]
        new_user_wallet_address = update.message.text
        with models.session_scope() as s:
            airdrop_subscription = s.get(
                models.AirdropSubscription, airdrop_subscription_id
            )
            if airdrop_subscription.airdrop.token_name not in new_user_wallet_address:
                await update.message.reply_text(
                    text=TEXTS[lang]["wrong_address"].format(
                        token_name=airdrop_subscription.airdrop.token_name
                    )
                )
                return
            airdrop_subscription.wallet_address = new_user_wallet_address
            s.commit()
        await update.message.reply_text(
            text=TEXTS[lang]["user_wallet_address_updated"],
            reply_markup=build_user_keyboard(
                lang=lang
            ),
        )
        return ConversationHandler.END


edit_user_wallet_address_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            edit_user_wallet_address,
            "^edit_user_wallet_address$",
        )
    ],
    states={
        AIRDROP_SUBSCRIPTION: [
            CallbackQueryHandler(
                choose_airdrop_subscription,
                r"^[0-9]+$",
            )
        ],
        NEW_USER_WALLET_ADDRESS: [
            MessageHandler(
                filters=(filters.TEXT & ~filters.COMMAND),
                callback=new_user_wallet_address,
            )
        ],
    },
    fallbacks=[
        start_command,
        back_to_admin_home_page_handler,
        airdrop_subscription_settings_handler,
        CallbackQueryHandler(
            back_to_choose_airdrop_subscription,
            "^back_to_choose_airdrop_subscription$",
        ),
    ],
    name="edit_user_wallet_address_handler",
    persistent=True,
)


AIRDROP_SUBSCRIPTION_TO_UNSUBSCRIBE = range(1)


async def unsubscribe_from_airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        with models.session_scope() as s:
            airdrop_subscriptions = (
                s.query(models.AirdropSubscription)
                .filter_by(user_id=update.effective_user.id)
                .all()
            )
            if not airdrop_subscriptions:
                await update.callback_query.answer(
                    text=TEXTS[lang]["no_airdrop_subscriptions"],
                    show_alert=True,
                )
                return ConversationHandler.END
            keyboard = build_keyboard(
                columns=1,
                texts=[
                    airdrop_subscription.airdrop.token_name
                    for airdrop_subscription in airdrop_subscriptions
                ],
                buttons_data=[
                    str(airdrop_subscription.id)
                    for airdrop_subscription in airdrop_subscriptions
                ],
            )
            keyboard.append(
                build_back_button(
                    data="back_to_airdrop_subscription_settings", lang=lang
                )
            )
            keyboard.append(
                build_back_to_home_page_button(lang=lang, is_admin=False)[0]
            )
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["unsubscribe_from_airdrop"],
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        return AIRDROP_SUBSCRIPTION_TO_UNSUBSCRIBE


async def choose_airdrop_subscription_to_unsubscribe(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        airdrop_subscription_id = int(update.callback_query.data)
        with models.session_scope() as s:
            airdrop_subscription = s.get(
                models.AirdropSubscription, airdrop_subscription_id
            )
            s.delete(airdrop_subscription)
            s.commit()
        await update.callback_query.answer(
            text=TEXTS[lang]["unsubscribed_from_airdrop"],
            show_alert=True,
        )
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["home_page"],
            reply_markup=build_user_keyboard(
                lang=lang
            ),
        )
        return ConversationHandler.END


unsubscribe_from_airdrop_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            unsubscribe_from_airdrop,
            "^unsubscribe_from_airdrop$",
        )
    ],
    states={
        AIRDROP_SUBSCRIPTION_TO_UNSUBSCRIBE: [
            CallbackQueryHandler(
                choose_airdrop_subscription_to_unsubscribe,
                r"^[0-9]+$",
            )
        ],
    },
    fallbacks=[
        start_command,
        back_to_admin_home_page_handler,
        airdrop_subscription_settings_handler,
    ],
    name="unsubscribe_from_airdrop_handler",
    persistent=True,
)


AIRDROP_SUBSCRIPTION_TO_SHOW = range(1)


async def show_airdrop_subscriptions(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        with models.session_scope() as s:
            airdrop_subscriptions = (
                s.query(models.AirdropSubscription)
                .filter_by(user_id=update.effective_user.id)
                .all()
            )
            if not airdrop_subscriptions:
                await update.callback_query.answer(
                    text=TEXTS[lang]["no_airdrop_subscriptions"],
                    show_alert=True,
                )
                return ConversationHandler.END
            keyboard = build_keyboard(
                columns=1,
                texts=[
                    airdrop_subscription.airdrop.token_name
                    for airdrop_subscription in airdrop_subscriptions
                ],
            )
            keyboard.append(
                build_back_button(
                    data="back_to_airdrop_subscription_settings", lang=lang
                )
            )
            keyboard.append(
                build_back_to_home_page_button(lang=lang, is_admin=False)[0]
            )
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["show_airdrop_subscriptions"],
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        return AIRDROP_SUBSCRIPTION_TO_SHOW


async def choose_airdrop_subscription_to_show(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        airdrop_subscription_id = int(update.callback_query.data)
        with models.session_scope() as s:
            airdrop_subscription = s.get(
                models.AirdropSubscription, airdrop_subscription_id
            )
            await update.callback_query.delete_message()
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=airdrop_subscription.airdrop.photo,
                caption=(
                    str(airdrop_subscription)
                    + "\n"
                    + TEXTS[lang]["airdrop_time_remaining"].format(
                        time_remaining=airdrop_subscription.airdrop.calculate_time_remaining(
                            lang
                        )
                    )
                    + "\n\n"
                    + TEXTS[lang]["continue_with_start_command"]
                ),
            )
        return ConversationHandler.END


show_airdrop_subscriptions_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            show_airdrop_subscriptions,
            "^show_airdrop_subscriptions$",
        )
    ],
    states={
        AIRDROP_SUBSCRIPTION_TO_SHOW: [
            CallbackQueryHandler(
                choose_airdrop_subscription_to_show,
                r"^[0-9]+$",
            )
        ],
    },
    fallbacks=[
        start_command,
        back_to_admin_home_page_handler,
        airdrop_subscription_settings_handler,
    ],
    name="show_airdrop_subscriptions_handler",
    persistent=True,
)
