import asyncio
import random
import string
import sqlite3
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

TOKEN = '8915805327:AAGSC0o39SCg3iVT-CftKEK2W0Y0_sj66aw'
ADMIN_PASSWORD = "hpQeu7Kk"

# ===== СЛОВАРИ ДЛЯ ПЕРЕВОДА =====
TEXTS = {
    "ru": {
        "welcome": "🏔️ Добро пожаловать в NORDNFT – надёжный P2P-гарант\n\n🔒 Покупайте и продавайте NFT, токены, Telegram-подарки и многое другое – безопасно и без риска.\n\n• Удобное управление балансами\n• Реферальная система\n• Сделки с гарантией\n\nВыберите нужный раздел ниже:",
        "profile": "💰 Ваши балансы:\n🇷🇺 Рубли: {rub} RUB\n💵 USD: {usd} USD\n⭐ Звёзды: {stars} STARS\n\n📝 Ваши реквизиты:\n{req_text}\n\n📊 Ваша история сделок:\n{history_text}",
        "no_req": "❌ Реквизиты не заполнены.",
        "no_history": "У вас пока нет сделок.",
        "reqs_saved": "✅ Реквизиты сохранены в базе!",
        "reqs_format": "💳 Введи свои реквизиты для вывода.\nИспользуй формат:\n\n`card: номер карты`\n`crypto: адрес кошелька`\n`stars: @username`\n\nПример:\n`card: 1234 5678 9012 3456`",
        "withdraw_ask": "💰 Введи сумму для вывода (в той валюте, которую хочешь вывести):",
        "withdraw_ok": "✅ Заявка на вывод {amount} {currency} создана!\nРеквизиты:\nКарта: {card}\nКрипта: {crypto}\nЗвёзды: {stars}\n\nСредства будут отправлены в ближайшее время.",
        "withdraw_low": "❌ Недостаточно средств на балансе.",
        "choose_pay": "💰 Выбери валюту, в которой принимаешь оплату:",
        "no_reqs_pay": "⚠️ Сначала добавь реквизиты для вывода!",
        "nft_name": "✏️ Введи название NFT (например: CryptoPunk #123):",
        "nft_price": "💰 Введи цену в выбранной валюте (только число):",
        "nft_buyer": "🆔 Введи @username покупателя (без @, например: john_doe):",
        "deal_created": "✅ Сделка #{id} создана!\nКод: {code}\nNFT: {nft}\nЦена: {price} {pay}\nПокупатель: @{buyer}\n\n🔗 Отправь ссылку покупателю:\n{link}",
        "buyer_notify": "📦 Продавец создал для тебя сделку!\nNFT: {nft}\nЦена: {price} {pay}\n\n🔗 Перейди по ссылке, чтобы оплатить:\n{link}",
        "deal_joined": "🔗 Вы присоединились к сделке #{id}!\nNFT: {nft}\nЦена: {price} {pay}\n\n💰 Ваш баланс ({pay}): {balance} \n\nДля оплаты нажмите кнопку. Деньги будут заморожены.",
        "pay_btn": "✅ Оплатить со счета",
        "no_money": "❌ Недостаточно средств на балансе в {pay}.\nВаш баланс: {balance}\nЦена: {price}\n\nОбратитесь к администратору.",
        "money_frozen": "✅ Деньги списаны и заморожены!\nСделка #{id} ожидает передачи NFT.",
        "seller_notify_pay": "🔔 Покупатель @{buyer} оплатил сделку #{id}!\nДеньги заморожены.\n\nПередайте NFT и нажмите кнопку.",
        "transfer_btn": "📤 Передал товар",
        "transfer_ok": "✅ Вы подтвердили передачу NFT!\nТеперь покупатель должен подтвердить получение.",
        "buyer_notify_transfer": "🔔 Продавец передал вам NFT по сделке #{id}!\nПроверьте получение и нажмите кнопку.",
        "confirm_btn": "✅ Подтвердить получение",
        "confirm_ok": "✅ Сделка #{id} завершена!\nДеньги разморожены и переведены продавцу.\nСпасибо!",
        "seller_notify_confirm": "💰 Сделка #{id} завершена!\nСумма {price} {pay} зачислена на ваш баланс.",
        "ref_link": "🔗 Твоя реферальная ссылка:\nhttps://t.me/NORDNFT_bot?start=ref_{uid}",
        "support": "📞 Связь с поддержкой: @Nordnftsupport",
        "back": "🏔️ Главное меню:",
        "lang_changed": "🌍 Язык изменён на русский.",
        "unknown": "Используй кнопки или /start.",
        "btn_profile": "💼 Профиль",
        "btn_create": "➕ Создать сделку",
        "btn_ref": "📊 Реферальная ссылка",
        "btn_lang": "🌐 Change language",
        "btn_support": "🆘 Поддержка",
        "btn_back": "🔙 Назад",
        "btn_edit_req": "✏️ Изменить реквизиты",
        "btn_withdraw": "💳 Вывести средства",
        "btn_add_req": "➕ Добавить реквизиты",
    },
    "en": {
        "welcome": "🏔️ Welcome to NORDNFT – reliable P2P escrow\n\n🔒 Buy and sell NFTs, tokens, Telegram gifts and more – safely and risk-free.\n\n• Easy balance management\n• Referral system\n• Secure deals\n\nChoose a section below:",
        "profile": "💰 Your balances:\n🇷🇺 RUB: {rub} RUB\n💵 USD: {usd} USD\n⭐ STARS: {stars} STARS\n\n📝 Your payment details:\n{req_text}\n\n📊 Your deal history:\n{history_text}",
        "no_req": "❌ Payment details not set.",
        "no_history": "You have no deals yet.",
        "reqs_saved": "✅ Details saved to database!",
        "reqs_format": "💳 Enter your payment details.\nFormat:\n\n`card: card number`\n`crypto: wallet address`\n`stars: @username`\n\nExample:\n`card: 1234 5678 9012 3456`",
        "withdraw_ask": "💰 Enter amount to withdraw (in the currency you want):",
        "withdraw_ok": "✅ Withdrawal request for {amount} {currency} created!\nDetails:\nCard: {card}\nCrypto: {crypto}\nStars: {stars}\n\nFunds will be sent soon.",
        "withdraw_low": "❌ Insufficient funds.",
        "choose_pay": "💰 Choose payment currency:",
        "no_reqs_pay": "⚠️ Add payment details first!",
        "nft_name": "✏️ Enter NFT name (e.g., CryptoPunk #123):",
        "nft_price": "💰 Enter price (number only):",
        "nft_buyer": "🆔 Enter buyer's @username (without @, e.g., john_doe):",
        "deal_created": "✅ Deal #{id} created!\nCode: {code}\nNFT: {nft}\nPrice: {price} {pay}\nBuyer: @{buyer}\n\n🔗 Send link to buyer:\n{link}",
        "buyer_notify": "📦 Seller created a deal for you!\nNFT: {nft}\nPrice: {price} {pay}\n\n🔗 Click to pay:\n{link}",
        "deal_joined": "🔗 You joined deal #{id}!\nNFT: {nft}\nPrice: {price} {pay}\n\n💰 Your balance ({pay}): {balance} \n\nClick to pay. Funds will be frozen.",
        "pay_btn": "✅ Pay from balance",
        "no_money": "❌ Insufficient funds in {pay}.\nBalance: {balance}\nPrice: {price}\n\nContact admin.",
        "money_frozen": "✅ Funds deducted and frozen!\nDeal #{id} awaits NFT transfer.",
        "seller_notify_pay": "🔔 Buyer @{buyer} paid for deal #{id}!\nFunds frozen.\n\nTransfer NFT and click button.",
        "transfer_btn": "📤 Transferred item",
        "transfer_ok": "✅ You confirmed transfer!\nNow buyer must confirm receipt.",
        "buyer_notify_transfer": "🔔 Seller transferred NFT for deal #{id}!\nCheck it and click confirm.",
        "confirm_btn": "✅ Confirm receipt",
        "confirm_ok": "✅ Deal #{id} completed!\nFunds unfrozen and sent to seller.\nThank you!",
        "seller_notify_confirm": "💰 Deal #{id} completed!\n{price} {pay} added to your balance.",
        "ref_link": "🔗 Your referral link:\nhttps://t.me/NORDNFT_bot?start=ref_{uid}",
        "support": "📞 Support: @Nordnftsupport",
        "back": "🏔️ Main menu:",
        "lang_changed": "🌍 Language changed to English.",
        "unknown": "Use buttons or /start.",
        "btn_profile": "💼 Profile",
        "btn_create": "➕ Create deal",
        "btn_ref": "📊 Referral link",
        "btn_lang": "🌐 Change language",
        "btn_support": "🆘 Support",
        "btn_back": "🔙 Back",
        "btn_edit_req": "✏️ Edit details",
        "btn_withdraw": "💳 Withdraw",
        "btn_add_req": "➕ Add details",
    }
}

# ===== БАЗА ДАННЫХ =====
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        uid INTEGER PRIMARY KEY,
        balance_rub REAL DEFAULT 0,
        balance_usd REAL DEFAULT 0,
        balance_stars REAL DEFAULT 0,
        card TEXT DEFAULT '',
        crypto TEXT DEFAULT '',
        stars TEXT DEFAULT '',
        lang TEXT DEFAULT 'ru'
    )''')
    cursor.execute("PRAGMA table_info(users)")
    columns = [info[1] for info in cursor.fetchall()]
    if "lang" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN lang TEXT DEFAULT 'ru'")
    cursor.execute('''CREATE TABLE IF NOT EXISTS deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seller_id INTEGER,
        buyer_id INTEGER,
        nft TEXT,
        price REAL,
        payment TEXT,
        status TEXT,
        code TEXT,
        buyer_username TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

def get_user(uid):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT balance_rub, balance_usd, balance_stars, card, crypto, stars, lang FROM users WHERE uid = ?", (uid,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"rub": row[0], "usd": row[1], "stars_bal": row[2], "card": row[3], "crypto": row[4], "stars": row[5], "lang": row[6]}
    else:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (uid) VALUES (?)", (uid,))
        conn.commit()
        conn.close()
        return {"rub": 0, "usd": 0, "stars_bal": 0, "card": "", "crypto": "", "stars": "", "lang": "ru"}

def update_balance(uid, field, amount):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if field in ['balance_rub', 'balance_usd', 'balance_stars']:
        cursor.execute(f"UPDATE users SET {field} = {field} + ? WHERE uid = ?", (amount, uid))
        conn.commit()
    conn.close()

def update_reqs(uid, field, value):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if field in ['card', 'crypto', 'stars']:
        cursor.execute(f"UPDATE users SET {field} = ? WHERE uid = ?", (value, uid))
        conn.commit()
    conn.close()

def update_lang(uid, lang):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET lang = ? WHERE uid = ?", (lang, uid))
    conn.commit()
    conn.close()

def get_deal(deal_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM deals WHERE id = ?", (deal_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "id": row[0], "seller": row[1], "buyer_id": row[2], "nft": row[3], 
            "price": row[4], "payment": row[5], "status": row[6], "code": row[7], "buyer_username": row[8]
        }
    return None

def get_user_deals(uid):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nft, price, status, buyer_username FROM deals WHERE seller_id = ? OR buyer_id = ? ORDER BY id DESC LIMIT 5", (uid, uid))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_deal_status(deal_id, status, buyer_id=None):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if buyer_id:
        cursor.execute("UPDATE deals SET status = ?, buyer_id = ? WHERE id = ?", (status, buyer_id, deal_id))
    else:
        cursor.execute("UPDATE deals SET status = ? WHERE id = ?", (status, deal_id))
    conn.commit()
    conn.close()

def generate_deal_code():
    chars = string.ascii_letters + string.digits
    return f"#{''.join(random.choices(chars, k=6))}"

# ===== ВСПОМОГАТЕЛЬНЫЕ =====
def get_lang(uid):
    return get_user(uid).get("lang", "ru")

def get_text(uid, key, **kwargs):
    lang = get_lang(uid)
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, key)
    if "uid" not in kwargs:
        kwargs["uid"] = uid
    return text.format(**kwargs)

def main_menu_keyboard(uid):
    lang = get_lang(uid)
    t = TEXTS[lang]
    keyboard = [
        [KeyboardButton(t["btn_profile"]), KeyboardButton(t["btn_create"])],
        [KeyboardButton(t["btn_ref"]), KeyboardButton(t["btn_lang"])],
        [KeyboardButton(t["btn_support"])]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def profile_keyboard(uid):
    lang = get_lang(uid)
    t = TEXTS[lang]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(t["btn_edit_req"], callback_data="edit_req")],
        [InlineKeyboardButton(t["btn_withdraw"], callback_data="withdraw")]
    ])

def payment_keyboard(uid):
    user = get_user(uid)
    buttons = []
    lang = get_lang(uid)
    if user.get("card"): buttons.append("🇷🇺 Рубли (карта)" if lang == "ru" else "🇷🇺 RUB (card)")
    if user.get("crypto"): buttons.append("💵 USDT (крипта)" if lang == "ru" else "💵 USDT (crypto)")
    if user.get("stars"): buttons.append("⭐ Звёзды (Telegram)" if lang == "ru" else "⭐ Stars (Telegram)")
    if not buttons: buttons = ["⚠️ Сначала добавь реквизиты" if lang == "ru" else "⚠️ Add details first"]
    keyboard = [[KeyboardButton(b)] for b in buttons]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ===== ХЕНДЛЕРЫ =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    get_user(uid)
    
    if context.args and context.args[0].startswith("deal_"):
        try:
            deal_id = int(context.args[0].split("_")[1])
        except (IndexError, ValueError):
            await update.message.reply_text("❌ Неверный формат ссылки.")
            return
        await handle_deal_link(update, context, deal_id)
        return

    await update.message.reply_text(get_text(uid, "welcome"), reply_markup=main_menu_keyboard(uid))

async def handle_deal_link(update: Update, context: ContextTypes.DEFAULT_TYPE, deal_id: int):
    uid = update.effective_user.id
    deal = get_deal(deal_id)

    if not deal:
        await update.message.reply_text("❌ Сделка не найдена.")
        return
    if deal['status'] != "ожидает оплаты":
        await update.message.reply_text(f"❌ Эта сделка уже {deal['status']}.")
        return

    buyer_username = update.effective_user.username or str(uid)
    if deal['buyer_username'] != buyer_username and deal['buyer_username'] != str(uid):
        await update.message.reply_text("❌ Эта сделка для другого пользователя.")
        return

    update_deal_status(deal_id, "ожидает оплаты", buyer_id=uid)
    context.user_data['current_deal'] = deal_id
    
    display_id = deal_id + 458
    
    user = get_user(uid)
    pay = deal['payment']
    if "Рубли" in pay: balance = user['rub']
    elif "USDT" in pay: balance = user['usd']
    else: balance = user['stars_bal']
    
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(get_text(uid, "pay_btn"), callback_data=f"pay_{deal_id}")]])

    await update.message.reply_text(
        get_text(uid, "deal_joined", id=display_id, nft=deal['nft'], price=deal['price'], pay=pay, balance=balance),
        reply_markup=keyboard
    )

async def rub_command(update: Update, context: ContextTypes.DEFAULT_TYPE): await handle_deposit(update, context, "balance_rub")
async def usd_command(update: Update, context: ContextTypes.DEFAULT_TYPE): await handle_deposit(update, context, "balance_usd")
async def stars_command(update: Update, context: ContextTypes.DEFAULT_TYPE): await handle_deposit(update, context, "balance_stars")

async def handle_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE, field: str):
    uid = update.effective_user.id
    args = context.args
    if len(args) != 2:
        await update.message.reply_text(f"❌ Формат: /{update.message.text.split()[0][1:]} сумма пароль")
        return
    try: amount = float(args[0])
    except ValueError: await update.message.reply_text("❌ Введи число."); return
    if args[1] != ADMIN_PASSWORD: await update.message.reply_text("❌ Неверный пароль."); return

    update_balance(uid, field, amount)
    user = get_user(uid)
    await update.message.reply_text(f"✅ Баланс пополнен на {amount}!\nТекущие балансы:\nРубли: {user['rub']}\nUSD: {user['usd']}\nЗвёзды: {user['stars_bal']}")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    user = get_user(uid)
    lang = get_lang(uid)
    t = TEXTS[lang]

    if text == t["btn_profile"]:
        req_text = ""
        if user.get("card"): req_text += f"💳 Карта: {user['card']}\n"
        if user.get("crypto"): req_text += f"🔗 Крипта: {user['crypto']}\n"
        if user.get("stars"): req_text += f"⭐ Звёзды: {user['stars']}\n"
        if not req_text: req_text = get_text(uid, "no_req")

        history_text = ""
        deals = get_user_deals(uid)
        if not deals:
            history_text = get_text(uid, "no_history")
        else:
            for d in deals:
                display_history_id = d[0] + 458
                history_text += f"🔹 #{display_history_id} | {d[1]} | {d[2]} | Статус: {d[3]}\n"
        
        await update.message.reply_text(
            get_text(uid, "profile", rub=user['rub'], usd=user['usd'], stars=user['stars_bal'], req_text=req_text, history_text=history_text),
            reply_markup=profile_keyboard(uid)
        )
        return

    elif text == t["btn_lang"]:
        new_lang = "en" if lang == "ru" else "ru"
        update_lang(uid, new_lang)
        await update.message.reply_text(get_text(uid, "lang_changed"), reply_markup=main_menu_keyboard(uid))
        return

    elif text == t["btn_create"]:
        if not any([user.get("card"), user.get("crypto"), user.get("stars")]):
            await update.message.reply_text(get_text(uid, "no_reqs_pay"))
            return
        await update.message.reply_text(get_text(uid, "choose_pay"), reply_markup=payment_keyboard(uid))
        context.user_data['awaiting_payment'] = True
        return

    elif text == t["btn_ref"]:
        await update.message.reply_text(get_text(uid, "ref_link"))
        return

    elif text == t["btn_support"]:
        await update.message.reply_text(get_text(uid, "support"))
        return

    elif text in ["🇷🇺 Рубли (карта)", "💵 USDT (крипта)", "⭐ Звёзды (Telegram)", "🇷🇺 RUB (card)", "💵 USDT (crypto)", "⭐ Stars (Telegram)"] and context.user_data.get('awaiting_payment'):
        context.user_data['payment_method'] = text
        context.user_data['awaiting_payment'] = False
        await update.message.reply_text(get_text(uid, "nft_name"))
        context.user_data['awaiting_nft'] = True
        return

async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    text = update.message.text
    lang = get_lang(uid)
    t = TEXTS[lang]

    if context.user_data.get('awaiting_requisites'):
        for line in text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                if key.strip().lower() in ['card', 'crypto', 'stars']: update_reqs(uid, key.strip().lower(), value.strip())
        context.user_data['awaiting_requisites'] = False
        await update.message.reply_text(get_text(uid, "reqs_saved"), reply_markup=main_menu_keyboard(uid))
        return

    if context.user_data.get('awaiting_withdraw'):
        try:
            amount = float(text)
            if amount <= 0:
                await update.message.reply_text("❌ Введи число больше 0.")
                return
            if amount > get_user(uid).get("rub", 0):
                await update.message.reply_text(get_text(uid, "withdraw_low"))
                return
            update_balance(uid, "balance_rub", -amount)
            user = get_user(uid)
            await update.message.reply_text(get_text(uid, "withdraw_ok", amount=amount, currency="RUB", card=user.get('card','-'), crypto=user.get('crypto','-'), stars=user.get('stars','-')), reply_markup=main_menu_keyboard(uid))
            context.user_data['awaiting_withdraw'] = False
        except ValueError: await update.message.reply_text("❌ Введи число.")
        return

    if context.user_data.get('awaiting_nft'):
        context.user_data['nft_name'] = text
        context.user_data['awaiting_nft'] = False
        await update.message.reply_text(get_text(uid, "nft_price"))
        context.user_data['awaiting_price'] = True
        return

    if context.user_data.get('awaiting_price'):
        try:
            price = float(text)
            context.user_data['price'] = price
            context.user_data['awaiting_price'] = False
            await update.message.reply_text(get_text(uid, "nft_buyer"))
            context.user_data['awaiting_buyer'] = True
        except: await update.message.reply_text("❌ Введи число.")
        return

    if context.user_data.get('awaiting_buyer'):
        buyer_username = text.strip().replace('@', '')
        context.user_data['buyer_username'] = buyer_username
        context.user_data['awaiting_buyer'] = False
        await finish_deal(update, context)
        return

async def finish_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    deal_data = {"nft": context.user_data.get('nft_name'), "price": context.user_data.get('price'), "buyer_username": context.user_data.get('buyer_username'), "payment_method": context.user_data.get('payment_method')}
    if not all(deal_data.values()):
        await update.message.reply_text("❌ Ошибка. Начни заново.")
        return

    deal_code = generate_deal_code()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO deals (seller_id, nft, price, payment, status, code, buyer_username) VALUES (?, ?, ?, ?, ?, ?, ?)''', (uid, deal_data['nft'], deal_data['price'], deal_data['payment_method'], "ожидает оплаты", deal_code, deal_data['buyer_username']))
    deal_id = cursor.lastrowid
    conn.commit()
    conn.close()

    display_id = deal_id + 458

    bot_username = (await context.bot.get_me()).username
    deal_link = f"https://t.me/{bot_username}?start=deal_{deal_id}"

    await update.message.reply_text(get_text(uid, "deal_created", id=display_id, code=deal_code, nft=deal_data['nft'], price=deal_data['price'], pay=deal_data['payment_method'], buyer=deal_data['buyer_username'], link=deal_link))
    try: await context.bot.send_message(deal_data['buyer_username'], get_text(deal_data['buyer_username'], "buyer_notify", nft=deal_data['nft'], price=deal_data['price'], pay=deal_data['payment_method'], link=deal_link))
    except: pass
    context.user_data.clear()

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = update.effective_user.id
    data = query.data
    lang = get_lang(uid)
    t = TEXTS[lang]

    if data == "edit_req":
        await query.message.reply_text(get_text(uid, "reqs_format"), parse_mode="Markdown")
        context.user_data['awaiting_requisites'] = True
        return
    elif data == "withdraw":
        user = get_user(uid)
        if not any([user.get("card"), user.get("crypto"), user.get("stars")]):
            await query.message.reply_text(get_text(uid, "no_reqs_pay"))
            return
        await query.message.reply_text(get_text(uid, "withdraw_ask"), reply_markup=ReplyKeyboardMarkup([[KeyboardButton(t["btn_back"])]], resize_keyboard=True))
        context.user_data['awaiting_withdraw'] = True
        return
    elif data == "back":
        await query.message.reply_text(get_text(uid, "back"), reply_markup=main_menu_keyboard(uid))
        return

    if data.startswith("pay_"):
        deal_id = int(data.split("_")[1])
        deal = get_deal(deal_id)
        if not deal or deal['status'] != "ожидает оплаты": await query.edit_message_text("❌ Недействительно."); return
        
        user = get_user(uid)
        pay = deal['payment']
        
        if "Рубли" in pay: bal = user['rub']
        elif "USDT" in pay: bal = user['usd']
        else: bal = user['stars_bal']
        
        if bal < deal['price']: 
            await query.edit_message_text(get_text(uid, "no_money", balance=bal, pay=pay, price=deal['price']))
            return
        
        if "Рубли" in pay: update_balance(uid, "balance_rub", -deal['price'])
        elif "USDT" in pay: update_balance(uid, "balance_usd", -deal['price'])
        else: update_balance(uid, "balance_stars", -deal['price'])
        
        update_deal_status(deal_id, "деньги заморожены", buyer_id=uid)
        display_id = deal_id + 458
        await query.edit_message_text(get_text(uid, "money_frozen", id=display_id))

        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(get_text(deal['seller'], "transfer_btn"), callback_data=f"transfer_{deal_id}")]])
        await context.bot.send_message(deal['seller'], get_text(deal['seller'], "seller_notify_pay", buyer=deal['buyer_username'], id=display_id), reply_markup=keyboard)

    elif data.startswith("transfer_"):
        deal_id = int(data.split("_")[1])
        deal = get_deal(deal_id)
        if not deal or deal['status'] != "деньги заморожены": await query.edit_message_text("❌ Ошибка."); return
        
        update_deal_status(deal_id, "передано")
        display_id = deal_id + 458
        await query.edit_message_text(get_text(uid, "transfer_ok"))
        
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(get_text(deal['buyer_id'], "confirm_btn"), callback_data=f"confirm_{deal_id}")]])
        try: await context.bot.send_message(deal['buyer_id'], get_text(deal['buyer_id'], "buyer_notify_transfer", id=display_id), reply_markup=keyboard)
        except: pass

    elif data.startswith("confirm_"):
        deal_id = int(data.split("_")[1])
        deal = get_deal(deal_id)
        if not deal or deal['status'] != "передано": await query.edit_message_text("❌ Ошибка."); return
        
        update_deal_status(deal_id, "завершена")
        
        pay = deal['payment']
        if "Рубли" in pay: update_balance(deal['seller'], "balance_rub", deal['price'])
        elif "USDT" in pay: update_balance(deal['seller'], "balance_usd", deal['price'])
        else: update_balance(deal['seller'], "balance_stars", deal['price'])
        
        display_id = deal_id + 458
        await query.edit_message_text(get_text(uid, "confirm_ok", id=display_id))
        await context.bot.send_message(deal['seller'], get_text(deal['seller'], "seller_notify_confirm", id=display_id, price=deal['price'], pay=pay))

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await update.message.reply_text(get_text(uid, "unknown"), reply_markup=main_menu_keyboard(uid))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("rub", rub_command))
    app.add_handler(CommandHandler("usd", usd_command))
    app.add_handler(CommandHandler("stars", stars_command))
    
    # Исправил предупреждение (добавил r перед строкой)
    button_filter = r"^(💼 Профиль|➕ Создать сделку|📊 Реферальная ссылка|🌐 Change language|🆘 Поддержка|💼 Profile|➕ Create deal|📊 Referral link|🆘 Support|🇷🇺 Рубли \(карта\)|💵 USDT \(крипта\)|⭐ Звёзды \(Telegram\)|🇷🇺 RUB \(card\)|💵 USDT \(crypto\)|⭐ Stars \(Telegram\)|🔙 Назад|🔙 Back)$"
    
    app.add_handler(MessageHandler(filters.Regex(button_filter), handle_buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_input))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🏔️ NORDNFT Bot запущен с БАЗОЙ ДАННЫХ...")
    app.run_polling()

if __name__ == "__main__":
    main()