"""Categorize prompts by task type."""

import re

CODE_PATTERNS = [
    r"write.*code", r"function", r"script", r"debug", r"fix.*bug",
    r"implement", r"refactor", r"class\b", r"import\b", r"def\b",
    r"syntax", r"compile", r"runtime.*error", r"stack\s*trace",
    r"pull\s*request", r"git\b", r"docker", r"deploy",
    r"api\b", r"endpoint", r"database", r"query", r"sql",
]

REASONING_PATTERNS = [
    r"explain", r"why\b", r"analyze", r"compare", r"think.*through",
    r"step\s*by\s*step", r"prove", r"derive", r"calculate",
    r"what\s*if", r"trade.?off", r"pros?\s*and\s*cons?",
]

VISION_PATTERNS = [
    r"image", r"screenshot", r"photo", r"picture", r"look\s*at",
    r"describe.*this", r"what.*see", r"diagram",
]

SEARCH_PATTERNS = [
    r"latest", r"news\b", r"current", r"weather", r"search\b",
    r"today", r"recent", r"update.*on",
]

CATEGORIES = {
    "code": CODE_PATTERNS,
    "reasoning": REASONING_PATTERNS,
    "vision": VISION_PATTERNS,
    "search": SEARCH_PATTERNS,
}


def categorize(prompt: str) -> str:
    """Return the best category for a prompt. Defaults to 'chat'."""
    prompt_lower = prompt.lower()
    scores = {}

    for category, patterns in CATEGORIES.items():
        score = sum(1 for p in patterns if re.search(p, prompt_lower))
        if score > 0:
            scores[category] = score

    if not scores:
        return "chat"

    return max(scores, key=scores.get)
