from telegram import Update
from start import start_command, admin_command
from common.common import create_folders
from common.back_to_home_page import (
    back_to_admin_home_page_handler,
    back_to_user_home_page_handler,
)
from common.error_handler import error_handler
from common.force_join import check_joined_handler

from user.user_calls import *
from user.user_settings import *
from user.airdrop_subscription_settings import *
from user.check_airdrop import *

from admin.admin_calls import *
from admin.admin_settings import *
from admin.broadcast import *
from admin.ban import *
from admin.force_join_chats_settings import *
from admin.airdrop_settings import *

from models import init_db

from MyApp import MyApp


def setup_and_run():
    create_folders()
    init_db()

    app = MyApp.build_app()

    # CHECK AIRDROP
    app.add_handler(check_airdrop_handler)

    # AIRDROP SUBSCRIPTION SETTINGS
    app.add_handler(edit_user_wallet_address_handler)
    app.add_handler(show_airdrop_subscriptions_handler)
    app.add_handler(unsubscribe_from_airdrop_handler)
    app.add_handler(airdrop_subscription_settings_handler)

    # USER SETTINGS
    app.add_handler(user_settings_handler)
    app.add_handler(change_lang_handler)

    # ADMIN SETTINGS
    app.add_handler(show_admins_handler)
    app.add_handler(add_admin_handler)
    app.add_handler(remove_admin_handler)
    app.add_handler(admin_settings_handler)

    # FORCE JOIN CHATS
    app.add_handler(add_force_join_chat_handler)
    app.add_handler(remove_force_join_chat_handler)
    app.add_handler(show_force_join_chats_handler)
    app.add_handler(force_join_chats_settings_handler)

    # AIRDROP SETTINGS
    app.add_handler(add_airdrop_handler)
    app.add_handler(edit_airdrop_handler)
    app.add_handler(remove_airdrop_handler)
    app.add_handler(show_airdrop_handler)
    app.add_handler(airdrop_settings_handler)

    app.add_handler(broadcast_message_handler)

    app.add_handler(check_joined_handler)

    app.add_handler(ban_unban_user_handler)

    app.add_handler(admin_command)
    app.add_handler(start_command)
    app.add_handler(find_id_handler)
    app.add_handler(hide_ids_keyboard_handler)
    app.add_handler(back_to_user_home_page_handler)
    app.add_handler(back_to_admin_home_page_handler)

    app.add_error_handler(error_handler)

    app.run_polling(allowed_updates=Update.ALL_TYPES)
