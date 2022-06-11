from typing import Optional


class Stream:
    def __init__(self, source: str):
        self.src = source
        self.idx = 0

    @property
    def next(self) -> Optional[str]:
        next_idx = self.idx + 1
        if next_idx == len(self.src):
            return None
        return self.src[next_idx]

    @property
    def current(self) -> Optional[str]:
        if self.idx == len(self.src):
            return None
        return self.src[self.idx]

    def advance(self) -> None:
        self.idx += 1
