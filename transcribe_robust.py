"""
Direct OGG to WAV conversion using system ffmpeg and then transcribe
"""
import subprocess
import speech_recognition as sr
import os
import shutil

audio_file = "WhatsApp Ptt 2025-12-01 at 12.02.34 PM.ogg"
wav_file = "temp_converted.wav"

print("=" * 70)
print("🎤 TRANSCRIBING TUTOR FEEDBACK")
print("=" * 70)

# Find ffmpeg
ffmpeg_path = shutil.which("ffmpeg")
if not ffmpeg_path:
    # Try common installation paths
    possible_paths = [
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        r"C:\Program Files (x86)\ffmpeg\bin\ffmpeg.exe",
        r"C:\ffmpeg\bin\ffmpeg.exe",
        r"C:\Users\Sanchit Kaushal\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg.exe",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            ffmpeg_path = path
            break

if not ffmpeg_path:
    print("❌ FFmpeg not found in PATH. Searching...")
    result = subprocess.run(["where", "ffmpeg"], capture_output=True, text=True)
    if result.returncode == 0:
        ffmpeg_path = result.stdout.strip().split('\n')[0]
        print(f"✅ Found ffmpeg at: {ffmpeg_path}")
    else:
        print("❌ FFmpeg not found. Using default 'ffmpeg' command...")
        ffmpeg_path = "ffmpeg"

print(f"\n📝 Converting OGG to WAV using: {ffmpeg_path}")

try:
    # Convert OGG to WAV
    subprocess.run([
        ffmpeg_path, "-i", audio_file,
        "-acodec", "pcm_s16le",
        "-ac", "1",
        "-ar", "16000",
        "-y",
        wav_file
    ], check=True, capture_output=True)
    
    print("✅ Conversion complete!")
    
    # Transcribe
    print(f"\n🔍 Transcribing {wav_file}...")
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(wav_file) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio_data = recognizer.record(source)
        
        print("⏳ Sending to Google Speech Recognition API...")
        
        text = recognizer.recognize_google(audio_data, language='en-GB', show_all=False)
        
        print("\n" + "=" * 70)
        print("📄 TUTOR FEEDBACK TRANSCRIPTION:")
        print("=" * 70)
        print()
        print(text)
        print()
        print("=" * 70)
        
        # Save
        output_file = "tutor_feedback_transcription.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("TUTOR FEEDBACK TRANSCRIPTION\n")
            f.write("WhatsApp Ptt 2025-12-01 at 12.02.34 PM\n")
            f.write("=" * 70 + "\n\n")
            f.write(text)
            f.write("\n\n" + "=" * 70 + "\n")
            f.write("\nNote: This is an automated transcription.\n")
            f.write("Multiple speakers may be present.\n")
        
        print(f"\n✅ Transcription saved to: {output_file}\n")
        
except subprocess.CalledProcessError as e:
    print(f"❌ FFmpeg conversion failed: {e.stderr.decode() if e.stderr else str(e)}")
    
except sr.UnknownValueError:
    print("❌ Could not understand audio")
    
except sr.RequestError as e:
    print(f"❌ Google Speech Recognition error: {e}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    if os.path.exists(wav_file):
        os.remove(wav_file)
        print("🧹 Cleaned up temporary files")
