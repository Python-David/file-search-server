import time
from collections import deque
from typing import Deque, Dict

from .logger import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """
    Implements rate limiting with exponential backoff.

    :param max_requests: Maximum number of requests allowed within the time window.
    :param window_size: Size of the time window in seconds.
    :param base_backoff: Base backoff time for exponential backoff in seconds.
    """

    def __init__(self, max_requests: int, window_size: int, base_backoff: int):
        self.max_requests = max_requests
        self.window_size = window_size
        self.base_backoff = base_backoff
        self.requests: Dict[str, Deque[float]] = {}
        self.attempts: Dict[str, int] = {}

    def is_allowed(self, client_address: str) -> bool:
        """
        Checks if a request from the given client is allowed.

        :param client_address: The address of the client.

        :return: True if the request is allowed, False otherwise.
        """
        current_time = time.time()
        if client_address not in self.requests:
            self.requests[client_address] = deque()
            self.attempts[client_address] = 0

        request_times = self.requests[client_address]

        # Remove old requests outside the window
        while request_times and request_times[0] < current_time - self.window_size:
            request_times.popleft()

        logger.debug(
            f"Client {client_address} has {len(request_times)} requests in the last {self.window_size} seconds"
        )

        if len(request_times) < self.max_requests:
            request_times.append(current_time)
            self.attempts[client_address] = 0  # Reset attempts on successful request
            logger.debug(f"Request allowed for {client_address}")
            return True
        else:
            self.attempts[client_address] += 1
            backoff_time = self.base_backoff * (2 ** self.attempts[client_address])
            logger.debug(
                f"Request denied for {client_address} - rate limit exceeded, backoff time: {backoff_time}s"
            )
            time.sleep(backoff_time)
            return False
