import flet as ft
from checker import check_password, generate_password

MIN_LEN = 8    # حداقل طول رمز
MAX_LEN = 30   # حداکثر طول رمز


async def main(page: ft.Page):
    # ---------- تنظیمات صفحه ----------
    page.title = "بررسی قدرت رمز عبور"
    page.rtl = True
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ---------- اجزای صفحه ----------
    title = ft.Text("🔐 بررسی قدرت رمز", size=22, weight=ft.FontWeight.BOLD)
    subtitle = ft.Text(
        "رمزت رو بنویس تا امنیتش رو بسنجیم",
        size=14,
        color=ft.Colors.ON_SURFACE_VARIANT,
    )

    password_field = ft.TextField(
        label="رمز عبور",
        password=True,
        can_reveal_password=True,
        max_length=MAX_LEN,
        border_radius=12,
        border_color=ft.Colors.BLUE_400,
        prefix_icon=ft.Icons.LOCK,
    )

    warning_text = ft.Text("", size=13, color=ft.Colors.AMBER_700)

    strength_bar = ft.ProgressBar(
        value=0, height=14, bar_height=14, border_radius=7,
        color=ft.Colors.GREY, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
    )
    level_text = ft.Text("", size=20, weight=ft.FontWeight.BOLD)
    crack_text = ft.Text("", size=14, color=ft.Colors.ON_SURFACE_VARIANT)
    suggestions_box = ft.Column(spacing=8)

    # ---------- تابعی که با هر تایپ اجرا می‌شه ----------
    def on_change(e=None):
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
                    content=ft.Row([
                        ft.Icon(ft.Icons.LIGHTBULB, color=ft.Colors.AMBER, size=20),
                        ft.Text(s, size=14, expand=True),
                    ]),
                    padding=12,
                    border_radius=12,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                )
            )
        page.update()

    password_field.on_change = on_change

    # ---------- تولید رمز تصادفی ----------
    def generate(e):
        password_field.value = generate_password(16)
        password_field.password = False   # رمز جدید رو نشون بده
        on_change()

    # ---------- کپی رمز ----------
    async def copy_password(e):
        if not password_field.value:
            page.show_dialog(ft.SnackBar("اول یه رمز بنویس یا تولید کن"))
            return
        await ft.Clipboard().set(password_field.value)
        page.show_dialog(ft.SnackBar("✅ رمز کپی شد"))

    # ---------- تغییر تم روشن/تیره ----------
    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_button.icon = ft.Icons.DARK_MODE
        else:
            page.theme_mode = ft.ThemeMode.DARK
            theme_button.icon = ft.Icons.LIGHT_MODE
        page.update()

    theme_button = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        tooltip="تغییر تم",
        on_click=toggle_theme,
    )

    generate_button = ft.Button(
        "تولید رمز قوی", icon=ft.Icons.AUTO_AWESOME, on_click=generate
    )
    copy_button = ft.OutlinedButton(
        "کپی رمز", icon=ft.Icons.COPY, on_click=copy_password
    )

    # ---------- کارت اصلی ----------
    card = ft.Container(
        width=420,
        padding=24,
        border_radius=20,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
        content=ft.Column(
            [
                ft.Row([title, theme_button],
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                subtitle,
                ft.Divider(height=10, color="transparent"),
                password_field,
                warning_text,
                ft.Row([generate_button, copy_button], wrap=True),
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