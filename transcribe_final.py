"""
Final transcription attempt using ffmpeg-python to convert OGG to WAV
"""
import ffmpeg
import speech_recognition as sr
import os
import sys

audio_file = "WhatsApp Ptt 2025-12-01 at 12.02.34 PM.ogg"
wav_file = "temp_converted.wav"

print("=" * 70)
print(f"🎤 TRANSCRIBING TUTOR FEEDBACK")
print("=" * 70)
print(f"Input file: {audio_file}")
print()

try:
    # Convert OGG to WAV using ffmpeg
    print("📝 Step 1: Converting OGG to WAV format...")
    (
        ffmpeg
        .input(audio_file)
        .output(wav_file, acodec='pcm_s16le', ac=1, ar='16000')
        .overwrite_output()
        .run(quiet=True)
    )
    print("✅ Conversion complete!")
    
    # Now transcribe the WAV file
    print("\n🔍 Step 2: Transcribing audio with Google Speech Recognition...")
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(wav_file) as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        # Record the audio
        audio_data = recognizer.record(source)
        
        print("⏳ Processing (this may take 10-30 seconds)...")
        
        # Transcribe
        text = recognizer.recognize_google(audio_data, language='en-GB', show_all=False)
        
        print("\n" + "=" * 70)
        print("📄 TRANSCRIPTION COMPLETE!")
        print("=" * 70)
        print()
        print(text)
        print()
        print("=" * 70)
        
        # Save to file
        output_file = "tutor_feedback_transcription.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("TUTOR FEEDBACK TRANSCRIPTION\n")
            f.write("WhatsApp Voice Note: 2025-12-01 at 12.02.34 PM\n")
            f.write("=" * 70 + "\n\n")
            f.write(text)
            f.write("\n\n" + "=" * 70 + "\n")
            f.write("Note: Automated transcription may not capture everything perfectly.\n")
            f.write("Multiple speakers may be present in the recording.\n")
        
        print(f"✅ Transcription saved to: {output_file}\n")
        
except ffmpeg.Error as e:
    print(f"❌ FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}")
    print("\nℹ️  FFmpeg is not installed or not in PATH")
    print("   Please install FFmpeg from: https://ffmpeg.org/download.html")
    sys.exit(1)
    
except sr.UnknownValueError:
    print("❌ Google Speech Recognition could not understand the audio")
    print("   The audio may be unclear or have background noise")
    sys.exit(1)
    
except sr.RequestError as e:
    print(f"❌ Could not request results from Google Speech Recognition; {e}")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
    
finally:
    # Clean up temporary file
    if os.path.exists(wav_file):
        os.remove(wav_file)
        print("🧹 Cleaned up temporary files")
