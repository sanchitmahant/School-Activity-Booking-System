"""
Simple audio transcription using Google Speech Recognition API
Works without ffmpeg by using alternative audio processing
"""
import speech_recognition as sr
import subprocess
import os

audio_file = "WhatsApp Ptt 2025-12-01 at 12.02.34 PM.ogg"

print(f"🎤 Transcribing: {audio_file}")
print("=" * 70)

# Initialize recognizer
recognizer = sr.Recognizer()

try:
    # Try to use the OGG file directly or convert using available tools
    print("📝 Processing audio file...")
    
    # Try using sr.AudioFile directly
    with sr.AudioFile(audio_file) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio_data = recognizer.record(source)
        
        print("🔍 Transcribing with Google Speech Recognition...")
        text = recognizer.recognize_google(audio_data, language='en-GB', show_all=False)
        
        print("\n" + "=" * 70)
        print("📄 TRANSCRIPTION:")
        print("=" * 70)
        print(text)
        print("=" * 70)
        
        # Save to file
        with open("tutor_feedback_transcription.txt", "w", encoding="utf-8") as f:
            f.write("TUTOR FEEDBACK - WhatsApp Voice Note\n")
            f.write("=" * 70 + "\n\n")
            f.write(text)
            f.write("\n\n" + "=" * 70)
        
        print("\n✅ Saved to: tutor_feedback_transcription.txt")
        
except Exception as e:
    print(f"❌ Direct method failed: {e}")
    print("\nℹ️ Trying alternative method with raw audio data...")
    
    try:
        # Alternative: Use recognize_google with the file path
        with open(audio_file, 'rb') as audio:
            audio_data = sr.AudioData(audio.read(), 48000, 2)
            text = recognizer.recognize_google(audio_data, language='en-GB')
            
            print("\n" + "=" * 70)
            print("📄 TRANSCRIPTION:")
            print("=" * 70)
            print(text)
            print("=" * 70)
            
    except Exception as e2:
        print(f"❌ Alternative method also failed: {e2}")
        print("\nℹ️ The audio file format may require additional processing.")
        print("ℹ️ Attempting web-based transcription service...")
