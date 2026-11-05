import math
import string

COMMON_PASSWORDS = {
    "123456", "12345678", "123456789", "password", "qwerty", "111111",
    "abc123", "iloveyou", "admin", "letmein", "welcome", "000000",
    "1234", "12345", "password1", "qwerty123", "123123", "654321",
}


def check_password(password: str) -> dict:
    """رمز رو بررسی می‌کنه و امتیاز، سطح، پیشنهادها و زمان شکستن رو برمی‌گردونه."""
    if not password:
        return {"score": 0, "level": "خالی", "suggestions": [], "crack_time": "-"}

    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(c in string.punctuation for c in password)
    length = len(password)

    suggestions = []
    score = 0

    # طول رمز
    if length >= 16:
        score += 40
    elif length >= 12:
        score += 30
    elif length >= 8:
        score += 18
    else:
        score += 5
        suggestions.append("رمز رو حداقل ۱۲ کاراکتر کن")
    if 8 <= length < 12:
        suggestions.append("برای امنیت بیشتر، طول رمز رو به ۱۲ کاراکتر یا بیشتر برسون")

    # انواع کاراکتر
    if has_lower:
        score += 10
    else:
        suggestions.append("از حروف کوچک انگلیسی استفاده کن")
    if has_upper:
        score += 15
    else:
        suggestions.append("از حروف بزرگ انگلیسی استفاده کن")
    if has_digit:
        score += 15
    else:
        suggestions.append("چند تا عدد به رمز اضافه کن")
    if has_symbol:
        score += 20
    else:
        suggestions.append("از نمادهایی مثل ! @ # $ % استفاده کن")

    # رمزهای رایج
    if password.lower() in COMMON_PASSWORDS:
        score = min(score, 10)
        suggestions.insert(0, "این رمز خیلی رایجه و در چند ثانیه حدس زده می‌شه!")

    # تکرار کاراکتر (مثل aaaa)
    if length >= 3 and len(set(password)) <= length // 2:
        score -= 15
        suggestions.append("از تکرار زیاد کاراکترها پرهیز کن")

    # الگوی ترتیبی (مثل 1234 یا abcd)
    lowered = password.lower()
    for seq in ("0123456789", "abcdefghijklmnopqrstuvwxyz", "qwertyuiop"):
        for i in range(len(seq) - 3):
            if seq[i:i + 4] in lowered:
                score -= 10
                suggestions.append("از الگوهای ساده مثل 1234 یا abcd استفاده نکن")
                break
        else:
            continue
        break

    score = max(0, min(100, score))

    if score < 40:
        level = "ضعیف"
    elif score < 70:
        level = "متوسط"
    else:
        level = "قوی"

    if not suggestions:
        suggestions.append("آفرین! رمزت عالیه 👏")

    return {
        "score": score,
        "level": level,
        "suggestions": suggestions,
        "crack_time": estimate_crack_time(password),
    }


def estimate_crack_time(password: str) -> str:
    """تخمین ساده‌ی زمان شکستن رمز (با فرض ۱۰ میلیارد حدس در ثانیه)."""
    pool = 0
    if any(c.islower() for c in password):
        pool += 26
    if any(c.isupper() for c in password):
        pool += 26
    if any(c.isdigit() for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += 32
    if pool == 0:
        pool = 26

    if password.lower() in COMMON_PASSWORDS:
        return "فوری"

    combos = pool ** len(password)
    seconds = combos / 10_000_000_000 / 2

    if seconds < 1:
        return "کمتر از یک ثانیه"
    if seconds < 60:
        return f"{int(seconds)} ثانیه"
    if seconds < 3600:
        return f"{int(seconds // 60)} دقیقه"
    if seconds < 86400:
        return f"{int(seconds // 3600)} ساعت"
    if seconds < 86400 * 365:
        return f"{int(seconds // 86400)} روز"
    years = seconds / (86400 * 365)
    if years < 1000:
        return f"{int(years)} سال"
    if years < 1_000_000:
        return "هزاران سال"
    return "میلیون‌ها سال"


import secrets


def generate_password(length: int = 16) -> str:
    """یه رمز قوی و تصادفی می‌سازه (حداقل یکی از هر نوع کاراکتر)."""
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*-_?"

    # اول از هر نوع یکی برمی‌داریم تا رمز حتماً قوی باشه
    chars = [
        secrets.choice(lower),
        secrets.choice(upper),
        secrets.choice(digits),
        secrets.choice(symbols),
    ]

    # بقیه‌ی کاراکترها رو از مجموع همه‌ی انواع انتخاب می‌کنیم
    all_chars = lower + upper + digits + symbols
    while len(chars) < length:
        chars.append(secrets.choice(all_chars))

    # ترتیب رو به‌هم می‌ریزیم
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)    