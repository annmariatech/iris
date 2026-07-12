from datetime import datetime


class TimestampManager:
    """
    Generates timestamps for captions.
    """

    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%H:%M:%S")