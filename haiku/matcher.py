from collections import deque
from dataclasses import dataclass


@dataclass
class Post:
    uri: str
    text: str
    syllables: int


@dataclass
class Haiku:
    line1: Post
    line2: Post
    line3: Post

    def __str__(self) -> str:
        return f"{self.line1.text}\n{self.line2.text}\n{self.line3.text}"


class HaikuMatcher:
    def __init__(self, buffer_size: int = 100):
        self.fives: deque[Post] = deque(maxlen=2 * buffer_size)
        self.sevens: deque[Post] = deque(maxlen=buffer_size)

    def add_post(self, uri: str, text: str, syllables: int) -> Haiku | None:
        post = Post(uri=uri, text=text, syllables=syllables)

        if syllables == 5:
            self.fives.append(post)
        elif syllables == 7:
            self.sevens.append(post)

        return self._try_match()

    def _try_match(self) -> Haiku | None:
        if len(self.fives) >= 2 and len(self.sevens) >= 1:
            line1 = self.fives.popleft()
            line2 = self.sevens.popleft()
            line3 = self.fives.popleft()
            return Haiku(line1=line1, line2=line2, line3=line3)
        return None
