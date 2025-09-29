def truncate_text(text: str, max_length: int) -> str:
    if len(text) > max_length:
        return text[: max_length - 1] + "⋯"
    return text
