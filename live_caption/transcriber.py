import whisper

print("🔄 Loading Whisper model...")

model = whisper.load_model("base")

print("✅ Model loaded!")

print("\n🎧 Transcribing audio...\n")

result = model.transcribe("test_recording.wav")

print("📝 Caption:\n")

print(result["text"])