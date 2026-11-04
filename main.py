import flet as ft
from checker import check_password

MIN_LEN = 8    # حداقل طول رمز
MAX_LEN = 30   # حداکثر طول رمز


def main(page: ft.Page):
    # ---------- تنظیمات صفحه ----------
    page.title = "بررسی قدرت رمز عبور"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0F172A"                      # پس‌زمینه‌ی سرمه‌ای تیره
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ---------- اجزای صفحه ----------
    title = ft.Text("🔐 بررسی قدرت رمز عبور", size=24, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text("رمزت رو بنویس تا امنیتش رو بسنجیم", size=14, color=ft.Colors.GREY_400)

    password_field = ft.TextField(
        label="رمز عبور",
        password=True,
        can_reveal_password=True,
        max_length=MAX_LEN,          # بیشتر از ۳۰ کاراکتر تایپ نمی‌شه
        border_radius=12,
        border_color=ft.Colors.BLUE_400,
        prefix_icon=ft.Icons.LOCK,
        autofocus=True,
    )

    # پیام هشدار برای کمتر از ۸ کاراکتر
    warning_text = ft.Text("", size=13, color=ft.Colors.AMBER)

    strength_bar = ft.ProgressBar(
        value=0, height=14, bar_height=14, border_radius=7,
        color=ft.Colors.GREY, bgcolor="#1E293B",
    )
    level_text = ft.Text("", size=20, weight=ft.FontWeight.BOLD)
    crack_text = ft.Text("", size=14, color=ft.Colors.GREY_300)
    suggestions_box = ft.Column(spacing=8)

    # ---------- تابعی که با هر تایپ اجرا می‌شه ----------
    def on_change(e):
        pw = password_field.value or ""

        # اگه خالیه، همه‌چیز رو پاک کن
        if not pw:
            warning_text.value = ""
            strength_bar.value = 0
            level_text.value = ""
            crack_text.value = ""
            suggestions_box.controls.clear()
            page.update()
            return

        # هشدار حداقل طول
        if len(pw) < MIN_LEN:
            warning_text.value = f"⚠️ حداقل {MIN_LEN} کاراکتر لازمه ({len(pw)}/{MIN_LEN})"
        else:
            warning_text.value = ""

        result = check_password(pw)

        # رنگ و ایموجی بر اساس سطح
        if result["level"] == "ضعیف":
            color, emoji = ft.Colors.RED_400, "😟"
        elif result["level"] == "متوسط":
            color, emoji = ft.Colors.ORANGE_400, "🙂"
        else:
            color, emoji = ft.Colors.GREEN_400, "😎"

        strength_bar.value = result["score"] / 100
        strength_bar.color = color
        level_text.value = f"{emoji} {result['level']} ({result['score']}/100)"
        level_text.color = color
        crack_text.value = f"⏱ زمان تقریبی شکستن: {result['crack_time']}"

        # ساخت کارت پیشنهادها
        suggestions_box.controls.clear()
        for s in result["suggestions"]:
            suggestions_box.controls.append(
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.LIGHTBULB, color=ft.Colors.AMBER, size=20),
                                    ft.Text(s, size=14, expand=True)]),
                    padding=12,
                    border_radius=12,
                    bgcolor="#1E293B",
                )
            )
        page.update()

    password_field.on_change = on_change

    # ---------- کارت اصلی ----------
    card = ft.Container(
        width=420,
        padding=24,
        border_radius=20,
        bgcolor="#162036",
        content=ft.Column(
            [
                title,
                subtitle,
                ft.Divider(height=10, color="transparent"),
                password_field,
                warning_text,
                strength_bar,
                level_text,
                crack_text,
                ft.Divider(),
                ft.Text("پیشنهادهای امنیتی", size=17, weight=ft.FontWeight.BOLD),
                suggestions_box,
            ],
            spacing=10,
        ),
    )

    page.add(card)


ft.run(main)