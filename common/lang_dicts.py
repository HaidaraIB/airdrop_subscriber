import models

TEXTS = {
    models.Language.ARABIC: {
        "welcome_msg": "أهلاً بك...",
        "force_join_msg": (
            f"لبدء استخدام البوت يجب عليك الانضمام الى محادثة البوت أولاً\n\n"
            "<b>اشترك أولاً 👇</b>\n"
            "ثم اضغط <b>تحقق ✅</b>"
        ),
        "force_join_multiple_msg": (
            f"لبدء استخدام البوت يجب عليك الانضمام الى محادثات البوت أولاً\n\n"
            "<b>اشترك في جميع المحادثات 👇</b>\n"
            "ثم اضغط <b>تحقق ✅</b>"
        ),
        "join_first_answer": "قم بالاشتراك بالمحادثة أولاً ❗️",
        "join_all_first_answer": "قم بالاشتراك في جميع المحادثات أولاً ❗️",
        "settings": "الإعدادات ⚙️",
        "change_lang": "اختر اللغة 🌐",
        "change_lang_success": "تم تغيير اللغة بنجاح ✅",
        "home_page": "القائمة الرئيسية 🔝",
        "currently_admin": "تعمل الآن كآدمن 🕹",
        "admin_settings_title": "إعدادات الآدمن 🪄",
        "add_admin_instruction": (
            "اختر حساب الآدمن الذي تريد إضافته بالضغط على الزر أدناه\n\n"
            "يمكنك إرسال الid برسالة أيضاً\n\n"
            "أو إلغاء العملية بالضغط على /admin."
        ),
        "admin_added_success": "تمت إضافة الآدمن بنجاح ✅",
        "cannot_remove_owner": "لا يمكنك إزالة مالك البوت من قائمة الآدمنز ❗️",
        "admin_removed_success": "تمت إزالة الآدمن بنجاح ✅",
        "remove_admin_instruction": "اختر من القائمة أدناه الآدمن الذي تريد إزالته.",
        "continue_with_admin_command": "للمتابعة اضغط /admin",
        "continue_with_start_command": "للمتابعة اضغط /start",
        "keyboard_hidden": "تم الإخفاء ✅",
        "keyboard_shown": "تم الإظهار ✅",
        "ban_instruction": (
            "اختر حساب المستخدم الذي تريد حظره بالضغط على الزر أدناه\n\n"
            "يمكنك إرسال الid برسالة أيضاً\n\n"
            "أو إلغاء العملية بالضغط على /admin."
        ),
        "user_not_found": (
            "لم يتم العثور على المستخدم ❗️\n"
            "تأكد من الآيدي أو من أن المستخدم قد بدأ محادثة مع البوت من قبل"
        ),
        "user_found": "تم العثور على المستخدم ✅",
        "do_you_want": "هل تريد",
        "operation_success": "تمت العملية بنجاح ✅",
        "ban_confirmation": (
            "معلومات المستخدم:\n"
            "{user_info}\n\n"
            "حالة الحظر الحالية: <b>{ban_status}</b>\n\n"
            "سيتم <b>{action}</b> هذا المستخدم.\n\n"
            "اضغط على زر <b>تأكيد</b> للمتابعة."
        ),
        "user_banned": "محظور 🔒",
        "user_not_banned": "غير محظور 🔓",
        "action_ban": "حظر",
        "action_unban": "فك حظر",
        "send_message": "أرسل الرسالة",
        "send_message_to": "هل تريد إرسال الرسالة إلى:",
        "send_user_ids": "قم بإرسال آيديات المستخدمين الذين تريد إرسال الرسالة لهم سطراً سطراً.",
        "send_chat_id": "أرسل آيدي القناة/المجموعة",
        "sending_messages": "يقوم البوت بإرسال الرسائل الآن، يمكنك متابعة استخدامه بشكل طبيعي",
        "bot_must_be_member": "يجب أن يكون البوت مشتركاً في هذه القناة/المجموعة حتى يتمكن من النشر فيها",
        "message_published_success": "تم نشر الرسالة في {chat_title} بنجاح ✅",
        "bot_owner": "مالك البوت",
        "force_join_chats_title": "إدارة محادثات الإجبار على الانضمام 💬",
        "add_force_join_chat_instruction": (
            "اختر المحادثة التي تريد إجبار المستخدمين على الانضمام إليها بالضغط على الزر أدناه\n\n"
            "يمكنك إرسال الid برسالة أيضاً\n\n"
            "أو إلغاء العملية بالضغط على /admin."
        ),
        "enter_chat_link_instruction": (
            "تم العثور على المحادثة: <b>{chat_title}</b>\n\n"
            "أرسل رابط المحادثة (invite link) أو اسم المستخدم\n\n"
            "مثال: https://t.me/channel_name أو @channel_name"
        ),
        "force_join_chat_added_success": "تمت إضافة محادثة الإجبار على الانضمام بنجاح ✅",
        "force_join_chat_removed_success": "تمت إزالة محادثة الإجبار على الانضمام بنجاح ✅",
        "remove_force_join_chat_instruction": "اختر من القائمة أدناه المحادثة التي تريد إزالتها.",
        "no_force_join_chats": "لا توجد محادثات إجبار على الانضمام حالياً ❗️",
        "force_join_chats_list_title": "قائمة محادثات الإجبار على الانضمام:",
        "invalid_chat_id": "آيدي المحادثة غير صحيح ❌",
        "chat_not_found": "لم يتم العثور على المحادثة ❗️\nتأكد من الآيدي أو من أن البوت عضو في المحادثة",
        "chat_link_required": "المحادثة لا تحتوي على رابط دعوة. يرجى إرسال رابط الدعوة يدوياً.",
        "invalid_chat_link": "رابط المحادثة غير صحيح ❌\nيجب أن يبدأ بـ https://t.me/ أو @",
        "send_contract_address": "أرسل عنوان العقد",
        "check_airdrop_instruction": "أرسل عنوان العقد أو اسم العملة",
        "airdrop_not_found": "لم يتم العثور على الآيردروب ❌\nتأكد من عنوان العقد",
        "airdrop_found": "تم العثور على الآيردروب ✅\n\n",
        "send_user_wallet_address": "أرسل عنوان المحفظة التي تحتفظ بها بعملة <b>{token_name}</b> أي عنوان لا يحتوي على <b>{token_name}</b> لن يتم احتسابه في الآيردروب أو التوزيع",
        "subscription_success": "تم الاشتراك في الآيردروب <b>{token_name}</b> بنجاح ✅",
        "wrong_address": "عنوان غير صحيح ❌\nيجب أن يحتوي العنوان على اسم العملة <b>{token_name}</b>",
        "airdrop_time_remaining": (
            "الوقت المتبقي لتوزيع الآيردروب:\n" "<b>{time_remaining}</b>"
        ),
        "no_airdrop_subscriptions": "لا يوجد اشتراكات في الآيردروبات ❗️",
        "choose_airdrop_subscription": "اختر الاشتراك في الآيردروب الذي تريد تعديل عنوان المحفظة عليه",
        "user_wallet_address_updated": "تم تعديل عنوان المحفظة بنجاح ✅",
        "unsubscribe_from_airdrop": "اختر الاشتراك في الآيردروب الذي تريد إلغاء الاشتراك منه",
        "unsubscribed_from_airdrop": "تم إلغاء الاشتراك في الآيردروب بنجاح ✅",
        "unsubscribe_confirmation": (
            "هل أنت متأكد من إلغاء الاشتراك في آيردروب <b>{token_name}</b>؟\n"
            "سيتم حذف جميع عناوين المحافظ المرتبطة بهذا الآيردروب."
        ),
        "airdrop_subscription_settings": "إعدادات الاشتراكات في الآيردروبات 🎁",
        "choose_airdrop_to_manage": "اختر الآيردروب الذي تريد إدارة اشتراكاته",
        "wallet_addresses_list": "عناوين المحافظ:\n{wallet_addresses}",
        "add_wallet_address": "إضافة عنوان محفظة ➕",
        "remove_wallet_address": "حذف عنوان محفظة ✖️",
        "wallet_address_added_success": "تمت إضافة عنوان المحفظة بنجاح ✅",
        "wallet_address_removed_success": "تم حذف عنوان المحفظة بنجاح ✅",
        "select_wallet_address_to_remove": "اختر عنوان المحفظة الذي تريد حذفه",
        "airdrop_settings_title": "إعدادات الآيردروبات 🎁",
        "add_airdrop_instruction": "أرسل عنوان العقد للآيردروب",
        "send_token_name": "أرسل اسم العملة",
        "send_amount": "أرسل المبلغ",
        "send_distribution_date": (
            "أرسل تاريخ التوزيع بصيغة:\n"
            "<code>YYYY-MM-DD HH:MM:SS</code>\n"
            "<i>مثال:</i>\n"
            "<code>2024-12-31 23:59:59</code>"
        ),
        "send_photo": "أرسل صورة الآيردروب",
        "airdrop_added_success": "تمت إضافة الآيردروب بنجاح ✅",
        "airdrop_removed_success": "تمت إزالة الآيردروب بنجاح ✅",
        "remove_airdrop_instruction": "اختر من القائمة أدناه الآيردروب الذي تريد إزالته",
        "no_airdrops": "لا توجد آيردروبات حالياً ❗️",
        "invalid_amount": "المبلغ غير صحيح ❌\n" "يجب أن يكون عدداً موجباً",
        "invalid_date": (
            "تاريخ التوزيع غير صحيح ❌\n"
            "يجب أن يكون بصيغة:\n"
            "<code>YYYY-MM-DD HH:MM:SS</code>\n"
            "<i>مثال:</i>\n"
            "<code>2024-12-31 23:59:59</code>"
        ),
        "distribution_date_in_the_past": "تاريخ التوزيع لا يمكن أن يكون في الماضي ❌",
        "airdrops_list_title": "قائمة الآيردروبات",
        "edit_airdrop_instruction": "اختر من القائمة أدناه الآيردروب الذي تريد تعديله",
        "airdrop_updated_success": "تم تحديث الآيردروب بنجاح ✅",
        "choose_field_to_edit": "اختر الحقل الذي تريد تعديله",
        "edit_contract_address": "تعديل عنوان العقد",
        "edit_token_name": "تعديل اسم العملة",
        "edit_amount": "تعديل المبلغ",
        "edit_distribution_date": "تعديل تاريخ التوزيع",
        "edit_photo": "تعديل الصورة",
        "airdrop_subscription_settings": "إعدادات الاشتراكات في الآيردروبات 🎁",
        "show_airdrop_instruction": "اختر الآيردروب الذي تريد عرضه",
        "subscribe_to_airdrop": "الاشتراك في آيردروب <b>{token_name}</b>",
        "current_wallet_address": "عنوان المحفظة الحالي: <code>{wallet_address}</code>",
        "choose_option": "اختر أحد الخيارات التالية",
    },
    models.Language.ENGLISH: {
        "welcome_msg": "Welcome...",
        "force_join_msg": (
            f"You have to join the bot's chat in order to be able to use it\n\n"
            "<b>Join First 👇</b>\n"
            "And then press <b>Verify ✅</b>"
        ),
        "force_join_multiple_msg": (
            f"You have to join the bot's chats in order to be able to use it\n\n"
            "<b>Join all chats 👇</b>\n"
            "And then press <b>Verify ✅</b>"
        ),
        "join_first_answer": "Join the chat first ❗️",
        "join_all_first_answer": "Join all chats first ❗️",
        "settings": "Settings ⚙️",
        "change_lang": "Choose a language 🌐",
        "change_lang_success": "Language changed ✅",
        "home_page": "Home page 🔝",
        "currently_admin": "You're currently an Admin 🕹",
        "admin_settings_title": "Admin Settings 🪄",
        "add_admin_instruction": (
            "Choose the admin account you want to add by clicking the button below\n\n"
            "You can also send the ID in a message\n\n"
            "Or cancel the operation by pressing /admin."
        ),
        "admin_added_success": "Admin added successfully ✅",
        "cannot_remove_owner": "You cannot remove the bot owner from the admin list ❗️",
        "admin_removed_success": "Admin removed successfully ✅",
        "remove_admin_instruction": "Choose from the list below the admin you want to remove.",
        "continue_with_admin_command": "To continue press /admin",
        "continue_with_start_command": "To continue press /start",
        "keyboard_hidden": "Hidden ✅",
        "keyboard_shown": "Shown ✅",
        "ban_instruction": (
            "Choose the user account you want to ban by clicking the button below\n\n"
            "You can also send the ID in a message\n\n"
            "Or cancel the operation by pressing /admin."
        ),
        "user_not_found": (
            "User not found ❗️\n"
            "Make sure of the ID or that the user has started a conversation with the bot before"
        ),
        "user_found": "User found ✅",
        "do_you_want": "Do you want to",
        "operation_success": "Operation completed successfully ✅",
        "ban_confirmation": (
            "User Information:\n"
            "{user_info}\n\n"
            "Current Ban Status: <b>{ban_status}</b>\n\n"
            "This user will be <b>{action}</b>.\n\n"
            "Press the <b>Confirm</b> button to proceed."
        ),
        "user_banned": "Banned 🔒",
        "user_not_banned": "Not Banned 🔓",
        "action_ban": "ban",
        "action_unban": "unban",
        "send_message": "Send the message",
        "send_message_to": "Who do you want to send the message to:",
        "send_user_ids": "Send the user IDs you want to send the message to, one per line.",
        "send_chat_id": "Send the channel/group ID",
        "sending_messages": "The bot is sending messages now, you can continue using it normally",
        "bot_must_be_member": "The bot must be a member of this channel/group to be able to post in it",
        "message_published_success": "Message published in {chat_title} successfully ✅",
        "bot_owner": "Bot Owner",
        "force_join_chats_title": "Manage Force Join Chats 💬",
        "add_force_join_chat_instruction": (
            "Choose the chat you want to force users to join by clicking the button below\n\n"
            "You can also send the ID in a message\n\n"
            "Or cancel the operation by pressing /admin."
        ),
        "enter_chat_link_instruction": (
            "Chat found: <b>{chat_title}</b>\n\n"
            "Send the chat invite link or username\n\n"
            "Example: https://t.me/channel_name or @channel_name"
        ),
        "force_join_chat_added_success": "Force join chat added successfully ✅",
        "force_join_chat_removed_success": "Force join chat removed successfully ✅",
        "remove_force_join_chat_instruction": "Choose from the list below the chat you want to remove.",
        "no_force_join_chats": "No force join chats currently ❗️",
        "force_join_chats_list_title": "Force Join Chats List:",
        "invalid_chat_id": "Invalid chat ID ❌",
        "chat_not_found": "Chat not found ❗️\nMake sure of the ID or that the bot is a member of the chat",
        "chat_link_required": "The chat doesn't have an invite link. Please send the invite link manually.",
        "invalid_chat_link": "Invalid chat link ❌\nMust start with https://t.me/ or @",
        "send_contract_address": "Send the contract address",
        "check_airdrop_instruction": "Send the contract address or token name",
        "airdrop_not_found": "Airdrop not found ❌\nMake sure of the contract address",
        "airdrop_found": "Airdrop found ✅\n\n",
        "send_user_wallet_address": "Send your address to receive the airdrop <b>{token_name}</b> any address that does not contain <b>{token_name}</b> will not be counted in the airdrop or distribution",
        "subscription_success": "Subscription to airdrop <b>{token_name}</b> successful ✅",
        "wrong_address": "Wrong address ❌\nThe address must contain the token name <b>{token_name}</b>",
        "airdrop_time_remaining": (
            "Time remaining to distribute the airdrop:\n" "<b>{time_remaining}</b>"
        ),
        "no_airdrop_subscriptions": "No airdrop subscriptions found ❗️",
        "choose_airdrop_subscription": "Choose the airdrop subscription you want to edit the wallet address of",
        "user_wallet_address_updated": "User wallet address updated successfully ✅",
        "unsubscribe_from_airdrop": "Choose the airdrop subscription you want to unsubscribe from",
        "unsubscribed_from_airdrop": "Unsubscribed from airdrop successfully ✅",
        "unsubscribe_confirmation": (
            "Are you sure you want to unsubscribe from airdrop <b>{token_name}</b>?\n\n"
            "All wallet addresses associated with this airdrop will be deleted."
        ),
        "airdrop_subscription_settings": "Airdrop Subscription Settings 🎁",
        "choose_airdrop_to_manage": "Choose the airdrop you want to manage subscriptions for",
        "wallet_addresses_list": "Wallet Addresses:\n{wallet_addresses}",
        "add_wallet_address": "Add Wallet Address ➕",
        "remove_wallet_address": "Remove Wallet Address ✖️",
        "wallet_address_added_success": "Wallet address added successfully ✅",
        "wallet_address_removed_success": "Wallet address removed successfully ✅",
        "select_wallet_address_to_remove": "Select the wallet address you want to remove",
        "airdrop_settings_title": "Airdrop Settings 🎁",
        "add_airdrop_instruction": "Send the contract address for the airdrop",
        "send_token_name": "Send the token name",
        "send_amount": "Send the amount",
        "send_distribution_date": (
            "Send the distribution date in format:\n"
            "<code>YYYY-MM-DD HH:MM:SS</code>\n"
            "<i>Example:</i>\n"
            "<code>2024-12-31 23:59:59</code>"
        ),
        "send_photo": "Send the airdrop photo",
        "airdrop_added_success": "Airdrop added successfully ✅",
        "airdrop_removed_success": "Airdrop removed successfully ✅",
        "remove_airdrop_instruction": "Choose from the list below the airdrop you want to remove",
        "no_airdrops": "No airdrops currently ❗️",
        "invalid_amount": "Invalid amount ❌\n" "Must be a positive number",
        "invalid_date": (
            "Invalid date ❌\n"
            "Must be in format:\n"
            "<code>YYYY-MM-DD HH:MM:SS</code>\n"
            "<i>Example:</i>\n"
            "<code>2024-12-31 23:59:59</code>"
        ),
        "distribution_date_in_the_past": "Distribution date cannot be in the past ❌",
        "airdrops_list_title": "Airdrops List",
        "edit_airdrop_instruction": "Choose from the list below the airdrop you want to edit",
        "airdrop_updated_success": "Airdrop updated successfully ✅",
        "choose_field_to_edit": "Choose the field you want to edit",
        "edit_contract_address": "Edit Contract Address",
        "edit_token_name": "Edit Token Name",
        "edit_amount": "Edit Amount",
        "edit_distribution_date": "Edit Distribution Date",
        "edit_photo": "Edit Photo",
        "airdrop_subscription_settings": "Airdrop Subscription Settings 🎁",
        "show_airdrop_instruction": "Choose the airdrop you want to show",
        "subscribe_to_airdrop": "Subscribe to Airdrop <b>{token_name}</b>",
        "current_wallet_address": "Current wallet address: <code>{wallet_address}</code>",
        "choose_option": "Choose one of the following options",
    },
}

BUTTONS = {
    models.Language.ARABIC: {
        "check_airdrop": "تحقق من وجود آيردروب 🔍",
        "check_joined": "تحقق ✅",
        "bot_channel": "قناة البوت 📢",
        "bot_chat": "محادثة البوت 💬",
        "back_button": "الرجوع 🔙",
        "settings": "الإعدادات ⚙️",
        "lang": "اللغة 🌐",
        "back_to_home_page": "العودة إلى القائمة الرئيسية 🔙",
        "select_admin_button": "اختيار حساب آدمن",
        "select_user_button": "اختيار حساب مستخدم",
        "unban_button": "فك الحظر 🔓",
        "ban_button": "حظر 🔒",
        "add_admin": "إضافة آدمن ➕",
        "remove_admin": "حذف آدمن ✖️",
        "show_admins": "عرض الآدمنز الحاليين 👓",
        "admin_settings": "إعدادات الآدمن 🎛",
        "ban_unban": "حظر/فك حظر 🔓🔒",
        "hide_ids_keyboard": "إخفاء/إظهار كيبورد معرفة الآيديات🪄",
        "broadcast": "رسالة جماعية 👥",
        "everyone": "الجميع 👥",
        "specific_users": "مستخدمين محددين 👤",
        "all_users": "جميع المستخدمين 👨🏻‍💼",
        "all_admins": "جميع الآدمنز 🤵🏻",
        "channel_or_group": "قناة أو مجموعة 📢",
        "force_join_chats": "محادثات الإجبار على الانضمام 💬",
        "force_join_chats_settings": "إعدادات محادثات الإجبار على الانضمام 💬",
        "add_force_join_chat": "إضافة محادثة ➕",
        "remove_force_join_chat": "حذف محادثة ✖️",
        "show_force_join_chats": "عرض المحادثات 👓",
        "select_chat_button": "اختيار محادثة",
        "confirm_button": "تأكيد ✅",
        "bot": "بوت 🤖",
        "channel": "قناة 📢",
        "group": "مجموعة 👥",
        "user": "مستخدم 🆔",
        "edit_user_wallet_address": "تعديل عنوان المحفظة 🖋",
        "unsubscribe_from_airdrop": "إلغاء الاشتراك في الآيردروب ⛔️",
        "show_airdrop_subscriptions": "عرض الاشتراكات في الآيردروبات 👓",
        "add_wallet_address": "إضافة عنوان محفظة ➕",
        "remove_wallet_address": "حذف عنوان محفظة ✖️",
        "airdrop_settings": "إعدادات الآيردروبات 🎁",
        "add_airdrop": "إضافة آيردروب ➕",
        "edit_airdrop": "تعديل آيردروب 🖋",
        "remove_airdrop": "حذف آيردروب ✖️",
        "show_airdrop": "عرض آيردروب 👓",
        "airdrop_subscription_settings": "إعدادات الاشتراكات في الآيردروبات 🎁",
        "edit_airdrop_contract_address": "تعديل عنوان العقد",
        "edit_airdrop_token_name": "تعديل اسم العملة",
        "edit_airdrop_amount": "تعديل المبلغ",
        "edit_airdrop_distribution_date": "تعديل تاريخ التوزيع",
        "edit_airdrop_photo": "تعديل الصورة",
        "subscribe_to_airdrop": "الاشتراك في الآيردروب ➕",
    },
    models.Language.ENGLISH: {
        "check_airdrop": "Check Airdrop 🔍",
        "check_joined": "Verify ✅",
        "bot_channel": "Bot's Channel 📢",
        "bot_chat": "Bot's Chat 💬",
        "back_button": "Back 🔙",
        "settings": "Settings ⚙️",
        "lang": "Language 🌐",
        "back_to_home_page": "Back to home page 🔙",
        "select_admin_button": "Select Admin Account",
        "select_user_button": "Select User Account",
        "unban_button": "Unban 🔓",
        "ban_button": "Ban 🔒",
        "add_admin": "Add Admin ➕",
        "remove_admin": "Remove Admin ✖️",
        "show_admins": "Show Current Admins 👓",
        "admin_settings": "Admin Settings 🎛",
        "ban_unban": "Ban/Unban 🔓🔒",
        "hide_ids_keyboard": "Hide/Show ID Keyboard🪄",
        "broadcast": "Broadcast Message 👥",
        "everyone": "Everyone 👥",
        "specific_users": "Specific Users 👤",
        "all_users": "All Users 👨🏻‍💼",
        "all_admins": "All Admins 🤵🏻",
        "channel_or_group": "Channel or Group 📢",
        "force_join_chats": "Force Join Chats 💬",
        "force_join_chats_settings": "Force Join Chats Settings 💬",
        "add_force_join_chat": "Add Chat ➕",
        "remove_force_join_chat": "Remove Chat ✖️",
        "show_force_join_chats": "Show Chats 👓",
        "select_chat_button": "Select Chat",
        "confirm_button": "Confirm ✅",
        "bot": "Bot 🤖",
        "channel": "Channel 📢",
        "group": "Group 👥",
        "user": "User 🆔",
        "edit_user_wallet_address": "Edit Wallet Address 🖋",
        "unsubscribe_from_airdrop": "Unsubscribe from Airdrop ⛔️",
        "show_airdrop_subscriptions": "Show Airdrop Subscriptions 👓",
        "add_wallet_address": "Add Wallet Address ➕",
        "remove_wallet_address": "Remove Wallet Address ✖️",
        "airdrop_settings": "Airdrop Settings 🎁",
        "add_airdrop": "Add Airdrop ➕",
        "edit_airdrop": "Edit Airdrop 🖋",
        "remove_airdrop": "Remove Airdrop ✖️",
        "show_airdrop": "Show Airdrop 👓",
        "airdrop_subscription_settings": "Airdrop Subscription Settings 🎁",
        "edit_airdrop_contract_address": "Edit Contract Address",
        "edit_airdrop_token_name": "Edit Token Name",
        "edit_airdrop_amount": "Edit Amount",
        "edit_airdrop_distribution_date": "Edit Distribution Date",
        "edit_airdrop_photo": "Edit Photo",
        "subscribe_to_airdrop": "Subscribe to Airdrop ➕",
    },
}


def get_lang(user_id: int):
    with models.session_scope() as s:
        return s.get(models.User, user_id).lang
