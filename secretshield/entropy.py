import math
import re
from collections import Counter

# Tokens shorter than this are too short to judge entropy meaningfully
MIN_TOKEN_LENGTH = 20

# Entropy threshold above which a string looks "random" rather than natural language
ENTROPY_THRESHOLD = 4.3

# Splits a line into candidate tokens: quoted strings, or chunks after =, :, etc.
TOKEN_SPLIT_PATTERN = re.compile(r"""['"]([^'"]{8,})['"]|[=:]\s*([A-Za-z0-9+/_\-\.]{8,})""")


def shannon_entropy(s: str) -> float:
    """Calculate the Shannon entropy of a string, in bits per character."""
    if not s:
        return 0.0
    counts = Counter(s)
    length = len(s)
    return -sum((c / length) * math.log2(c / length) for c in counts.values())


def extract_candidate_tokens(line: str) -> list[str]:
    """Pull out quoted strings and assignment values that might be secrets."""
    tokens = []
    for match in TOKEN_SPLIT_PATTERN.finditer(line):
        token = match.group(1) or match.group(2)
        if token and len(token) >= MIN_TOKEN_LENGTH:
            tokens.append(token)
    return tokens


def find_high_entropy_strings(line: str) -> list[tuple[str, float]]:
    """Return (token, entropy) pairs for tokens that look random enough to be secrets."""
    results = []
    for token in extract_candidate_tokens(line):
        score = shannon_entropy(token)
        if score >= ENTROPY_THRESHOLD:
            results.append((token, score))
    return results