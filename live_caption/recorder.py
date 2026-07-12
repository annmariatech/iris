import sounddevice as sd
from scipy.io.wavfile import write


class AudioRecorder:
    """
    Records audio from the microphone.
    """

    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def record(self, duration=5, filename="temp.wav"):
        """
        Record audio for a given duration.
        """

        print(f"🎤 Recording for {duration} seconds...")

        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=self.sample_rate,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        write(filename, self.sample_rate, audio)

        print(f"✅ Audio saved as {filename}")

        return filename
    
