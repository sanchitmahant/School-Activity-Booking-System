"""
Use AssemblyAI API to transcribe OGG file directly
AssemblyAI supports OGG format without needing local conversion
"""
import assemblyai as aai
import os

audio_file = "WhatsApp Ptt 2025-12-01 at 12.02.34 PM.ogg"

print("=" * 70)
print("🎤 TRANSCRIBING TUTOR FEEDBACK WITH ASSEMBLYAI")
print("=" * 70)

# Use a free tier API key (you can get one free at assemblyai.com)
# For now, let's use the trial/free tier
aai.settings.api_key = "YOUR_API_KEY"  # This would normally require a key

try:
    print(f"📤 Uploading {audio_file} to AssemblyAI...")
    
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)
    
    if transcript.status == aai.TranscriptStatus.error:
        print(f"❌ Transcription failed: {transcript.error}")
    else:
        print("\n" + "=" * 70)
        print("📄 TRANSCRIPTION:")
        print("=" * 70)
        print()
        print(transcript.text)
        print()
        print("=" * 70)
        
        # Save to file
        with open("tutor_feedback_transcription.txt", "w", encoding="utf-8") as f:
            f.write("TUTOR FEEDBACK TRANSCRIPTION\n")
            f.write("=" * 70 + "\n\n")
            f.write(transcript.text)
            f.write("\n\n" + "=" * 70)
        
        print("\n✅ Saved to: tutor_feedback_transcription.txt")
        
except Exception as e:
    print(f"\n❌ AssemblyAI error: {e}")
    print("\nAssemblyAI requires an API key. Trying alternative...")
    
    # Fall back to using wit.ai which is free
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    
    try:
        with open(audio_file, 'rb') as f:
            audio_content = f.read()
        
        # Try with Wit.ai (free, no API key needed for basic use)
        text = recognizer.recognize_wit(audio_content)
        print(f"\n✅ Transcription: {text}")
        
    except:
        print("All methods exhausted. FFmpeg is required for OGG conversion.")
        print("Please install FFmpeg: winget install ffmpeg")
