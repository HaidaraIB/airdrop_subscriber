from telegram import Update, BotCommandScopeChat, Bot
from telegram.ext import CommandHandler, ContextTypes, Application, ConversationHandler
from common.decorators import is_user_banned, add_new_user, is_user_member
from common.keyboards import build_user_keyboard, build_admin_keyboard
from common.common import check_hidden_keyboard
from common.lang_dicts import TEXTS, get_lang
from custom_filters import Admin, PrivateChat, PrivateChatAndAdmin
from Config import Config
import models


async def inits(app: Application):
    bot: Bot = app.bot
    tg_owner = await bot.get_chat(chat_id=Config.OWNER_ID)
    with models.session_scope() as s:
        owner = s.get(models.User, tg_owner.id)
        if not owner:
            s.add(
                models.User(
                    user_id=tg_owner.id,
                    username=tg_owner.username if tg_owner.username else "",
                    name=tg_owner.full_name,
                    is_admin=True,
                )
            )

    await bot.set_my_description(
        description=(
            "• Search through available airdrops\n"
            "• Register on your behalf without wallet connection\n"
            "• Save and track the status of each airdrop you join\n"
            "• Notify you about new airdrop opportunities\n"
            "• Automatically send distributions to your wallet when released\n\n"
            "ماذا يمكن أن يفعل SamBot؟\n\n"
            "• البحث في قائمة الايردروبات المتاحة\n"
            "• التسجيل دون الحاجة لربط المحفظة\n"
            "• حفظ حالة كل ايردروب تشارك فيه\n"
            "• تنبيهك بالايردروبات الجديدة\n"
            "• إرسال التوزيعات إلى محفظتك بشكل تلقائي عند صدورها"
        ),
    )


async def set_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    st_cmd = ("start", "start command")
    commands = [st_cmd]
    if Admin().filter(update):
        commands.append(("admin", "admin command"))
    await context.bot.set_my_commands(
        commands=commands, scope=BotCommandScopeChat(chat_id=update.effective_chat.id)
    )


@add_new_user
@is_user_banned
@is_user_member
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChat().filter(update):
        await set_commands(update, context)
        lang = get_lang(update.effective_user.id)
        await update.message.reply_text(
            text=TEXTS[lang]["user_welcome_msg"],
            reply_markup=build_user_keyboard(lang=lang),
            disable_web_page_preview=True,
        )
        return ConversationHandler.END


start_command = CommandHandler(command="start", callback=start)


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if PrivateChatAndAdmin().filter(update):
        await set_commands(update, context)
        lang = get_lang(update.effective_user.id)
        await update.message.reply_text(
            text=TEXTS[lang]["admin_welcome_msg"],
            reply_markup=check_hidden_keyboard(context),
        )

        await update.message.reply_text(
            text=TEXTS[lang]["currently_admin"],
            reply_markup=build_admin_keyboard(lang, update.effective_user.id),
        )
        return ConversationHandler.END


admin_command = CommandHandler(command="admin", callback=admin)
