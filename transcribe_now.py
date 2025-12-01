import subprocess
import speech_recognition as sr
import os

audio_file = "WhatsApp Ptt 2025-12-01 at 12.02.34 PM.ogg"
wav_file = "temp_audio.wav"

print("=" * 70)
print("TRANSCRIBING TUTOR FEEDBACK")
print("=" * 70)

# Step 1: Convert
print(f"\nConverting {audio_file} to WAV...")
subprocess.run([
    "ffmpeg", "-i", audio_file,
    "-acodec", "pcm_s16le",
    "-ac", "1",  
    "-ar", "16000",
    "-y",
    wav_file
], check=True, capture_output=True)

print("Conversion complete!")

# Step 2: Transcribe
print("\nTranscribing audio...")
recognizer = sr.Recognizer()

with sr.AudioFile(wav_file) as source:
    recognizer.adjust_for_ambient_noise(source, 0.5)
    audio_data = recognizer.record(source)
    
    print("Sending to Google Speech Recognition API...")
    text = recognizer.recognize_google(audio_data, language="en-GB")
    
    print("\n" + "=" * 70)
    print("TRANSCRIPTION:")
    print("=" * 70)
    print()
    print(text)
    print()
    print("=" * 70)
    
    # Save
    with open("tutor_feedback_transcription.txt", "w", encoding="utf-8") as f:
        f.write("TUTOR FEEDBACK TRANSCRIPTION\n")
        f.write("=" * 70 + "\n\n")
        f.write(text)
        f.write("\n\n" + "=" * 70)
    
    print("\nSaved to: tutor_feedback_transcription.txt")

# Cleanup
os.remove(wav_file)
print("Done!")
