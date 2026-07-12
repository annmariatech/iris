from sender import CaptionSender
from recorder import AudioRecorder
from transcriber import WhisperTranscriber
from cleaner import CaptionCleaner
from transcript import TranscriptManager


class LiveCaptionSystem:
    """
    Controls the complete live caption pipeline.
    """

    def __init__(self):
        self.sender = CaptionSender()
        self.recorder = AudioRecorder()
        self.transcriber = WhisperTranscriber()
        self.cleaner = CaptionCleaner()
        self.transcript = TranscriptManager()

        self.running = False

    def start(self):
        """Starts the lecture session."""
        print("Lecture started.")
        self.running = True

    def run(self):
        """Continuously process audio until stopped."""
        while self.running:
            self.process_once()

    def stop(self):
        """Stops the lecture session."""
        print("Lecture stopped.")
        self.running = False

    def process_once(self):
        """Process one chunk of audio."""

        audio_file = self.recorder.record()

        text = self.transcriber.transcribe(audio_file)

        print(f"\n🎙 Raw Whisper Output: '{text}'")

        cleaned = self.cleaner.clean(text)

        print(f"🧹 Cleaned Output: {cleaned}")

        if cleaned:
            self.transcript.add_caption(cleaned)

            print(f"📝 Final Caption: {cleaned}")

            self.sender.send(cleaned)


if __name__ == "__main__":

    system = LiveCaptionSystem()

    try:
        system.start()
        system.run()

    except KeyboardInterrupt:
        system.stop()