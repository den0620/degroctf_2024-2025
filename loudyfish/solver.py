#!/bin/env python3

from morse import INTERNATIONAL_MORSE_CODES

import socket


HOST = "127.0.0.1"
PORT = 9998

IMAGE_LENGTH = 386

bits_sequence: str = str()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for bit in range(IMAGE_LENGTH):
        data = s.recv(1024).decode("utf-8")
        bits_sequence = bits_sequence + ('1' if data.count('\a') > 0 else '0')


def decode_bits(bits):
    # Remove leading and trailing zeros
    bits = bits.strip('0')
    
    # Find the length of the shortest sequence of consecutive 1s or 0s
    time_units = []
    count = 1
    prev = bits[0]
    
    for bit in bits[1:]:
        if bit == prev:
            count += 1
        else:
            time_units.append(count)
            count = 1
            prev = bit
    time_units.append(count)
    
    unit = min(time_units)
    
    # Decode the bits to Morse code
    morse_code = ''
    i = 0
    
    while i < len(bits):
        if bits[i] == '1':
            length = 0
            while i < len(bits) and bits[i] == '1':
                length += 1
                i += 1
            if length // unit == 1:
                morse_code += '.'
            elif length // unit == 3:
                morse_code += '-'
        else:
            length = 0
            while i < len(bits) and bits[i] == '0':
                length += 1
                i += 1
            if length // unit == 1:
                morse_code += ''
            elif length // unit == 3:
                morse_code += ' '
            elif length // unit == 7:
                morse_code += '   '
                
    return morse_code


MORSE_CODE_DICT = {
    str().join(map(lambda bit: '-' if bit == 1 else '.', code)): character for character, code in INTERNATIONAL_MORSE_CODES.items()
}

def decode_morse(morse_code):
    morseCode = morse_code.strip()
    words = morse_code.split('   ')
    decoded_message = []
    
    for word in words:
        characters = word.split(' ')
        decoded_word = ''.join(MORSE_CODE_DICT.get(char, '') for char in characters)
        decoded_message.append(decoded_word)
    
    return ' '.join(decoded_message)


morse_code = decode_bits(bits_sequence)
print(morse_code)
decoded_message = decode_morse(morse_code)
print(decoded_message)
