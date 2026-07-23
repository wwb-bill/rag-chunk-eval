from dataclasses import dataclass

@dataclass
class Chunk:
    text: str
    start_char: int
    end_char: int

def fixed_size(text: str, size: int = 500) -> list:
    return [Chunk(text=text[i:i+size], start_char=i, end_char=min(i+size, len(text))) for i in range(0, len(text), size)]

def sentence(text: str) -> list:
    import re
    sents = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    pos = 0
    for s in sents:
        end = pos + len(s)
        chunks.append(Chunk(text=s, start_char=pos, end_char=end))
        pos = end + 1
    return chunks

def paragraph(text: str) -> list:
    paras = text.split('\n\n')
    chunks = []
    pos = 0
    for p in paras:
        end = pos + len(p)
        chunks.append(Chunk(text=p, start_char=pos, end_char=end))
        pos = end + 2
    return chunks

def recursive(text: str, size: int = 500) -> list:
    if len(text) <= size:
        return [Chunk(text=text, start_char=0, end_char=len(text))]
    mid = len(text) // 2
    return recursive(text[:mid], size) + recursive(text[mid:], size)