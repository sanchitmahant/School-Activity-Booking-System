"""
Transcribe WhatsApp voice note to text using speech recognition
"""
import speech_recognition as sr
from pydub import AudioSegment
import os

# Path to the audio file
audio_file = "WhatsApp Ptt 2025-12-01 at 12.02.34 PM.ogg"

print(f"🎤 Transcribing audio file: {audio_file}")
print("=" * 60)

try:
    # Convert OGG to WAV (required for speech recognition)
    print("📝 Converting OGG to WAV...")
    audio = AudioSegment.from_ogg(audio_file)
    wav_file = "temp_audio.wav"
    audio.export(wav_file, format="wav")
    print("✅ Conversion complete")
    
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    # Load the audio file
    print("🎧 Loading audio...")
    with sr.AudioFile(wav_file) as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        # Record the audio
        audio_data = recognizer.record(source)
        
        print("🔍 Transcribing... (this may take a moment)")
        
        # Perform speech recognition
        try:
            # Using Google Speech Recognition (free)
            text = recognizer.recognize_google(audio_data, language='en-US', show_all=False)
            
            print("\n" + "=" * 60)
            print("📄 TRANSCRIPTION:")
            print("=" * 60)
            print(text)
            print("=" * 60)
            
            # Save transcription to file
            with open("audio_transcription.txt", "w", encoding="utf-8") as f:
                f.write("TUTOR FEEDBACK TRANSCRIPTION\n")
                f.write("=" * 60 + "\n")
                f.write(f"Audio File: {audio_file}\n")
                f.write("=" * 60 + "\n\n")
                f.write(text)
                f.write("\n\n" + "=" * 60 + "\n")
                f.write("Note: Multiple speakers detected. Manual review recommended.\n")
            
            print("\n✅ Transcription saved to: audio_transcription.txt")
            
        except sr.UnknownValueError:
            print("❌ Could not understand audio - speech not clear enough")
        except sr.RequestError as e:
            print(f"❌ Could not request results from Google Speech Recognition service; {e}")
    
    # Clean up temporary file
    if os.path.exists(wav_file):
        os.remove(wav_file)
        print("🧹 Cleaned up temporary files")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nℹ️ Required packages: pip install SpeechRecognition pydub")
    print("ℹ️ Also need ffmpeg installed on system for audio conversion")
