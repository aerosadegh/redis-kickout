import time
from typing import Optional

import redis

from logger import logger
from common import execute_after_inactivity


def connect_to_redis(host: str, port: int, db: int) -> Optional[redis.Redis]:
    """Establish a connection to Redis, retrying until successful."""
    repeated = False
    while True:
        try:
            if not repeated:
                logger.info(f"Connecting to Redis with {host}:{port}")
            client = redis.Redis(host=host, port=port, db=db)
            client.ping()
            logger.info("Connected to Redis")
            return client
        except Exception as e:
            if not repeated:
                logger.error(f"Failed to connect to Redis: {e}")
                repeated = True
            time.sleep(1)  # Wait before retrying


def listen_for_messages(
    redis_client: redis.Redis,
    channel_pattern: str,
    inactivity_timeout: int,
    cmd: str,
) -> None:
    """Listen for messages on Redis channels and execute a command after inactivity."""
    while True:
        try:
            pubsub = redis_client.pubsub()
            pubsub.psubscribe(*channel_pattern.split())
            logger.info(f"Subscribed to channels with pattern: '{channel_pattern}'")

            last_message_time = None
            current_channel = None
            repeated = False

            while True:
                message = pubsub.get_message()
                current_time = time.time()

                if message and message["type"] == "pmessage":
                    data = message["data"]
                    channel = message["channel"]
                    # Decode bytes to strings
                    if isinstance(channel, bytes):
                        channel = channel.decode("utf-8")
                    if isinstance(data, bytes):
                        data = data.decode("utf-8")
                    if not repeated:
                        logger.info(f"Received message on channel pattern")
                        repeated = True
                    last_message_time = current_time
                    current_channel = channel
                elif (
                    last_message_time
                    and (current_time - last_message_time) >= inactivity_timeout
                ):
                    execute_after_inactivity(current_channel, cmd, inactivity_timeout)
                    # Reset to prevent repeated execution
                    last_message_time = None
                    current_channel = None

                time.sleep(0.001)  # Sleep briefly to reduce CPU usage
        except redis.exceptions.ConnectionError as e:
            logger.error(f"Redis connection error: {e}")
            logger.info("Attempting to reconnect to Redis")
            redis_client = connect_to_redis(
                redis_client.connection_pool.connection_kwargs["host"],
                redis_client.connection_pool.connection_kwargs["port"],
                redis_client.connection_pool.connection_kwargs["db"],
            )
        except Exception as e:
            logger.error(f"An error occurred while listening for messages: {e}")
            time.sleep(1)  # Wait before retrying
