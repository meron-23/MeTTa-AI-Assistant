from __future__ import annotations

import asyncio
import random
import time
from typing import Awaitable, Callable, Iterable, Optional, Type, Union


class RetryConfig:
    def __init__(
        self,
        max_retries: int = 5,
        base_delay: float = 0.5,
        factor: float = 2.0,
        max_delay: float = 8.0,
        jitter: float = 0.25,
    ) -> None:
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.factor = factor
        self.max_delay = max_delay
        self.jitter = jitter

    def compute_sleep(self, attempt: int) -> float:
        delay = min(self.base_delay * (self.factor ** attempt), self.max_delay)
        return delay + random.uniform(0, self.jitter)


def _retry_after_from_error(err: Exception) -> Optional[float]:
    """Best-effort extraction of Retry-After seconds from known error shapes."""
    msg = str(err).lower()
    tokens = msg.replace("\n", " ").split()
    for i, tok in enumerate(tokens):
        if tok in {"retry-after", "retry", "after"}:
            for j in range(i + 1, min(i + 4, len(tokens))):
                try:
                    val = float(tokens[j].strip(";:,s"))
                    if val >= 0:
                        return val
                except Exception:
                    continue
    return None


def async_retry(
    *,
    retry_on: Union[Iterable[Type[BaseException]], Callable[[Exception], bool]],
    cfg: RetryConfig | None = None,
):
    """Retry decorator with exponential backoff + jitter for async callables.

    retry_on: iterable of Exception types or a predicate(Exception) -> bool
    cfg: RetryConfig with backoff parameters
    """
    cfg = cfg or RetryConfig()

    def _is_retryable(err: Exception) -> bool:
        if callable(retry_on):
            return bool(retry_on(err))
        try:
            return any(isinstance(err, t) for t in retry_on)
        except TypeError:
            return False

    def wrapper(fn: Callable[..., Awaitable]):
        async def inner(*args, **kwargs):
            last_err: Optional[Exception] = None
            for attempt in range(cfg.max_retries):
                try:
                    return await fn(*args, **kwargs)
                except Exception as e:  
                    if not _is_retryable(e):
                        raise
                    last_err = e
                    retry_after = _retry_after_from_error(e)
                    sleep = retry_after if retry_after is not None else cfg.compute_sleep(attempt)
                    await asyncio.sleep(sleep)
            assert last_err is not None
            raise last_err

        return inner

    return wrapper
