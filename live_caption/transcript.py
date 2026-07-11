from datetime import datetime


class TranscriptManager:
    """
    Stores all captions generated during a lecture session.
    """

    def __init__(self):
        self.captions = []

    def add_caption(self, text):
        """Add a caption with the current timestamp."""

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.captions.append({
            "timestamp": timestamp,
            "text": text
        })

    def get_transcript(self):
        """Return the complete transcript."""

        return self.captions

    def clear(self):
        """Clear transcript when a new lecture starts."""

        self.captions.clear()

