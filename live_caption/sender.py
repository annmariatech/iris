class CaptionSender:
    """
    Sends captions to the frontend and backend.

    For now this is a mock implementation.
    Later it can be replaced with WebSockets or FastAPI.
    """

    def send_to_frontend(self, caption):
        print(f"📺 Frontend received: {caption}")

    def send_to_backend(self, caption):
        print(f"💾 Backend received: {caption}")

    def send(self, caption):
        self.send_to_frontend(caption)
        self.send_to_backend(caption)