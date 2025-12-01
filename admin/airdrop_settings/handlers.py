from telegram import Update, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from admin.airdrop_settings.keyboards import (
    build_airdrop_settings_keyboard,
    build_edit_airdrop_fields_keyboard,
)
from common.back_to_home_page import back_to_admin_home_page_handler
from common.keyboards import (
    build_admin_keyboard,
    build_back_to_home_page_button,
    build_back_button,
    build_keyboard,
)
from common.lang_dicts import TEXTS, get_lang
from custom_filters import PrivateChatAndAdmin
from start import admin_command
from datetime import datetime
from Config import Config
import models


async def airdrop_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        lang = get_lang(update.effective_user.id)
        keyboard = build_airdrop_settings_keyboard(lang)
        keyboard.append(build_back_to_home_page_button(lang=lang, is_admin=True)[0])
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["airdrop_settings_title"],
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
        return ConversationHandler.END


airdrop_settings_handler = CallbackQueryHandler(
    airdrop_settings,
    "^airdrop_settings$|^back_to_airdrop_settings$",
)


# Add Airdrop Conversation States
CONTRACT_ADDRESS, TOKEN_NAME, TOKEN_CODE, AMOUNT, DISTRIBUTION_DATE, PHOTO = range(6)


async def add_airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        lang = get_lang(update.effective_user.id)
        back_buttons = [
            build_back_button("back_to_airdrop_settings", lang=lang),
            build_back_to_home_page_button(lang=lang, is_admin=True)[0],
        ]
        await update.callback_query.edit_message_text(
            text=TEXTS[lang]["add_airdrop_instruction"],
            reply_markup=InlineKeyboardMarkup(back_buttons),
        )
        return CONTRACT_ADDRESS


async def get_contract_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        lang = get_lang(update.effective_user.id)
        back_buttons = [
            build_back_button("back_to_get_contract_address", lang=lang),
            build_back_to_home_page_button(lang=lang, is_admin=True)[0],
        ]
        if update.message:
            contract_address = update.message.text.strip()
            context.user_data["airdrop_contract_address"] = contract_address
            await update.message.reply_text(
                text=TEXTS[lang]["send_token_name"],
                reply_markup=InlineKeyboardMarkup(back_buttons),
            )
        else:
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["send_token_name"],
                reply_markup=InlineKeyboardMarkup(back_buttons),
            )
        return TOKEN_NAME


back_to_get_contract_address = add_airdrop


async def get_token_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        lang = get_lang(update.effective_user.id)
        back_buttons = [
            build_back_button("back_to_get_token_name", lang=lang),
            build_back_to_home_page_button(lang=lang, is_admin=True)[0],
        ]
        if update.message:
            token_name = update.message.text.strip()
            context.user_data["airdrop_token_name"] = token_name
            await update.message.reply_text(
                text=TEXTS[lang]["send_amount"],
                reply_markup=InlineKeyboardMarkup(back_buttons),
            )
        else:
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["send_amount"],
                reply_markup=InlineKeyboardMarkup(back_buttons),
            )
        return TOKEN_CODE


back_to_get_token_name = get_contract_address


async def get_token_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        lang = get_lang(update.effective_user.id)
        back_buttons = [
            build_back_button("back_to_get_token_code", lang=lang),
            build_back_to_home_page_button(lang=lang, is_admin=True)[0],
        ]
        if update.message:
            token_code = update.message.text.strip()
            context.user_data["token_code"] = token_code
            await update.message.reply_text(
                text=TEXTS[lang]["send_token_code"],
                reply_markup=InlineKeyboardMarkup(back_buttons),
            )
        else:
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["send_token_code"],
                reply_markup=InlineKeyboardMarkup(back_buttons),
            )
        return AMOUNT


back_to_get_token_code = get_token_name


async def get_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        lang = get_lang(update.effective_user.id)
        back_buttons = [
            build_back_button("back_to_get_amount", lang=lang),
            build_back_to_home_page_button(lang=lang, is_admin=True)[0],
        ]
        if update.message:
            amount = int(update.message.text.strip())
            context.user_data["airdrop_amount"] = amount
            await update.message.reply_text(
                text=TEXTS[lang]["send_distribution_date"],
                reply_markup=InlineKeyboardMarkup(back_buttons),
            )
        else:
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["send_distribution_date"],
                reply_markup=InlineKeyboardMarkup(back_buttons),
            )
        return DISTRIBUTION_DATE


back_to_get_amount = get_token_code


async def get_distribution_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        lang = get_lang(update.effective_user.id)
        back_buttons = [
            build_back_button("back_to_get_distribution_date", lang=lang),
            build_back_to_home_page_button(lang=lang, is_admin=True)[0],
        ]
        if update.message:
            date_str = update.message.text.strip()
            distribution_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            if distribution_date < datetime.now():
                await update.message.reply_text(
                    text=TEXTS[lang]["distribution_date_in_the_past"]
                )
                return
            context.user_data["airdrop_distribution_date"] = distribution_date
            await update.message.reply_text(
                text=TEXTS[lang]["send_photo"],
                reply_markup=InlineKeyboardMarkup(back_buttons),
            )
        else:
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["send_photo"],
                reply_markup=InlineKeyboardMarkup(back_buttons),
            )
        return PHOTO


back_to_get_distribution_date = get_amount


async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        lang = get_lang(update.effective_user.id)

        photo_message = await context.bot.send_photo(
            chat_id=Config.PHOTOS_CHANNEL,
            photo=update.message.photo[-1],
            caption=update.message.caption,
        )
        airdrop_photo = photo_message.photo[-1].file_id

        # Create the airdrop
        with models.session_scope() as s:
            new_airdrop = models.Airdrop(
                contract_address=context.user_data["airdrop_contract_address"],
                token_name=context.user_data["airdrop_token_name"],
                amount=context.user_data["airdrop_amount"],
                distribution_date=context.user_data["airdrop_distribution_date"],
                photo=airdrop_photo,
            )
            s.add(new_airdrop)
            s.commit()

        await update.message.reply_text(
            text=TEXTS[lang]["airdrop_added_success"],
            reply_markup=build_admin_keyboard(lang, update.effective_user.id),
        )
        return ConversationHandler.END


add_airdrop_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=add_airdrop,
            pattern="^add_airdrop$",
        ),
    ],
    states={
        CONTRACT_ADDRESS: [
            MessageHandler(
                filters=filters.TEXT & ~filters.COMMAND,
                callback=get_contract_address,
            ),
        ],
        TOKEN_NAME: [
            MessageHandler(
                filters=filters.TEXT & ~filters.COMMAND,
                callback=get_token_name,
            ),
        ],
        TOKEN_CODE: [
            MessageHandler(
                filters=filters.TEXT & ~filters.COMMAND,
                callback=get_token_code,
            ),
        ],
        AMOUNT: [
            MessageHandler(
                filters=filters.TEXT & filters.Regex("^[0-9]+$"),
                callback=get_amount,
            ),
        ],
        DISTRIBUTION_DATE: [
            MessageHandler(
                filters=filters.TEXT
                & filters.Regex(
                    "^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$"
                ),
                callback=get_distribution_date,
            ),
        ],
        PHOTO: [
            MessageHandler(
                filters=filters.PHOTO,
                callback=get_photo,
            ),
        ],
    },
    fallbacks=[
        airdrop_settings_handler,
        admin_command,
        back_to_admin_home_page_handler,
        CallbackQueryHandler(
            back_to_get_contract_address, "^back_to_get_contract_address$"
        ),
        CallbackQueryHandler(back_to_get_token_name, "^back_to_get_token_name$"),
        CallbackQueryHandler(back_to_get_token_code, "^back_to_get_token_code$"),
        CallbackQueryHandler(back_to_get_amount, "^back_to_get_amount$"),
        CallbackQueryHandler(
            back_to_get_distribution_date, "^back_to_get_distribution_date$"
        ),
    ],
)


# Remove Airdrop
CHOOSE_AIRDROP_TO_REMOVE = range(1)


async def remove_airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        lang = get_lang(update.effective_user.id)
        with models.session_scope() as s:
            if update.callback_query.data.isnumeric():
                airdrop = s.get(models.Airdrop, int(update.callback_query.data))
                if airdrop:
                    s.delete(airdrop)
                    s.commit()
                    await update.callback_query.answer(
                        text=TEXTS[lang]["airdrop_removed_success"],
                        show_alert=True,
                    )

            airdrops = s.query(models.Airdrop).all()

            if not airdrops:
                await update.callback_query.answer(
                    text=TEXTS[lang]["no_airdrops"],
                    show_alert=True,
                )
                if update.callback_query.data.isnumeric():
                    await update.callback_query.edit_message_text(
                        text=TEXTS[lang]["home_page"],
                        reply_markup=build_admin_keyboard(
                            lang=lang, user_id=update.effective_user.id
                        ),
                    )
                return ConversationHandler.END

            airdrop_keyboard = build_keyboard(
                columns=1,
                texts=[airdrop.token_name for airdrop in airdrops],
                buttons_data=[str(airdrop.id) for airdrop in airdrops],
            )
            airdrop_keyboard.append(
                build_back_button("back_to_airdrop_settings", lang=lang)
            )
            airdrop_keyboard.append(
                build_back_to_home_page_button(lang=lang, is_admin=True)[0]
            )
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["remove_airdrop_instruction"],
                reply_markup=InlineKeyboardMarkup(airdrop_keyboard),
            )
        return CHOOSE_AIRDROP_TO_REMOVE


remove_airdrop_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=remove_airdrop,
            pattern="^remove_airdrop$",
        ),
    ],
    states={
        CHOOSE_AIRDROP_TO_REMOVE: [
            CallbackQueryHandler(
                remove_airdrop,
                "^[0-9]+$",
            ),
        ]
    },
    fallbacks=[
        airdrop_settings_handler,
        admin_command,
        back_to_admin_home_page_handler,
    ],
)


# Show Airdrop
AIRDROP_TO_SHOW = range(1)


async def show_airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        lang = get_lang(update.effective_user.id)
        with models.session_scope() as s:
            airdrops = s.query(models.Airdrop).all()
            if not airdrops:
                await update.callback_query.answer(
                    text=TEXTS[lang]["no_airdrops"],
                    show_alert=True,
                )
                return ConversationHandler.END

            airdrop_keyboard = build_keyboard(
                columns=1,
                texts=[airdrop.token_name for airdrop in airdrops],
                buttons_data=[str(airdrop.id) for airdrop in airdrops],
            )
            airdrop_keyboard.append(
                build_back_button("back_to_airdrop_settings", lang=lang)
            )
            airdrop_keyboard.append(
                build_back_to_home_page_button(lang=lang, is_admin=True)[0]
            )
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["show_airdrop_instruction"],
                reply_markup=InlineKeyboardMarkup(airdrop_keyboard),
            )
        return AIRDROP_TO_SHOW


async def choose_airdrop_to_show(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        lang = get_lang(update.effective_user.id)
        airdrop_id = int(update.callback_query.data)
        with models.session_scope() as s:
            airdrop = s.get(models.Airdrop, airdrop_id)
            await update.callback_query.delete_message()
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=airdrop.photo,
                caption=(
                    str(airdrop)
                    + "\n\n"
                    + TEXTS[lang]["airdrop_time_remaining"].format(
                        time_remaining=airdrop.calculate_time_remaining(lang)
                    )
                    + "\n\n"
                    + TEXTS[lang]["continue_with_admin_command"]
                ),
            )
        return ConversationHandler.END


show_airdrop_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=show_airdrop,
            pattern="^show_airdrop$",
        ),
    ],
    states={
        AIRDROP_TO_SHOW: [
            CallbackQueryHandler(
                choose_airdrop_to_show,
                r"^[0-9]+$",
            ),
        ],
    },
    fallbacks=[
        airdrop_settings_handler,
        admin_command,
        back_to_admin_home_page_handler,
    ],
)


# Edit Airdrop
CHOOSE_AIRDROP_TO_EDIT, CHOOSE_FIELD_TO_EDIT, NEW_VALUE = range(3)


async def edit_airdrop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        lang = get_lang(update.effective_user.id)
        with models.session_scope() as s:
            airdrops = s.query(models.Airdrop).all()
            if not airdrops:
                await update.callback_query.answer(
                    text=TEXTS[lang]["no_airdrops"],
                    show_alert=True,
                )
                return
            airdrop_keyboard = build_keyboard(
                columns=1,
                texts=[airdrop.token_name for airdrop in airdrops],
                buttons_data=[str(airdrop.id) for airdrop in airdrops],
            )
            airdrop_keyboard.append(
                build_back_button("back_to_airdrop_settings", lang=lang)
            )
            airdrop_keyboard.append(
                build_back_to_home_page_button(lang=lang, is_admin=True)[0]
            )
            await update.callback_query.edit_message_text(
                text=TEXTS[lang]["edit_airdrop_instruction"],
                reply_markup=InlineKeyboardMarkup(airdrop_keyboard),
            )
        return CHOOSE_AIRDROP_TO_EDIT


async def choose_airdrop_to_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        lang = get_lang(update.effective_user.id)
        if not update.callback_query.data.startswith("back"):
            airdrop_id = int(update.callback_query.data)
            context.user_data["edit_airdrop_id"] = airdrop_id
        else:
            airdrop_id = context.user_data["edit_airdrop_id"]
        with models.session_scope() as s:
            airdrop = s.get(models.Airdrop, airdrop_id)
            keyboard = build_edit_airdrop_fields_keyboard(lang)
            keyboard.append(
                build_back_button("back_to_choose_airdrop_to_edit", lang=lang)
            )
            keyboard.append(build_back_to_home_page_button(lang=lang, is_admin=True)[0])
            await update.callback_query.delete_message()
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=airdrop.photo,
                caption=(
                    str(airdrop)
                    + "\n\n"
                    + TEXTS[lang]["airdrop_time_remaining"].format(
                        time_remaining=airdrop.calculate_time_remaining(lang)
                    )
                ),
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=TEXTS[lang]["choose_field_to_edit"],
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
        return CHOOSE_FIELD_TO_EDIT


back_to_choose_airdrop_to_edit = edit_airdrop


async def choose_field_to_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        lang = get_lang(update.effective_user.id)
        if not update.callback_query.data.startswith("back"):
            field = update.callback_query.data
            context.user_data["edit_airdrop_field"] = field
        else:
            field = context.user_data["edit_airdrop_field"]
        if field == "edit_airdrop_contract_address":
            text = TEXTS[lang]["send_contract_address"]
        elif field == "edit_airdrop_token_name":
            text = TEXTS[lang]["send_token_name"]
        elif field == "edit_airdrop_token_code":
            text = TEXTS[lang]["send_token_code"]
        elif field == "edit_airdrop_amount":
            text = TEXTS[lang]["send_amount"]
        elif field == "edit_airdrop_distribution_date":
            text = TEXTS[lang]["send_distribution_date"]
        elif field == "edit_airdrop_photo":
            text = TEXTS[lang]["send_photo"]
        else:
            return CHOOSE_FIELD_TO_EDIT

        back_buttons = [
            build_back_button("back_to_choose_field_to_edit", lang=lang),
            build_back_to_home_page_button(lang=lang, is_admin=True)[0],
        ]
        await update.callback_query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(back_buttons),
        )
        return NEW_VALUE


back_to_choose_field_to_edit = choose_airdrop_to_edit


async def get_new_value(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        lang = get_lang(update.effective_user.id)
        field = context.user_data.get("edit_airdrop_field")
        airdrop_id = context.user_data.get("edit_airdrop_id")

        with models.session_scope() as s:
            airdrop = s.get(models.Airdrop, airdrop_id)
            if field == "edit_airdrop_contract_address":
                airdrop.contract_address = update.message.text.strip()
            elif field == "edit_airdrop_token_name":
                airdrop.token_name = update.message.text.strip()
            elif field == "edit_airdrop_token_code":
                airdrop.token_code = update.message.text.strip()
            elif field == "edit_airdrop_amount":
                try:
                    airdrop.amount = int(update.message.text.strip())
                except ValueError:
                    await update.message.reply_text(text=TEXTS[lang]["invalid_amount"])
                    return
            elif field == "edit_airdrop_distribution_date":
                try:
                    date_str = update.message.text.strip()
                    airdrop.distribution_date = datetime.strptime(
                        date_str, "%Y-%m-%d %H:%M:%S"
                    )
                except ValueError:
                    await update.message.reply_text(text=TEXTS[lang]["invalid_date"])
                    return
            elif field == "edit_airdrop_photo":
                if update.message.photo:
                    photo_message = await context.bot.send_photo(
                        chat_id=Config.PHOTOS_CHANNEL,
                        photo=update.message.photo[-1],
                        caption=update.message.caption,
                    )
                    airdrop.photo = photo_message.photo[-1].file_id
            s.commit()

        await update.message.reply_text(
            text=TEXTS[lang]["airdrop_updated_success"],
            reply_markup=build_admin_keyboard(lang, update.effective_user.id),
        )
        return ConversationHandler.END


edit_airdrop_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(
            callback=edit_airdrop,
            pattern="^edit_airdrop$",
        ),
    ],
    states={
        CHOOSE_AIRDROP_TO_EDIT: [
            CallbackQueryHandler(
                choose_airdrop_to_edit,
                "^\d+$",
            ),
        ],
        CHOOSE_FIELD_TO_EDIT: [
            CallbackQueryHandler(
                choose_field_to_edit,
                "^edit_airdrop_(contract_address|token_name|token_code|amount|distribution_date|photo)$",
            ),
        ],
        NEW_VALUE: [
            MessageHandler(
                filters=(filters.TEXT & ~filters.COMMAND) | filters.PHOTO,
                callback=get_new_value,
            ),
        ],
    },
    fallbacks=[
        airdrop_settings_handler,
        admin_command,
        back_to_admin_home_page_handler,
        CallbackQueryHandler(
            back_to_choose_airdrop_to_edit, "^back_to_choose_airdrop_to_edit$"
        ),
        CallbackQueryHandler(
            back_to_choose_field_to_edit, "^back_to_choose_field_to_edit$"
        ),
    ],
)
