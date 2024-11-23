import os

from common import Config


def read_envs() -> Config:
    """Read environment variables and set default values."""
    return Config(
        redis_host=os.getenv("REDIS_HOST", "localhost"),
        redis_port=int(os.getenv("REDIS_PORT", 6379)),
        redis_db=int(os.getenv("REDIS_DB", 0)),
        redis_channel_pattern=os.getenv("REDIS_CHANNEL_PATTERN", "AST*"),
        redis_inactivity_timeout=int(os.getenv("REDIS_INACTIVITY_TIMEOUT", 60)),
        cmd=os.getenv("CMD", "shutdown -r -t 0"),
    )
