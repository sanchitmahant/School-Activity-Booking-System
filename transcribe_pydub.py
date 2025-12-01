"""
Transcribe using pydub with simpleaudio backend
"""
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import os
import io

audio_file = "WhatsApp Ptt 2025-12-01 at 12.02.34 PM.ogg"

print("=" * 70)
print("🎤 TRANSCRIBING TUTOR FEEDBACK")
print("=" * 70)

try:
    print(f"📂 Loading {audio_file}...")
    
    # Load OGG file directly with pydub (it can handle OGG without ffmpeg in some cases)
    # Try loading with different methods
    try:
        audio = AudioSegment.from_file(audio_file, format="ogg", codec="libopus")
    except:
        try:
            audio = AudioSegment.from_file(audio_file, format="ogg")
        except:
            audio = AudioSegment.from_file(audio_file)
    
    print(f"✅ Audio loaded: {len(audio)/1000:.1f} seconds, {audio.frame_rate} Hz")
    
    # Convert to WAV in memory
    print("📝 Converting to WAV format in memory...")
    wav_io = io.BytesIO()
    audio.export(wav_io, format='wav')
    wav_io.seek(0)
    
    print("✅ Conversion complete!")
    
    # Save temporary WAV file
    temp_wav = "temp_audio.wav"
    with open(temp_wav, 'wb') as f:
        f.write(wav_io.read())
    
    # Transcribe
    print("\n🔍 Transcribing with Google Speech Recognition...")
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(temp_wav) as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio_data = recognizer.record(source)
        
        print("⏳ Processing...")
        
        text = recognizer.recognize_google(audio_data, language='en-GB', show_all=False)
        
        print("\n" + "=" * 70)
        print("📄 TRANSCRIPTION:")
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
            
        print("\n✅ Saved to: tutor_feedback_transcription.txt")
        
    # Cleanup
    if os.path.exists(temp_wav):
        os.remove(temp_wav)
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTrying Windows-specific method...")
    
    import subprocess
    result = subprocess.run(
        ['.venv\\Scripts\\python.exe', '-c', 
         f'from pydub import AudioSegment; AudioSegment.converter = "C:\\\\Windows\\\\System32\\\\ffmpeg.exe"; audio = AudioSegment.from_file("{audio_file}"); audio.export("temp_audio.wav", format="wav")'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ Conversion successful!")
        # Now transcribe
        recognizer = sr.Recognizer()
        with sr.AudioFile("temp_audio.wav") as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='en-GB')
            print(f"\nTranscription: {text}")
    else:
        print(f"Failed: {result.stderr}")
