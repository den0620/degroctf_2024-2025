#!/bin/env python3


from morse import encode_words

from socketserver import ForkingTCPServer, BaseRequestHandler
from itertools import cycle, repeat, chain
from time import sleep


ASCII_ART_TEMPLATE: str = r"""
+-----------------+        
| STILL SCREAMING |        
+-----------------+        
                   \       
                    <0)))><
"""
TEMPLATE_REPLACEMENT_STRING: str = "STILL SCREAMING"

FLAG: str = "DEGRO_FISH_SPEAK_UPTO_YOU".replace("_", " ")

FLAG_PROMPT: str = f"{FLAG}"
FLAG_REPEAT_PROMPT: str = ", " + FLAG_PROMPT


def center_text(text: str, width: int, filling_characters: str = ' ') -> str:
    filling_characters_amount: int = width - sum(map(lambda text_charcter: 1 if text_charcter.isprintable() else 0, text))

    return \
        (filling_characters_amount // 2) * filling_characters + \
        text + \
        (filling_characters_amount // 2 + filling_characters_amount % 2) * filling_characters


class FishyServer(ForkingTCPServer):
    class TCPHandler(BaseRequestHandler):
        def handle(self):
            print(f"Client {self.client_address} connected")

            flag_prompt = self.server.flag_prompt
            flag_repeat_prompt = self.server.flag_repeat_prompt
            delay = self.server.delay
            encoding = self.server.encoding

            signal_one = ASCII_ART_TEMPLATE.replace(TEMPLATE_REPLACEMENT_STRING, center_text("SCREAMING\a", len(TEMPLATE_REPLACEMENT_STRING)))
            signal_zero = ASCII_ART_TEMPLATE.replace(TEMPLATE_REPLACEMENT_STRING, center_text("/SILENCE/", len(TEMPLATE_REPLACEMENT_STRING)))
            try:
                last_lines_amount: int = 0
                for signal, signal_duration in encode_words(chain(flag_prompt.split(), cycle(flag_repeat_prompt.split())), signal_one=signal_one, signal_zero=signal_zero):
                    for _ in range(signal_duration):
                        self.request.sendall((last_lines_amount * '\033[A' + signal).encode(encoding))
                        last_lines_amount = signal.count('\n')
                        sleep(delay)
            except (BrokenPipeError, ConnectionResetError):
                print(f"Client {self.client_address} disconnected")
            finally:
                self.request.close()

    def __init__(self, address, flag_prompt: str, flag_repeat_prompt: str, delay: float | int = 1, encoding: str = "utf-8"):
        super().__init__(address, self.TCPHandler)

        self.flag_prompt = flag_prompt
        self.flag_repeat_prompt = flag_repeat_prompt
        self.delay = delay
        self.encoding = encoding


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9998

    with FishyServer((HOST, PORT), FLAG_PROMPT, FLAG_REPEAT_PROMPT, delay=0.05) as server:
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            server.server_close()
