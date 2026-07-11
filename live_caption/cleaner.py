class CaptionCleaner:
    """
    Removes duplicate and empty captions.
    """

    def __init__(self):
        self.last_caption = ""

    def clean(self, text):
        """
        Returns a cleaned caption.
        Returns None if it should be ignored.
        """

        text = text.strip()

        # Ignore empty captions
        if text == "":
            return None

        # Ignore repeated captions
        if text == self.last_caption:
            return None

        self.last_caption = text

        return text

    def reset(self):
        """Reset when a new lecture starts."""
        self.last_caption = ""

