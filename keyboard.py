from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def basic() -> ReplyKeyboardMarkup:
    btn0 = KeyboardButton(text="Планиметрия")
    btn1 = KeyboardButton(text="Стереометрия")
    btn2 = KeyboardButton(text="Информация")

    markup = ReplyKeyboardMarkup(
        keyboard=[
            [btn0, btn1],
            [btn2]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Выберите раздел..."
    )
    return markup


if __name__ == '__main__':
    markup = basic()
    print(markup.as_json())  