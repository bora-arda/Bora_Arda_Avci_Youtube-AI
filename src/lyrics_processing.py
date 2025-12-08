import re
import tiktoken
from src.utils import md5_hash


class LyricsProcessor:
    def __init__(self):
        self.encoder = tiktoken.get_encoding("cl100k_base") # Setting encoder using cl100k_base encoding.

    def process(self, lyrics: str) -> dict:
        text = lyrics.strip() # Remove leading and trailing whitespace
        chars = len(text) # Length of text
        words = len(re.findall(r"\w+", text)) # Find matches using regex, total number of words
        tokens = len(self.encoder.encode(text)) # total number of tokens
        tokens_per_word = round(tokens / words, 2) if words > 0 else 0
        hash_value = md5_hash(text)

        return {
            "lyrics_length_chars": chars,
            "lyrics_length_words": words,
            "lyrics_length_tokens": tokens,
            "tokens_per_word": tokens_per_word,
            "lyrics_hash": hash_value
        }
        