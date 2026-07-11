import sounddevice as sd
from scipy.io.wavfile import write

# Recording settings
sample_rate = 16000
duration = 5  # seconds

print("🎤 Recording... Speak now!")

audio = sd.rec(
    int(duration * sample_rate),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

sd.wait()

write("test_recording.wav", sample_rate, audio)

print("✅ Recording saved as test_recording.wav")