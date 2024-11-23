import os
from typing import Optional
import subprocess
import shlex
from dataclasses import dataclass

from dotenv import load_dotenv

from logger import logger


@dataclass
class Config:
    """Configuration for the Redis listener."""

    redis_host: str
    redis_port: int
    redis_db: int
    redis_channel_pattern: str
    redis_inactivity_timeout: int
    cmd: str


def load_environment(env_file: str) -> None:
    """Load environment variables from a .env file."""
    if os.path.exists(env_file):
        load_dotenv(dotenv_path=env_file)
        logger.info(f"Loaded environment variables from '{env_file}'")
    else:
        logger.warning(
            f"Environment file '{env_file}' not found. Using defaults or system environment variables."
        )


def execute_after_inactivity(
    channel: Optional[str], cmd: str, inactivity_timeout: int
) -> None:
    """Execute a command after inactivity period."""
    logger.info(
        f"No messages received on {channel} for {inactivity_timeout} seconds. Executing command: '{cmd}'"
    )
    try:
        subprocess.Popen(shlex.split(cmd))
    except Exception as e:
        logger.error(f"Failed to execute command '{cmd}': {e}")
