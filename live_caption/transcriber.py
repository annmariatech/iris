import whisper


class WhisperTranscriber:
    """
    Converts audio files into text using OpenAI Whisper.
    """

    def __init__(self, model_name="base"):
        print("Loading Whisper model...")
        self.model = whisper.load_model(model_name)
        print("Whisper model loaded successfully.")

    def transcribe(self, audio_file):
        """
        Transcribe an audio file and return the text.
        """

        result = self.model.transcribe(
    audio_file,
    language="en",
    fp16=False
)

        return result["text"].strip()
    
