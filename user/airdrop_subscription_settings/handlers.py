from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
import sqlalchemy as sa
from common.keyboards import (
    build_back_to_home_page_button,
    build_back_button,
    build_keyboard,
    build_user_keyboard,
)
from common.lang_dicts import TEXTS, BUTTONS, get_lang
from custom_filters import PrivateChat
from common.back_to_home_page import back_to_user_home_page_handler
from user.airdrop_subscription_settings.keyboards import (
    build_airdrop_subscription_settings_keyboard,
)
from start import start_command
import models


# State constants
(
    AIRDROP,
    OPTION,
    NEW_WALLET_ADDRESS,
    WALLET_ADDRESS_TO_REMOVE,
    UNSUBSCRIBE_CONFIRMATION,
    REMOVE_LAST_WALLET_CONFIRMATION,
) = range(6)


async def airdrop_subscription_settings(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        with models.session_scope() as s:
            # Get all subscriptions and group by airdrop_id to get unique airdrops
            stmt = sa.select(
                sa.distinct(models.AirdropSubscription.airdrop_id)
            ).filter_by(user_id=update.effective_user.id)

            subscription_airdrop_ids = s.execute(stmt).scalars().all()

            if not subscription_airdrop_ids:
                await update.callback_query.answer(
                    text=TEXTS[lang]["no_airdrop_subscriptions"],
                    show_alert=True,
                )
                return ConversationHandler.END

            airdrops: list[models.Airdrop] = []
            for i in subscription_airdrop_ids:
                airdrop = s.get(models.Airdrop, i)
                airdrops.append(airdrop)

            subscriptions_summary = ""
            for airdrop in airdrops:
                subscriptions_summary += airdrop.stringify_for_user(
                    lang=lang, wallets_used=len(airdrop.subscriptions)
                )

            # Build keyboard with unique airdrops
            keyboard = build_keyboard(
                columns=1,
                texts=[airdrop.token_name for airdrop in airdrops],
                buttons_data=[str(i) for i in subscription_airdrop_ids],
            )

            keyboard.append(
                build_back_to_home_page_button(lang=lang, is_admin=False)[0]
            )
            await update.callback_query.edit_message_text(
                text=subscriptions_summary + TEXTS[lang]["choose_airdrop_to_manage"],
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        return AIRDROP


async def choose_airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)

        # Get airdrop_id from callback or context
        if not update.callback_query.data.startswith("back"):
            airdrop_id = int(update.callback_query.data)
            context.user_data["airdrop_id"] = airdrop_id
        else:
            airdrop_id = context.user_data["airdrop_id"]

        await update.callback_query.delete_message()

        with models.session_scope() as s:
            airdrop = s.get(models.Airdrop, airdrop_id)
            # Get all subscriptions for this airdrop and user
            subscriptions = (
                s.query(models.AirdropSubscription)
                .filter_by(user_id=update.effective_user.id, airdrop_id=airdrop_id)
                .all()
            )

            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=airdrop.photo,
                caption=(
                    airdrop.stringify(lang)
                    + "\n\n"
                    + TEXTS[lang]["airdrop_time_remaining"].format(
                        time_remaining=airdrop.calculate_time_remaining(lang)
                    )
                    + "\n\n"
                    + TEXTS[lang]["wallet_addresses_list"].format(
                        wallets_used=len(subscriptions)
                    )
                ),
            )
            # Build keyboard
            keyboard = build_airdrop_subscription_settings_keyboard(lang=lang)
            keyboard.append(build_back_button(data="back_to_choose_airdrop", lang=lang))
            keyboard.append(
                build_back_to_home_page_button(lang=lang, is_admin=False)[0]
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=TEXTS[lang]["choose_option"],
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        return OPTION


back_to_choose_airdrop = airdrop_subscription_settings


async def add_wallet_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        airdrop_id = context.user_data["airdrop_id"]

        with models.session_scope() as s:
            airdrop = s.get(models.Airdrop, airdrop_id)
            back_buttons = [
                build_back_button(data="back_to_add_wallet_address", lang=lang),
                build_back_to_home_page_button(lang=lang, is_admin=False)[0],
            ]
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["send_user_wallet_address"].format(
                    token_name=airdrop.token_name
                ),
                reply_markup=InlineKeyboardMarkup(back_buttons),
            )
        return NEW_WALLET_ADDRESS


back_to_add_wallet_address = choose_airdrop


async def get_new_wallet_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        airdrop_id = context.user_data["airdrop_id"]
        new_wallet_address = update.message.text.strip()

        with models.session_scope() as s:
            airdrop = s.get(models.Airdrop, airdrop_id)
            # Create new subscription with this wallet address
            s.add(
                models.AirdropSubscription(
                    airdrop_id=airdrop_id,
                    user_id=update.effective_user.id,
                    wallet_address=new_wallet_address,
                )
            )
            s.commit()

        await update.message.reply_text(
            text=TEXTS[lang]["wallet_address_added_success"],
            reply_markup=build_user_keyboard(lang=lang),
        )
        return ConversationHandler.END


async def remove_wallet_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        airdrop_id = context.user_data["airdrop_id"]

        with models.session_scope() as s:
            subscriptions = (
                s.query(models.AirdropSubscription)
                .filter_by(user_id=update.effective_user.id, airdrop_id=airdrop_id)
                .all()
            )
            keyboard = build_keyboard(
                columns=1,
                texts=[sub.wallet_address for sub in subscriptions],
                buttons_data=[str(sub.id) for sub in subscriptions],
            )

            keyboard.append(
                build_back_button(data="back_to_remove_wallet_address", lang=lang)
            )
            keyboard.append(
                build_back_to_home_page_button(lang=lang, is_admin=False)[0]
            )

            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["select_wallet_address_to_remove"],
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        return WALLET_ADDRESS_TO_REMOVE


back_to_remove_wallet_address = choose_airdrop


async def choose_wallet_address_to_remove(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        subscription_id = int(update.callback_query.data)

        with models.session_scope() as s:
            subscription = s.get(models.AirdropSubscription, subscription_id)

            # Check if this is the last wallet address
            remaining_subscriptions = (
                s.query(models.AirdropSubscription)
                .filter_by(
                    user_id=update.effective_user.id, airdrop_id=subscription.airdrop_id
                )
                .all()
            )

            if len(remaining_subscriptions) == 1:
                # Last wallet address, show confirmation
                airdrop = s.get(models.Airdrop, subscription.airdrop_id)
                context.user_data["subscription_id_to_remove"] = subscription_id
                keyboard = [
                    [
                        InlineKeyboardButton(
                            text=BUTTONS[lang]["confirm_button"],
                            callback_data="confirm_remove_last_wallet",
                        )
                    ],
                    build_back_button(data="back_to_remove_wallet_address", lang=lang),
                    build_back_to_home_page_button(lang=lang, is_admin=False)[0],
                ]
                await update.callback_query.edit_message_text(
                    text=TEXTS[lang]["remove_last_wallet_confirmation"].format(
                        wallet_address=subscription.wallet_address,
                        token_name=airdrop.token_name,
                    ),
                    reply_markup=InlineKeyboardMarkup(keyboard),
                )
                return REMOVE_LAST_WALLET_CONFIRMATION
            else:
                # Remove this subscription
                s.delete(subscription)
                s.commit()

                await update.callback_query.answer(
                    text=TEXTS[lang]["wallet_address_removed_success"],
                    show_alert=True,
                )

                # Get remaining subscriptions to build updated list
                remaining_subscriptions = (
                    s.query(models.AirdropSubscription)
                    .filter_by(
                        user_id=update.effective_user.id,
                        airdrop_id=subscription.airdrop_id,
                    )
                    .all()
                )

                # Build wallet addresses list
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=subscription.airdrop.photo,
                    caption=(
                        subscription.airdrop.stringify(lang)
                        + "\n\n"
                        + TEXTS[lang]["airdrop_time_remaining"].format(
                            time_remaining=subscription.airdrop.calculate_time_remaining(
                                lang
                            )
                        )
                        + "\n\n"
                        + TEXTS[lang]["wallet_addresses_list"].format(
                            wallets_used=len(remaining_subscriptions)
                        )
                    ),
                )
                # Build keyboard
                keyboard = build_airdrop_subscription_settings_keyboard(lang=lang)
                keyboard.append(
                    build_back_button(data="back_to_choose_airdrop", lang=lang)
                )
                keyboard.append(
                    build_back_to_home_page_button(lang=lang, is_admin=False)[0]
                )
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=TEXTS[lang]["choose_option"],
                    reply_markup=InlineKeyboardMarkup(keyboard),
                )
        return OPTION


async def unsubscribe_airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show confirmation before unsubscribing"""
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        airdrop_id = context.user_data["airdrop_id"]
        with models.session_scope() as s:
            airdrop = s.get(models.Airdrop, airdrop_id)
            keyboard = [
                [
                    InlineKeyboardButton(
                        text=BUTTONS[lang]["confirm_button"],
                        callback_data="confirm_unsubscribe",
                    )
                ],
                build_back_button(data="back_to_unsubscribe_airdrop", lang=lang),
                build_back_to_home_page_button(lang=lang, is_admin=False)[0],
            ]

            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["unsubscribe_confirmation"].format(
                    token_name=airdrop.token_name
                ),
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        return UNSUBSCRIBE_CONFIRMATION


back_to_unsubscribe_airdrop = choose_airdrop


async def confirm_unsubscribe_airdrop(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Actually unsubscribe from airdrop after confirmation"""
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        airdrop_id = context.user_data["airdrop_id"]
        with models.session_scope() as s:
            subscriptions = (
                s.query(models.AirdropSubscription)
                .filter_by(user_id=update.effective_user.id, airdrop_id=airdrop_id)
                .all()
            )

            for subscription in subscriptions:
                s.delete(subscription)
            s.commit()

        await update.callback_query.answer(
            text=TEXTS[lang]["unsubscribed_from_airdrop"],
            show_alert=True,
        )
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["home_page"],
            reply_markup=build_user_keyboard(lang=lang),
        )
        return ConversationHandler.END


async def confirm_remove_last_wallet(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    """Actually remove the last wallet address after confirmation"""
    if PrivateChat().filter(update):
        lang = get_lang(update.effective_user.id)
        subscription_id = context.user_data["subscription_id_to_remove"]

        with models.session_scope() as s:
            subscription = s.get(models.AirdropSubscription, subscription_id)
            airdrop_id = subscription.airdrop_id

            # Get all subscriptions for this airdrop and user
            subscriptions = (
                s.query(models.AirdropSubscription)
                .filter_by(user_id=update.effective_user.id, airdrop_id=airdrop_id)
                .all()
            )

            # Delete all subscriptions (unsubscribe completely)
            for sub in subscriptions:
                s.delete(sub)
            s.commit()

        await update.callback_query.answer(
            text=TEXTS[lang]["unsubscribed_from_airdrop"],
            show_alert=True,
        )
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["home_page"],
            reply_markup=build_user_keyboard(lang=lang),
        )
        return ConversationHandler.END


# Handler registrations
airdrop_subscription_settings_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            airdrop_subscription_settings,
            r"^airdrop_subscription_settings$",
        )
    ],
    states={
        AIRDROP: [
            CallbackQueryHandler(
                choose_airdrop,
                r"^[0-9]+$",
            ),
        ],
        OPTION: [
            CallbackQueryHandler(
                add_wallet_address,
                r"^add_wallet_address$",
            ),
            CallbackQueryHandler(
                remove_wallet_address,
                r"^remove_wallet_address$",
            ),
            CallbackQueryHandler(
                unsubscribe_airdrop,
                r"^unsubscribe_from_airdrop$",
            ),
        ],
        NEW_WALLET_ADDRESS: [
            MessageHandler(
                filters=(filters.TEXT & ~filters.COMMAND),
                callback=get_new_wallet_address,
            ),
        ],
        WALLET_ADDRESS_TO_REMOVE: [
            CallbackQueryHandler(
                choose_wallet_address_to_remove,
                r"^[0-9]+$",
            ),
        ],
        UNSUBSCRIBE_CONFIRMATION: [
            CallbackQueryHandler(
                confirm_unsubscribe_airdrop,
                r"^confirm_unsubscribe$",
            ),
        ],
        REMOVE_LAST_WALLET_CONFIRMATION: [
            CallbackQueryHandler(
                confirm_remove_last_wallet,
                r"^confirm_remove_last_wallet$",
            ),
        ],
    },
    fallbacks=[
        start_command,
        back_to_user_home_page_handler,
        CallbackQueryHandler(back_to_choose_airdrop, r"^back_to_choose_airdrop$"),
        CallbackQueryHandler(
            back_to_add_wallet_address, r"^back_to_add_wallet_address$"
        ),
        CallbackQueryHandler(
            back_to_remove_wallet_address, r"^back_to_remove_wallet_address$"
        ),
        CallbackQueryHandler(
            back_to_unsubscribe_airdrop, r"^back_to_unsubscribe_airdrop$"
        ),
    ],
    name="airdrop_subscription_settings_handler",
    persistent=True,
)
