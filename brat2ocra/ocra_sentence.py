from brat2ocra.ocra_token import OcraToken
from typing import List

class OcraSentence:
    index: int
    tokens: List[OcraToken]

    def __init__(self, index: int, tokens: List[OcraToken]):
        self.index = index
        self.tokens = tokens

    def to_dict(self):
        return {
            'index': self.index,
            'tokens': list(map(lambda t: t.to_dict(), self.tokens))
        }