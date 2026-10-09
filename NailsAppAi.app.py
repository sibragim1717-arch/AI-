
import io
import csv
import random
import hashlib
from datetime import datetime

import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageOps

# =========================================================
# AI NAIL STYLIST
# Полный рабочий прототип приложения
# =========================================================

st.set_page_config(
    page_title="AI Nail Stylist",
    page_icon="💅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- ДИЗАЙН ИНТЕРФЕЙСА --------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #fff7fb 0%, #fffafd 100%);
    }
    h1, h2, h3 {
        color: #542744;
    }
    .hero {
        padding: 25px;
        border-radius: 22px;
        background: linear-gradient(120deg, #f8d7e8, #f5e9ff);
        text-align: center;
        margin-bottom: 20px;
    }
    .hero h1 {
        margin-bottom: 5px;
        font-size: 34px;
    }
    .hero p {
        color: #70475f;
        margin-bottom: 0;
    }
    .design-card {
        background: #ffffff;
        padding: 14px;
        border: 1px solid #f0dce8;
        border-radius: 18px;
        margin-bottom: 8px;
    }
    .muted {
        color: #806b79;
        font-size: 13px;
    }
    div.stButton > button {
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- КАТАЛОГ --------------------

DESIGNS = [
    {
        "id": 1, "name": "Классический френч",
        "category": "Френч", "level": "Лёгкий",
        "base": "#F5DDE0", "accent": "#FFFFFF",
        "style": "Классика", "occasion": "На каждый день",
        "length": "Любая", "shape": "Любая",
        "description": "Нежная база и белые кончики.",
        "tags": "нюд, белый, аккуратно, классика",
    },
    {
        "id": 2, "name": "Чёрный френч",
        "category": "Френч", "level": "Средний",
        "base": "#F2DCE2", "accent": "#19151C",
        "style": "Минимализм", "occasion": "Вечер",
        "length": "Средняя", "shape": "Любая",
        "description": "Контрастные чёрные кончики.",
        "tags": "чёрный, контраст, вечер",
    },
    {
        "id": 3, "name": "Розовый френч",
        "category": "Френч", "level": "Лёгкий",
        "base": "#F8E0E9", "accent": "#F28BB7",
        "style": "Романтика", "occasion": "На каждый день",
        "length": "Любая", "shape": "Любая",
        "description": "Мягкий розовый оттенок на кончиках.",
        "tags": "розовый, нежный, романтика",
    },
    {
        "id": 4, "name": "Золотой френч",
        "category": "Френч", "level": "Средний",
        "base": "#F4E4D8", "accent": "#C69A45",
        "style": "Люкс", "occasion": "Вечер",
        "length": "Средняя", "shape": "Любая",
        "description": "Тонкие золотистые кончики.",
        "tags": "золото, роскошь, праздник",
    },
    {
        "id": 5, "name": "Молочная нежность",
        "category": "Нюд", "level": "Лёгкий",
        "base": "#F5E9E1", "accent": "#FFF8F0",
        "style": "Минимализм", "occasion": "На каждый день",
        "length": "Любая", "shape": "Любая",
        "description": "Полупрозрачный молочный оттенок.",
        "tags": "молочный, нежный, минимализм",
    },
    {
        "id": 6, "name": "Пудровый нюд",
        "category": "Нюд", "level": "Лёгкий",
        "base": "#E9BFC6", "accent": "#F9E6E8",
        "style": "Классика", "occasion": "На каждый день",
        "length": "Любая", "shape": "Любая",
        "description": "Пудровый цвет с мягким блеском.",
        "tags": "нюд, пудра, офис",
    },
    {
        "id": 7, "name": "Кофе с молоком",
        "category": "Нюд", "level": "Лёгкий",
        "base": "#B98A77", "accent": "#E9D1BF",
        "style": "Классика", "occasion": "На каждый день",
        "length": "Любая", "shape": "Любая",
        "description": "Тёплый кофейный оттенок.",
        "tags": "коричневый, кофе, осень",
    },
    {
        "id": 8, "name": "Шоколадный глянец",
        "category": "Однотонный", "level": "Лёгкий",
        "base": "#512D32", "accent": "#9C6067",
        "style": "Люкс", "occasion": "Вечер",
        "length": "Любая", "shape": "Любая",
        "description": "Глубокий шоколадный цвет.",
        "tags": "шоколад, коричневый, глянец",
    },
    {
        "id": 9, "name": "Красная классика",
        "category": "Однотонный", "level": "Лёгкий",
        "base": "#C51435", "accent": "#F55A6C",
        "style": "Классика", "occasion": "Вечер",
        "length": "Любая", "shape": "Любая",
        "description": "Насыщенный красный лак.",
        "tags": "красный, классика, яркий",
    },
    {
        "id": 10, "name": "Бордовый бархат",
        "category": "Однотонный", "level": "Лёгкий",
        "base": "#6E1237", "accent": "#B63B65",
        "style": "Люкс", "occasion": "Вечер",
        "length": "Любая", "shape": "Любая",
        "description": "Благородный винный оттенок.",
        "tags": "бордо, винный, люкс",
    },
    {
        "id": 11, "name": "Чёрный глянец",
        "category": "Однотонный", "level": "Лёгкий",
        "base": "#17151D", "accent": "#77717E",
        "style": "Минимализм", "occasion": "Вечер",
        "length": "Любая", "shape": "Любая",
        "description": "Глубокий чёрный с бликом.",
        "tags": "чёрный, готика, вечер",
    },
    {
        "id": 12, "name": "Небесно-голубой",
        "category": "Однотонный", "level": "Лёгкий",
        "base": "#91D4F3", "accent": "#DDF5FF",
        "style": "Нежный", "occasion": "Лето",
        "length": "Любая", "shape": "Любая",
        "description": "Свежий пастельный голубой.",
        "tags": "голубой, лето, пастель",
    },
    {
        "id": 13, "name": "Лавандовый сон",
        "category": "Однотонный", "level": "Лёгкий",
        "base": "#B9A0E8", "accent": "#E8DEFF",
        "style": "Нежный", "occasion": "На каждый день",
        "length": "Любая", "shape": "Любая",
        "description": "Мягкий лавандовый оттенок.",
        "tags": "лаванда, фиолетовый, пастель",
    },
    {
        "id": 14, "name": "Мятное настроение",
        "category": "Однотонный", "level": "Лёгкий",
        "base": "#9DDFC9", "accent": "#E1FFF4",
        "style": "Нежный", "occasion": "Лето",
        "length": "Любая", "shape": "Любая",
        "description": "Светлый мятный цвет.",
        "tags": "мята, зелёный, лето",
    },
    {
        "id": 15, "name": "Жемчужный хром",
        "category": "Хром", "level": "Средний",
        "base": "#E7E4EB", "accent": "#FFFFFF",
        "style": "Люкс", "occasion": "Вечер",
        "length": "Средняя", "shape": "Любая",
        "description": "Светлый жемчужный металлический эффект.",
        "tags": "хром, жемчуг, сияние",
    },
    {
        "id": 16, "name": "Розовое зеркало",
        "category": "Хром", "level": "Средний",
        "base": "#D78BAF", "accent": "#F8D7E8",
        "style": "Люкс", "occasion": "Вечер",
        "length": "Средняя", "shape": "Любая",
        "description": "Розовый зеркальный эффект.",
        "tags": "хром, розовый, блеск",
    },
    {
        "id": 17, "name": "Золотое зеркало",
        "category": "Хром", "level": "Средний",
        "base": "#C49A42", "accent": "#F9E4A8",
        "style": "Люкс", "occasion": "Праздник",
        "length": "Средняя", "shape": "Любая",
        "description": "Металлическое золотое покрытие.",
        "tags": "золото, хром, праздник",
    },
    {
        "id": 18, "name": "Радужное сияние",
        "category": "Хром", "level": "Сложный",
        "base": "#B8A8DB", "accent": "#F8D8EE",
        "style": "Яркий", "occasion": "Праздник",
        "length": "Средняя", "shape": "Любая",
        "description": "Переливчатая фантазийная палитра.",
        "tags": "радуга, сияние, необычный",
    },
    {
        "id": 19, "name": "Розовое омбре",
        "category": "Омбре", "level": "Средний",
        "base": "#E88AB5", "accent": "#FFF0F5",
        "style": "Романтика", "occasion": "На каждый день",
        "length": "Средняя", "shape": "Любая",
        "description": "Переход от розового к молочному.",
        "tags": "омбре, розовый, градиент",
    },
    {
        "id": 20, "name": "Закатное омбре",
        "category": "Омбре", "level": "Сложный",
        "base": "#F08062", "accent": "#FFD17C",
        "style": "Яркий", "occasion": "Лето",
        "length": "Средняя", "shape": "Любая",
        "description": "Тёплый градиент в цветах заката.",
        "tags": "закат, оранжевый, лето",
    },
    {
        "id": 21, "name": "Ледяное омбре",
        "category": "Омбре", "level": "Средний",
        "base": "#80C9EA", "accent": "#F8FFFF",
        "style": "Нежный", "occasion": "Зима",
        "length": "Средняя", "shape": "Любая",
        "description": "Холодный голубой переход.",
        "tags": "голубой, зима, градиент",
    },
    {
        "id": 22, "name": "Маленькие цветы",
        "category": "Цветы", "level": "Средний",
        "base": "#FFF0E8", "accent": "#E96B9C",
        "style": "Романтика", "occasion": "Весна",
        "length": "Любая", "shape": "Любая",
        "description": "Миниатюрные цветочные мотивы.",
        "tags": "цветы, весна, романтика",
    },
    {
        "id": 23, "name": "Ромашковое поле",
        "category": "Цветы", "level": "Средний",
        "base": "#BDE4B4", "accent": "#FFFFFF",
        "style": "Нежный", "occasion": "Лето",
        "length": "Любая", "shape": "Любая",
        "description": "Светлые ромашки на пастельном фоне.",
        "tags": "ромашка, цветы, лето",
    },
    {
        "id": 24, "name": "Вишнёвый цвет",
        "category": "Цветы", "level": "Сложный",
        "base": "#F5DDE5", "accent": "#D46B91",
        "style": "Романтика", "occasion": "Весна",
        "length": "Средняя", "shape": "Любая",
        "description": "Деликатные цветочные детали.",
        "tags": "сакура, розовый, цветы",
    },
    {
        "id": 25, "name": "Звёздная ночь",
        "category": "Геометрия", "level": "Средний",
        "base": "#20223F", "accent": "#F7D879",
        "style": "Яркий", "occasion": "Вечер",
        "length": "Средняя", "shape": "Любая",
        "description": "Звёзды и золотистые акценты.",
        "tags": "звёзды, ночь, золото",
    },
    {
        "id": 26, "name": "Тонкие линии",
        "category": "Геометрия", "level": "Средний",
        "base": "#F8F0EA", "accent": "#29242A",
        "style": "Минимализм", "occasion": "На каждый день",
        "length": "Любая", "shape": "Любая",
        "description": "Лаконичные графичные линии.",
        "tags": "линии, минимализм, геометрия",
    },
    {
        "id": 27, "name": "Шахматный узор",
        "category": "Геометрия", "level": "Сложный",
        "base": "#FFFFFF", "accent": "#29252D",
        "style": "Яркий", "occasion": "Вечер",
        "length": "Средняя", "shape": "Любая",
        "description": "Контрастная чёрно-белая клетка.",
        "tags": "шахматы, клетка, графика",
    },
    {
        "id": 28, "name": "Золотая фольга",
        "category": "Декор", "level": "Средний",
        "base": "#F3DDE0", "accent": "#C99A42",
        "style": "Люкс", "occasion": "Праздник",
        "length": "Любая", "shape": "Любая",
        "description": "Нюдовая основа с золотыми фрагментами.",
        "tags": "фольга, золото, люкс",
    },
    {
        "id": 29, "name": "Стразы и блеск",
        "category": "Декор", "level": "Сложный",
        "base": "#E8C9DA", "accent": "#FFFFFF",
        "style": "Люкс", "occasion": "Праздник",
        "length": "Средняя", "shape": "Любая",
        "description": "Акцентные блестящие детали.",
        "tags": "стразы, блеск, праздник",
    },
    {
        "id": 30, "name": "Мрамор",
        "category": "Декор", "level": "Сложный",
        "base": "#F1F0ED", "accent": "#777780",
        "style": "Люкс", "occasion": "Вечер",
        "length": "Средняя", "shape": "Любая",
        "description": "Мраморные прожилки на светлой основе.",
        "tags": "мрамор, серый, камень",
    },
    {
        "id": 31, "name": "Черепаховый принт",
        "category": "Принт", "level": "Сложный",
        "base": "#6E402D", "accent": "#D8A15E",
        "style": "Люкс", "occasion": "Осень",
        "length": "Средняя", "shape": "Любая",
        "description": "Коричнево-карамельный принт.",
        "tags": "принт, черепаха, коричневый",
    },
    {
        "id": 32, "name": "Леопард",
        "category": "Принт", "level": "Сложный",
        "base": "#D9B17A", "accent": "#392820",
        "style": "Яркий", "occasion": "Вечер",
        "length": "Средняя", "shape": "Любая",
        "description": "Животный принт с контрастными пятнами.",
        "tags": "леопард, принт, яркий",
    },
    {
        "id": 33, "name": "Сердечки",
        "category": "Романтика", "level": "Средний",
        "base": "#FFE7EE", "accent": "#E64D7A",
        "style": "Романтика", "occasion": "Свидание",
        "length": "Любая", "shape": "Любая",
        "description": "Маленькие сердечки на нежной основе.",
        "tags": "сердце, любовь, розовый",
    },
    {
        "id": 34, "name": "Вишенки",
        "category": "Романтика", "level": "Средний",
        "base": "#FFF0E8", "accent": "#D42D4E",
        "style": "Яркий", "occasion": "Лето",
        "length": "Любая", "shape": "Любая",
        "description": "Игривый принт с маленькими вишнями.",
        "tags": "вишня, лето, красный",
    },
    {
        "id": 35, "name": "Снежинки",
        "category": "Сезонный", "level": "Средний",
        "base": "#A8D5ED", "accent": "#FFFFFF",
        "style": "Нежный", "occasion": "Зима",
        "length": "Любая", "shape": "Любая",
        "description": "Зимний дизайн со снежинками.",
        "tags": "снег, зима, снежинки",
    },
    {
        "id": 36, "name": "Новогодний блеск",
        "category": "Сезонный", "level": "Средний",
        "base": "#1D634B", "accent": "#D9B75D",
        "style": "Праздничный", "occasion": "Новый год",
        "length": "Любая", "shape": "Любая",
        "description": "Зелёная основа с золотыми акцентами.",
        "tags": "новый год, зелёный, золото",
    },
    {
        "id": 37, "name": "Хэллоуин",
        "category": "Сезонный", "level": "Сложный",
        "base": "#281C35", "accent": "#FF8C32",
        "style": "Яркий", "occasion": "Хэллоуин",
        "length": "Средняя", "shape": "Любая",
        "description": "Тёмная основа с оранжевыми акцентами.",
        "tags": "хэллоуин, тыква, чёрный",
    },
    {
        "id": 38, "name": "Летний неон",
        "category": "Яркий", "level": "Средний",
        "base": "#D4F14A", "accent": "#FF4FA3",
        "style": "Яркий", "occasion": "Лето",
        "length": "Любая", "shape": "Любая",
        "description": "Неоновые цвета для яркого образа.",
        "tags": "неон, лето, яркий",
    },
    {
        "id": 39, "name": "Сиреневый градиент",
        "category": "Омбре", "level": "Средний",
        "base": "#9774D4", "accent": "#F1E7FF",
        "style": "Нежный", "occasion": "На каждый день",
        "length": "Средняя", "shape": "Любая",
        "description": "Сиреневый переход с мягким финишем.",
        "tags": "сиреневый, омбре, градиент",
    },
    {
        "id": 40, "name": "Голубой хром",
        "category": "Хром", "level": "Средний",
        "base": "#6EA7D9", "accent": "#DDF4FF",
        "style": "Люкс", "occasion": "Вечер",
        "length": "Средняя", "shape": "Любая",
        "description": "Холодный металлический голубой.",
        "tags": "голубой, хром, металл",
    },
]

# -------------------- ГЕНЕРАЦИЯ ПРЕВЬЮ --------------------

def hex_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def draw_design(design, size=(360, 230)):
    """Создаёт иллюстрацию дизайна, а не примерку на реальную руку."""
    width, height = size
    image = Image.new("RGB", size, (255, 247, 251))
    draw = ImageDraw.Draw(image)

    base = hex_rgb(design["base"])
    accent = hex_rgb(design["accent"])

    # Мягкий декоративный фон
    draw.ellipse(
        (-50, -70, 150, 130),
        fill=(250, 231, 242),
    )
    draw.ellipse(
        (width - 130, height - 100, width + 50, height + 70),
        fill=(242, 229, 250),
    )

    nail_width = 48
    nail_height = 105
    gap = 14
    total = nail_width * 5 + gap * 4
    start_x = (width - total) // 2
    top_y = 45

    style = design["category"].lower()

    for index in range(5):
        x = start_x + index * (nail_width + gap)
        y = top_y + (index % 2) * 7

        # Ноготь с закруглёнными углами
        draw.rounded_rectangle(
            (x, y, x + nail_width, y + nail_height),
            radius=22,
            fill=base,
            outline=(224, 197, 211),
            width=2,
        )

        # Декоративные элементы по категории
        if "френч" in style:
            draw.arc(
                (x + 3, y + 2, x + nail_width - 3, y + 30),
                start=0,
                end=180,
                fill=accent,
                width=7,
            )
            draw.line(
                (x + 7, y + 15, x + nail_width - 7, y + 15),
                fill=accent,
                width=4,
            )

        elif "омбре" in style:
            for line in range(18):
                blend = line / 18
                color = tuple(
                    int(base[c] * (1 - blend) + accent[c] * blend)
                    for c in range(3)
                )
                yy = y + 35 + line * 3
                draw.line(
                    (x + 3, yy, x + nail_width - 3, yy),
                    fill=color,
                    width=3,
                )

        elif "цвет" in style or "романтика" in style:
            cx = x + nail_width // 2
            cy = y + nail_height // 2
            for angle_x, angle_y in [
                (0, -9), (8, 0), (0, 9), (-8, 0)
            ]:
                draw.ellipse(
                    (
                        cx + angle_x - 5,
                        cy + angle_y - 5,
                        cx + angle_x + 5,
                        cy + angle_y + 5,
                    ),
                    fill=accent,
                )
            draw.ellipse(
                (cx - 4, cy - 4, cx + 4, cy + 4),
                fill=(255, 215, 80),
            )

        elif "геометрия" in style:
            draw.line(
                (x + 7, y + 30, x + nail_width - 7, y + 75),
                fill=accent,
                width=3,
            )
            draw.line(
                (x + nail_width - 7, y + 30, x + 7, y + 75),
                fill=accent,
                width=2,
            )

        elif "хром" in style:
            draw.line(
                (x + 10, y + 10, x + 17, y + 88),
                fill=accent,
                width=5,
            )
            draw.line(
                (x + 25, y + 8, x + 31, y + 86),
                fill=(255, 255, 255),
                width=3,
            )

        elif "декор" in style:
            for dot_y in (y + 35, y + 50, y + 65):
                draw.ellipse(
                    (x + 18, dot_y, x + 27, dot_y + 9),
                    fill=accent,
                    outline=(255, 255, 255),
                )

        elif "принт" in style:
            for dot_y in (y + 25, y + 50, y + 75):
                draw.ellipse(
                    (x + 7, dot_y, x + 22, dot_y + 13),
                    fill=accent,
                )
                draw.ellipse(
                    (x + 25, dot_y + 7, x + 39, dot_y + 19),
                    fill=(40, 30, 25),
                )

        elif "сезонный" in style:
            draw.line(
                (x + 24, y + 28, x + 24, y + 75),
                fill=accent,
                width=3,
            )
            draw.line(
                (x + 10, y + 40, x + 38, y + 62),
                fill=accent,
                width=3,
            )
            draw.line(
                (x + 38, y + 40, x + 10, y + 62),
                fill=accent,
                width=3,
            )

        elif "яркий" in style:
            draw.line(
                (x + 8, y + 25, x + 40, y + 25),
                fill=accent,
                width=5,
            )
            draw.line(
                (x + 8, y + 55, x + 40, y + 55),
                fill=accent,
                width=5,
            )

        # Блик лака
        draw.line(
            (x + 9, y + 14, x + 9, y + 31),
            fill=(255, 255, 255),
            width=3,
        )

    return image


# -------------------- СОСТОЯНИЕ ПРИЛОЖЕНИЯ --------------------

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "recently_viewed" not in st.session_state:
    st.session_state.recently_viewed = []

if "photo_bytes" not in st.session_state:
    st.session_state.photo_bytes = None

# -------------------- ЗАГОЛОВОК --------------------

st.markdown(
    """
    <div class="hero">
        <h1>💅 AI Nail Stylist</h1>
        <p>Ваш каталог идей для идеального маникюра</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    "Выбирайте стиль, сохраняйте идеи и создавайте собственную "
    "коллекцию дизайнов."
)

# -------------------- БОКОВОЕ МЕНЮ --------------------

with st.sidebar:
    st.title("✨ Меню")

    page = st.radio(
        "Раздел",
        [
            "Каталог дизайнов",
            "Фото и камера",
            "Подбор дизайна",
            "Избранное",
            "Случайная идея",
            "О приложении",
        ],
    )

    st.divider()
    st.metric("Дизайнов в каталоге", len(DESIGNS))
    st.metric("В избранном", len(st.session_state.favorites))

# -------------------- КАТАЛОГ --------------------

if page == "Каталог дизайнов":
    st.header("Коллекция дизайнов")
    st.write("Используйте фильтры, чтобы найти подходящий вариант.")

    search = st.text_input(
        "🔎 Поиск",
        placeholder="Например: френч, золото, розовый, омбре",
    )

    col1, col2, col3 = st.columns(3)

    categories = ["Все"] + sorted(
        set(item["category"] for item in DESIGNS)
    )
    styles = ["Все"] + sorted(
        set(item["style"] for item in DESIGNS)
    )
    occasions = ["Все"] + sorted(
        set(item["occasion"] for item in DESIGNS)
    )

    with col1:
        chosen_category = st.selectbox("Категория", categories)

    with col2:
        chosen_style = st.selectbox("Стиль", styles)

    with col3:
        chosen_occasion = st.selectbox("Повод", occasions)

    level = st.selectbox(
        "Сложность выполнения",
        ["Любая", "Лёгкий", "Средний", "Сложный"],
    )

    results = []

    for design in DESIGNS:
        searchable = " ".join(
            [
                design["name"],
                design["category"],
                design["style"],
                design["occasion"],
                design["description"],
                design["tags"],
            ]
        ).lower()

        if search.strip() and search.lower() not in searchable:
            continue

        if chosen_category != "Все":
            if design["category"] != chosen_category:
                continue

        if chosen_style != "Все":
            if design["style"] != chosen_style:
                continue

        if chosen_occasion != "Все":
            if design["occasion"] != chosen_occasion:
                continue

        if level != "Любая" and design["level"] != level:
            continue

        results.append(design)

    st.write(f"Найдено дизайнов: **{len(results)}**")

    if not results:
        st.info("Ничего не найдено. Измените фильтры или поисковый запрос.")

    for start in range(0, len(results), 3):
        columns = st.columns(3)

        for column, design in zip(columns, results[start:start + 3]):
            with column:
                st.image(
                    draw_design(design),
                    use_container_width=True,
                )
                st.subheader(design["name"])
                st.caption(
                    f'{design["category"]} • {design["level"]}'
                )
                st.write(design["description"])
                st.caption(
                    f'Стиль: {design["style"]} · '
                    f'Повод: {design["occasion"]}'
                )

                if design["id"] in st.session_state.favorites:
                    button_label = "💗 Убрать из избранного"
                else:
                    button_label = "♡ В избранное"

                if st.button(
                    button_label,
                    key=f"fav_catalog_{design['id']}",
                    use_container_width=True,
                ):
                    if design["id"] in st.session_state.favorites:
                        st.session_state.favorites.remove(design["id"])
                    else:
                        st.session_state.favorites.append(design["id"])
                    st.rerun()

                if st.button(
                    "Подробнее",
                    key=f"details_{design['id']}",
                    use_container_width=True,
                ):
                    st.session_state.selected_design = design["id"]
                    st.session_state.page_details = True
                    st.rerun()

    if st.session_state.get("page_details", False):
        selected_id = st.session_state.get("selected_design")
        selected = next(
            (d for d in DESIGNS if d["id"] == selected_id),
            None,
        )

        if selected:
            st.divider()
            st.header(f'Подробнее: {selected["name"]}')
            st.image(draw_design(selected), width=420)
            st.write(selected["description"])
            st.write(f'Категория: {selected["category"]}')
            st.write(f'Стиль: {selected["style"]}')
            st.write(f'Сложность: {selected["level"]}')
            st.write(f'Повод: {selected["occasion"]}')
            st.write(f'Ключевые слова: {selected["tags"]}')

            if st.button("Закрыть описание"):
                st.session_state.page_details = False
                st.rerun()

    # Экспорт полного каталога
    export_df = pd.DataFrame(DESIGNS)
    st.download_button(
        "⬇️ Скачать каталог в CSV",
        data=export_df.to_csv(index=False).encode("utf-8-sig"),
        file_name="nail_design_catalog.csv",
        mime="text/csv",
    )

# -------------------- ФОТО И КАМЕРА --------------------

elif page == "Фото и камера":
    st.header("📸 Фото ногтей")
    st.write(
        "Загрузите фотографию из галереи или сделайте снимок камерой."
    )

    upload_col, camera_col = st.columns(2)

    with upload_col:
        uploaded = st.file_uploader(
            "Выбрать фото из галереи",
            type=["jpg", "jpeg", "png", "webp"],
        )

    with camera_col:
        camera_photo = st.camera_input("Сделать фото")

    photo = camera_photo if camera_photo is not None else uploaded

    if photo is not None:
        try:
            image = Image.open(photo)
            image = ImageOps.exif_transpose(image).convert("RGB")

            # Ограничиваем размер для более быстрой работы
            image.thumbnail((1600, 1600))

            st.session_state.photo_bytes = image.copy()

            st.success("Фото загружено!")
            st.image(
                image,
                caption="Ваша фотография",
                use_container_width=True,
            )

            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=92)

            st.download_button(
                "⬇️ Скачать фотографию",
                data=buffer.getvalue(),
                file_name="my_nails_photo.jpg",
                mime="image/jpeg",
            )

            st.info(
                "Фото сохранено только в текущем сеансе приложения. "
                "Автоматическое распознавание ногтевых пластин и точное "
                "наложение дизайна на фото пока не реализованы."
            )

        except Exception as error:
            st.error(f"Не удалось обработать изображение: {error}")

    elif st.session_state.photo_bytes is not None:
        st.image(
            st.session_state.photo_bytes,
            caption="Последнее загруженное фото в текущем сеансе",
            use_container_width=True,
        )
    else:
        st.info("Сначала выберите фото или сделайте снимок.")

# -------------------- ПОДБОР ДИЗАЙНА --------------------

elif page == "Подбор дизайна":
    st.header("✨ Подбор маникюра")
    st.write("Ответьте на несколько вопросов, и каталог покажет подходящие идеи.")

    preferred_style = st.selectbox(
        "Какой стиль вам нравится?",
        [
            "Неважно",
            "Классика",
            "Минимализм",
            "Люкс",
            "Нежный",
            "Романтика",
            "Яркий",
            "Праздничный",
        ],
    )

    preferred_occasion = st.selectbox(
        "Для какого случая?",
        [
            "Любой повод",
            "На каждый день",
            "Работа",
            "Свидание",
            "Вечер",
            "Праздник",
            "Лето",
            "Весна",
            "Осень",
            "Зима",
            "Новый год",
            "Хэллоуин",
        ],
    )

    preferred_length = st.selectbox(
        "Длина ногтей",
        ["Любая", "Короткая", "Средняя", "Длинная"],
    )

    preferred_shape = st.selectbox(
        "Форма ногтей",
        ["Любая", "Овал", "Миндаль", "Квадрат", "Мягкий квадрат"],
    )

    preferred_color = st.selectbox(
        "Предпочитаемая цветовая гамма",
        [
            "Любая",
            "Нюдовая",
            "Розовая",
            "Красная",
            "Тёмная",
            "Светлая",
            "Голубая",
            "Зелёная",
            "Фиолетовая",
            "Золотая",
        ],
    )

    if st.button("Подобрать дизайны", type="primary"):
        recommendations = []

        for design in DESIGNS:
            score = 0
            text_to_check = (
                design["name"] + " " + design["tags"] + " "
                + design["category"] + " " + design["base"]
            ).lower()

            if preferred_style != "Неважно":
                if design["style"] == preferred_style:
                    score += 3

            if preferred_occasion != "Любой повод":
                if design["occasion"] == preferred_occasion:
                    score += 3
                elif preferred_occasion == "Работа":
                    if design["style"] in ["Классика", "Минимализм"]:
                        score += 2

            if preferred_length == "Любая":
                score += 1
            elif preferred_length == "Короткая":
                if design["level"] == "Лёгкий":
                    score += 2
            elif preferred_length == "Средняя":
                if design["length"] in ["Средняя", "Любая"]:
                    score += 2
            elif preferred_length == "Длинная":
                if design["level"] in ["Средний", "Сложный"]:
                    score += 2

            if preferred_color != "Любая":
                color_terms = {
                    "Нюдовая": ["нюд", "молочный", "пудра", "кофе"],
                    "Розовая": ["розовый", "розовая", "пудра", "сердце"],
                    "Красная": ["красный", "красная", "бордо", "вишня"],
                    "Тёмная": ["чёрный", "черный", "бордо", "ночь", "шоколад"],
                    "Светлая": ["белый", "молочный", "жемчуг", "пастель"],
                    "Голубая": ["голубой", "голубая", "ледяное"],
                    "Зелёная": ["зелёный", "зелёная", "мятный", "мята"],
                    "Фиолетовая": ["фиолетовый", "лаванда", "сиреневый"],
                    "Золотая": ["золото", "золотой", "золотая"],
                }
                terms = color_terms.get(preferred_color, [])
                if any(term in text_to_check for term in terms):
                    score += 3

            recommendations.append((score, design))

        recommendations.sort(key=lambda item: item[0], reverse=True)
        best = [item[1] for item in recommendations[:9]]

        if best:
            st.subheader("Ваши идеи")
            for start in range(0, len(best), 3):
                cols = st.columns(3)
                for col, design in zip(cols, best[start:start + 3]):
                    with col:
                        st.image(draw_design(design), use_container_width=True)
                        st.markdown(f'**{design["name"]}**')
                        st.caption(
                            f'{design["category"]} · {design["style"]}'
                        )
                        st.write(design["description"])

                        if st.button(
                            "♡ Сохранить",
                            key=f"fav_recommend_{design['id']}",
                        ):
                            if design["id"] not in st.session_state.favorites:
                                st.session_state.favorites.append(design["id"])
                            st.rerun()

        st.caption(
            "Результаты — рекомендации по вашим ответам, а не диагноз "
            "и не автоматический анализ фотографии."
        )

# -------------------- ИЗБРАННОЕ --------------------

elif page == "Избранное":
    st.header("💗 Мои любимые дизайны")

    favorites = [
        design for design in DESIGNS
        if design["id"] in st.session_state.favorites
    ]

    if not favorites:
        st.info(
            "Здесь пока пусто. Откройте каталог и нажмите "
            "«В избранное» на понравившемся дизайне."
        )
    else:
        st.write(f"Сохранено дизайнов: {len(favorites)}")

        for start in range(0, len(favorites), 3):
            cols = st.columns(3)

            for col, design in zip(cols, favorites[start:start + 3]):
                with col:
                    st.image(draw_design(design), use_container_width=True)
                    st.subheader(design["name"])
                    st.caption(design["category"])
                    st.write(design["description"])

                    if st.button(
                        "Убрать из избранного",
                        key=f"remove_fav_{design['id']}",
                    ):
                        st.session_state.favorites.remove(design["id"])
                        st.rerun()

        fav_df = pd.DataFrame(favorites)
        st.download_button(
            "⬇️ Скачать избранное в CSV",
            data=fav_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="my_favorite_nail_designs.csv",
            mime="text/csv",
        )

# -------------------- СЛУЧАЙНАЯ ИДЕЯ --------------------

elif page == "Случайная идея":
    st.header("🎲 Вдохновение дня")
    st.write("Не знаете, какой маникюр выбрать? Доверьтесь случаю.")

    if st.button("Подобрать случайный дизайн", type="primary"):
        design = random.choice(DESIGNS)
        st.session_state.random_design_id = design["id"]

    selected_id = st.session_state.get("random_design_id")
    selected = next(
        (d for d in DESIGNS if d["id"] == selected_id),
        None,
    )

    if selected:
        st.image(draw_design(selected), width=500)
        st.subheader(selected["name"])
        st.write(selected["description"])
        st.write(f'Категория: {selected["category"]}')
        st.write(f'Стиль: {selected["style"]}')
        st.write(f'Сложность: {selected["level"]}')

        if selected["id"] not in st.session_state.favorites:
            if st.button("♡ Добавить в избранное", key="random_favorite"):
                st.session_state.favorites.append(selected["id"])
                st.rerun()

# -------------------- О ПРИЛОЖЕНИИ --------------------

elif page == "О приложении":
    st.header("О проекте AI Nail Stylist")

    st.write(
        """
        **AI Nail Stylist** — прототип помощника для поиска идей маникюра.

        В текущей версии доступны:
        - каталог из 40 дизайнов;
        - фильтры по категориям, стилю, случаю и сложности;
        - поиск по названию и ключевым словам;
        - загрузка фотографии и съёмка камерой;
        - подбор рекомендаций по предпочтениям;
        - список избранного;
        - случайная идея;
        - экспорт каталога и избранного в CSV.
        """
    )

    st.warning(
        "Иллюстрации в каталоге — демонстрационные эскизы. "
        "Приложение пока не распознаёт контур каждого ногтя и не "
        "переносит рисунок на реальные ногтевые пластины."
    )

    st.caption(
        "Версия 1.0 · "
        + datetime.now().strftime("%Y")
    )

st.divider()
st.caption("AI Nail Stylist · Идеи для вашего следующего маникюра 💅")
