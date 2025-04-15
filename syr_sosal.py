# Translated to python from https://github.com/paulgb/emoji-encoder/blob/main/app/encoding.ts

VARIATION_SELECTOR_START = 0xFE00
VARIATION_SELECTOR_END = 0xFE0F

VARIATION_SELECTOR_SUPPLEMENT_START = 0xE0100
VARIATION_SELECTOR_SUPPLEMENT_END = 0xE01EF


def to_variation_selector(byte: int) -> str | None:
    if 0 <= byte < 16:
        return chr(VARIATION_SELECTOR_START + byte)
    elif 16 <= byte < 256:
        return chr(VARIATION_SELECTOR_SUPPLEMENT_START + (byte - 16))
    else:
        return None


def from_variation_selector(code_point: int) -> int | None:
    if VARIATION_SELECTOR_START <= code_point <= VARIATION_SELECTOR_END:
        return code_point - VARIATION_SELECTOR_START
    elif VARIATION_SELECTOR_SUPPLEMENT_START <= code_point <= VARIATION_SELECTOR_SUPPLEMENT_END:
        return (code_point - VARIATION_SELECTOR_SUPPLEMENT_START) + 16
    else:
        return None


def encode(emoji: str, text: str) -> str:
    encoded = emoji
    for byte in text.encode('utf-8'):
        vs = to_variation_selector(byte)
        if vs:
            encoded += vs
    return encoded


def decode(text: str) -> str:
    decoded_bytes = []
    for char in text:
        code_point = ord(char)
        byte = from_variation_selector(code_point)
        if byte is None and decoded_bytes:
            break
        elif byte is None:
            continue
        decoded_bytes.append(byte)

    return bytes(decoded_bytes).decode('utf-8')


# === DEMO ===
if __name__ == "__main__":
    string = "🧀🍔"
    secret = "degro_americans_be_eating_cheesed_burghas"
    print("Original Text:", secret)

    encoded = encode(string, secret)
    print("Encoded:", encoded)

    decoded = decode(encoded)
    print("Decoded:", decoded)
