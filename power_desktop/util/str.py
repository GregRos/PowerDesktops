def truncate_text(text: str, max_length: int) -> str:
    if len(text) > max_length:
        return text[: max_length - 1] + "⋯"
    return text


def get_number_emoji(number: int):
    emoji_digits = {
        "0": "0️⃣",
        "1": "1️⃣",
        "2": "2️⃣",
        "3": "3️⃣",
        "4": "4️⃣",
        "5": "5️⃣",
        "6": "6️⃣",
        "7": "7️⃣",
        "8": "8️⃣",
        "9": "9️⃣",
    }

    emoji_number = ""
    for digit in str(number):
        if digit in emoji_digits:
            emoji_number += emoji_digits[digit]
        else:
            emoji_number += digit

    return emoji_number
