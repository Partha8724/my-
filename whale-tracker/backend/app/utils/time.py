from datetime import UTC, datetime


def utc_now() -> datetime:
    # Keep stored timestamps naive-in-UTC for compatibility with the existing SQLite schema.
    return datetime.now(UTC).replace(tzinfo=None)
