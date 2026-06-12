from slowapi import Limiter
from slowapi.util import get_remote_address
from app.config import settings

# Default limits set from settings.RATE_LIMIT_PER_MINUTE
default_limit = f"{settings.RATE_LIMIT_PER_MINUTE}/minute"
limiter = Limiter(key_func=get_remote_address, default_limits=[default_limit])
