"""
Transcribe OGG audio using SpeechRecognition with online Google API
This version uploads the audio to Google's free API for transcription
"""
import speech_recognition as sr
import os

audio_file = "WhatsApp Ptt 2025-12-01 at 12.02.34 PM.ogg"

print(f"🎤 Transcribing: {audio_file}")
print("=" * 70)

# Initialize recognizer
recognizer = sr.Recognizer()

# Since OGG format isn't natively supported, we'll read it as raw audio
# and let Google's API handle the heavy lifting
print("📤 Uploading audio to Google Speech API for transcription...")
print("(This may take a moment...)")

try:
    # Read the audio file
    with open(audio_file, 'rb') as f:
        audio_content = f.read()
    
    print(f"✅ Audio file loaded ({len(audio_content)} bytes)")
    print("🔍 Sending to Google for transcription...")
    
    # Use the audio data directly - Google API can handle OGG
    # We'll try with opus codec which WhatsApp uses
    from speech_recognition import AudioData
    
    # Create AudioData object (sample rate for WhatsApp is typically 48000 or 16000)
    # Try with common WhatsApp settings
    for sample_rate in [48000, 16000, 44100]:
        try:
            print(f"Trying sample rate: {sample_rate} Hz...")
            audio_data = AudioData(audio_content, sample_rate, 2)
            
            # Attempt transcription
            text = recognizer.recognize_google(audio_data, language='en-GB')
            
            print("\n" + "=" * 70)
            print("📄 TRANSCRIPTION SUCCESS!")
            print("=" * 70)
            print(text)
            print("=" * 70)
            
            # Save to file
            with open("tutor_feedback_transcription.txt", "w", encoding="utf-8") as output:
                output.write("TUTOR FEEDBACK - WhatsApp Voice Note Transcription\n")
                output.write("=" * 70 + "\n")
                output.write(f"File: {audio_file}\n")
                output.write("=" * 70 + "\n\n")
                output.write(text)
                output.write("\n\n" + "=" * 70 + "\n")
                output.write("\nNote: This is an automated transcription. ")
                output.write("Multiple speakers may be present.\n")
            
            print(f"\n✅ Transcription saved to: tutor_feedback_transcription.txt")
            exit(0)
            
        except Exception as e:
            print(f"  ❌ Failed with {sample_rate} Hz: {str(e)[:50]}...")
            continue
    
    print("\n❌ All sample rates failed. The audio format may need conversion.")
    print("ℹ️  WhatsApp uses Opus codec in OGG container which needs special handling.")
    
except FileNotFoundError:
    print(f"❌ File not found: {audio_file}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
