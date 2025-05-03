from typing import TypeVar, Optional, Iterable, Generator, Callable


INTERNATIONAL_MORSE_CODES: dict[str, list[int]] = {
    'A': [0, 1],
    'B': [1, 0, 0, 0],
    'C': [1, 0, 1, 0],
    'D': [1, 0, 0],
    'E': [0],
    'F': [0, 0, 1, 0],
    'G': [1, 1, 0],
    'H': [0, 0, 0, 0],
    'I': [0, 0],
    'J': [0, 1, 1, 1],
    'K': [1, 0, 1],
    'L': [0, 1, 0, 0],
    'M': [1, 1],
    'N': [1, 0],
    'O': [1, 1, 1],
    'P': [0, 1, 1, 1, 0],
    'Q': [1, 1, 0, 1],
    'R': [0, 1, 0],
    'S': [0, 0, 0],
    'T': [1],
    'U': [0, 0, 1],
    'V': [0, 0, 0, 1],
    'W': [0, 1, 1],
    'X': [1, 0, 0, 1],
    'Y': [1, 0, 1, 1],
    'Z': [1, 1, 0, 0],
    '1': [0, 1, 1, 1, 1],
    '2': [0, 0, 1, 1, 1],
    '3': [0, 0, 0, 1, 1],
    '4': [0, 0, 0, 0, 1],
    '5': [0, 0, 0, 0, 0],
    '6': [1, 0, 0, 0, 0],
    '7': [1, 1, 0, 0, 0],
    '8': [1, 1, 1, 0, 0],
    '9': [1, 1, 1, 1, 0],
    '0': [1, 1, 1, 1, 1],
    ')': [1, 0, 1, 1, 0, 1],
    '(': [1, 0, 1, 1, 0],
    ',': [1, 1, 0, 0, 1, 1],
    '.': [0, 1, 0, 1, 0, 1]
}


Duration = TypeVar("Duration")
Character = TypeVar("Character")

# Type object of which is convertable to bool, if it gives True - it is dash, otherwise - dot
DotOrDash = TypeVar("DotOrDash")

Signal = TypeVar("Signal")


def encode_character_bits(
    character_bits: Iterable[DotOrDash],
    dit_duration: Duration = 1,
    dah_duration: Optional[Duration] = None,
    absence_duration: Optional[Duration] = None,
    signal_one: Signal = True,
    signal_zero: Signal = False
) -> Generator[tuple[Signal, Duration]]:
    if dah_duration is None:
        dah_duration: Duration = 3 * dit_duration
    
    if absence_duration is None:
        absence_duration: Duration = dit_duration

    is_first_character_bit = True
    for character_bit in character_bits:
        if not is_first_character_bit:
            yield (signal_zero, absence_duration)

        yield (signal_one, dah_duration if character_bit else dit_duration)
        is_first_character_bit = False


def encode_word(
    word: Iterable[Character],
    dit_duration: Duration = 1,
    dah_duration: Optional[Duration] = None,
    absence_duration: Optional[Duration] = None,
    space_duration: Optional[Duration] = None,
    codes: Callable[[Character], Iterable[DotOrDash]] = INTERNATIONAL_MORSE_CODES.get,
    signal_one: Signal = True,
    signal_zero: Signal = False
) -> Generator[tuple[Signal, Duration]]:
    if space_duration is None:
        space_duration: Duration = 3 * dit_duration

    is_first_word_character = True
    for word_character in word:
        if not is_first_word_character:
            yield (signal_zero, space_duration)
        
        yield from encode_character_bits(codes(word_character), dit_duration, dah_duration, absence_duration, signal_one, signal_zero)
        is_first_word_character = False


def encode_words(
    words: Iterable[Iterable[Character]],
    dit_duration: Duration = 1,
    dah_duration: Optional[Duration] = None,
    absence_duration: Optional[Duration] = None,
    space_duration: Optional[Duration] = None,
    separator_duration: Optional[Duration] = None,
    codes: Callable[[Character], Iterable[DotOrDash]] = INTERNATIONAL_MORSE_CODES.get,
    signal_one: Signal = True,
    signal_zero: Signal = False
) -> Generator[tuple[Signal, Duration]]:
    if separator_duration is None:
        separator_duration: Duration = 7 * dit_duration

    is_first_word = True
    for word in words:
        if not is_first_word:
            yield (signal_zero, separator_duration)

        yield from encode_word(word, dit_duration, dah_duration, absence_duration, space_duration, codes, signal_one, signal_zero)
        is_first_word = False
