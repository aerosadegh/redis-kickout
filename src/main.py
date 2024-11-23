import argparse

from settings import read_envs
from logger import logger
from common import load_environment
from redis_client import connect_to_redis, listen_for_messages


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Redis Listener Script")
    parser.add_argument(
        "-e",
        "--env-file",
        type=str,
        default=".env",
        help="Path to the .env file (default: .env)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    load_environment(args.env_file)
    config = read_envs()
    redis_client = connect_to_redis(
        config.redis_host, config.redis_port, config.redis_db
    )
    if not redis_client:
        logger.error("Could not establish Redis connection. Exiting.")
        return

    try:
        listen_for_messages(
            redis_client,
            config.redis_channel_pattern,
            config.redis_inactivity_timeout,
            config.cmd,
        )
    except KeyboardInterrupt:
        logger.info("Program interrupted by user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        logger.info("Program is exiting.")


if __name__ == "__main__":
    main()
