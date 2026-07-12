from datetime import datetime, timezone


class TimestampManager:
    """
    Generates ISO 8601 timestamps for captions.
    """

    @staticmethod
    def get_timestamp():
        return datetime.now(timezone.utc).isoformat()