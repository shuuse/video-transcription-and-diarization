import openai
import os
from dotenv import load_dotenv
from pydub import AudioSegment

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Paths
VIDEO_FOLDER = "./video"
OUTPUT_FOLDER = "./transcriptions"

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def convert_audio_to_wav(input_file, output_file):
    """Convert audio from input file to WAV format."""
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="wav")

def transcribe_audio(file_path):
    """Transcribe audio using OpenAI's Whisper API."""
    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript

def process_videos_in_folder(folder):
    """Process all video files in the specified folder."""
    for file_name in os.listdir(folder):
        if file_name.endswith((".mp4", ".mkv", ".avi", ".mov")):  # Add other video formats if needed
            input_path = os.path.join(folder, file_name)
            wav_path = os.path.join(folder, "temp_audio.wav")
            output_path = os.path.join(OUTPUT_FOLDER, f"{file_name}.txt")

            print(f"Processing {file_name}...")

            try:
                # Convert video to audio
                print("Converting audio to WAV format...")
                convert_audio_to_wav(input_path, wav_path)

                # Transcribe audio
                print("Transcribing audio...")
                transcript = transcribe_audio(wav_path)

                # Save transcription
                print(f"Saving transcription to {output_path}...")
                with open(output_path, "w") as output_file:
                    output_file.write(transcript["text"])

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

            finally:
                # Clean up temporary files
                if os.path.exists(wav_path):
                    os.remove(wav_path)

if __name__ == "__main__":
    print(f"Processing all video files in {VIDEO_FOLDER}...")
    process_videos_in_folder(VIDEO_FOLDER)
    print("All videos processed!")
