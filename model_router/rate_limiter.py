"""Rate limiter for Ollama cloud requests."""

import time
from collections import defaultdict


class RateLimiter:
    def __init__(self, max_per_minute=15, retry_after=30, max_retries=3):
        self.max_per_minute = max_per_minute
        self.retry_after = retry_after
        self.max_retries = max_retries
        self._timestamps = defaultdict(list)

    def wait_if_needed(self, model: str):
        """Block until we're under the rate limit for this model."""
        now = time.time()
        cutoff = now - 60

        # clean old timestamps
        self._timestamps[model] = [
            t for t in self._timestamps[model] if t > cutoff
        ]

        if len(self._timestamps[model]) >= self.max_per_minute:
            oldest = self._timestamps[model][0]
            wait_time = 60 - (now - oldest) + 0.1
            if wait_time > 0:
                time.sleep(wait_time)

        self._timestamps[model].append(time.time())

    def handle_429(self, model: str, attempt: int) -> bool:
        """Handle a 429 rate limit response. Returns True if should retry."""
        if attempt >= self.max_retries:
            return False
        wait = self.retry_after * (attempt + 1)
        time.sleep(wait)
        return True
