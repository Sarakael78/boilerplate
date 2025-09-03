import time
from typing import Dict, Tuple

import redis.asyncio as redis
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from ..core.config import settings


class RateLimiter:
    def __init__(self):
        self.redis_client = None
        self.rate_limits = {
            "default": {"requests": 60, "window": 60},  # 60 requests per minute
            "auth": {"requests": 5, "window": 60},  # 5 auth attempts per minute
            "api": {"requests": 100, "window": 60},  # 100 API calls per minute
        }

    async def get_redis_client(self):
        if self.redis_client is None:
            self.redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
            )
        return self.redis_client

    async def is_rate_limited(
        self, key: str, limit_type: str = "default"
    ) -> Tuple[bool, Dict]:
        """
        Check if request is rate limited.
        Returns (is_limited, rate_info)
        """
        redis_client = await self.get_redis_client()
        limit_config = self.rate_limits[limit_type]

        # Create rate limit key
        window_key = f"rate_limit:{key}:{limit_type}:{int(time.time() // limit_config['window'])}"

        try:
            # Get current count
            current_count = await redis_client.get(window_key)
            current_count = int(current_count) if current_count else 0

            # Check if limit exceeded
            if current_count >= limit_config["requests"]:
                return True, {
                    "limit": limit_config["requests"],
                    "remaining": 0,
                    "reset": int(time.time() // limit_config["window"] + 1)
                    * limit_config["window"],
                }

            # Increment counter
            await redis_client.incr(window_key)
            await redis_client.expire(window_key, limit_config["window"])

            return False, {
                "limit": limit_config["requests"],
                "remaining": limit_config["requests"] - current_count - 1,
                "reset": int(time.time() // limit_config["window"] + 1)
                * limit_config["window"],
            }

        except Exception as e:
            # If Redis is unavailable, allow request but log error
            print(f"Rate limiting error: {e}")
            return False, {"limit": 0, "remaining": 0, "reset": 0}

    def get_client_ip(self, request: Request) -> str:
        """Extract client IP from request."""
        # Check for forwarded headers
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        return request.client.host if request.client else "unknown"


async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware."""
    rate_limiter = RateLimiter()

    # Determine rate limit type based on path
    path = request.url.path
    if path.startswith("/auth"):
        limit_type = "auth"
    elif path.startswith("/api"):
        limit_type = "api"
    else:
        limit_type = "default"

    # Get client identifier
    client_ip = rate_limiter.get_client_ip(request)
    user_id = request.headers.get("X-User-ID", "anonymous")
    client_key = f"{client_ip}:{user_id}"

    # Check rate limit
    is_limited, rate_info = await rate_limiter.is_rate_limited(client_key, limit_type)

    if is_limited:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "detail": "Rate limit exceeded",
                "retry_after": rate_info["reset"] - int(time.time()),
            },
            headers={
                "X-RateLimit-Limit": str(rate_info["limit"]),
                "X-RateLimit-Remaining": str(rate_info["remaining"]),
                "X-RateLimit-Reset": str(rate_info["reset"]),
                "Retry-After": str(rate_info["reset"] - int(time.time())),
            },
        )

    # Add rate limit headers to response
    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(rate_info["limit"])
    response.headers["X-RateLimit-Remaining"] = str(rate_info["remaining"])
    response.headers["X-RateLimit-Reset"] = str(rate_info["reset"])

    return response


# Decorator for specific endpoints
def rate_limit(limit_type: str = "default"):
    """Decorator to apply rate limiting to specific endpoints."""

    async def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract request from args or kwargs
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

            if not request:
                for value in kwargs.values():
                    if isinstance(value, Request):
                        request = value
                        break

            if request:
                rate_limiter = RateLimiter()
                client_ip = rate_limiter.get_client_ip(request)
                user_id = request.headers.get("X-User-ID", "anonymous")
                client_key = f"{client_ip}:{user_id}"

                is_limited, rate_info = await rate_limiter.is_rate_limited(
                    client_key, limit_type
                )

                if is_limited:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Rate limit exceeded",
                    )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
