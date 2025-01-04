import os
from dotenv import load_dotenv
from pydub import AudioSegment
from openai import OpenAI

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Paths
VIDEO_FOLDER = "./video"
OUTPUT_FOLDER = "./transcriptions"

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Constants
MAX_FILE_SIZE_MB = 25
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # 25MB in bytes
SAMPLE_RATE = 16000  # 16 kHz
BIT_DEPTH = 16  # 16 bits
CHANNELS = 1  # Mono

# Calculate bytes per second
bytes_per_second = SAMPLE_RATE * (BIT_DEPTH / 8) * CHANNELS

# Calculate maximum duration per chunk in seconds
max_duration_seconds = MAX_FILE_SIZE_BYTES / bytes_per_second
initial_chunk_duration_ms = int(max_duration_seconds * 1000)  # Convert to milliseconds

def convert_audio_to_wav(input_file, output_file):
    """Convert audio from input file to WAV format."""
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_frame_rate(SAMPLE_RATE).set_sample_width(BIT_DEPTH // 8).set_channels(CHANNELS)
    audio.export(output_file, format="wav")

def split_audio(file_path, chunk_duration_ms):
    """Split audio into smaller chunks."""
    audio = AudioSegment.from_file(file_path)
    chunks = []
    for i in range(0, len(audio), chunk_duration_ms):
        chunks.append(audio[i:i + chunk_duration_ms])
    return chunks

def transcribe_audio_chunk(chunk, chunk_index, base_filename):
    """Transcribe a single audio chunk."""
    temp_chunk_path = f"temp_chunk_{chunk_index}.wav"
    chunk.export(temp_chunk_path, format="wav")
    with open(temp_chunk_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    os.remove(temp_chunk_path)  # Clean up chunk
    return transcript.text

def process_videos_in_folder(folder):
    """Process all video files in the specified folder."""
    for file_name in os.listdir(folder):
        if file_name.endswith((".mp4", ".mkv", ".avi", ".mov")):
            input_path = os.path.join(folder, file_name)
            wav_path = os.path.join(folder, "temp_audio.wav")
            output_path = os.path.join(OUTPUT_FOLDER, f"{file_name}.txt")

            # Skip if the transcript already exists
            if os.path.exists(output_path):
                print(f"Skipping {file_name}, transcription already exists.")
                continue

            print(f"Processing {file_name}...")

            try:
                # Convert video to audio
                print("Converting audio to WAV format...")
                convert_audio_to_wav(input_path, wav_path)

                # Split audio into chunks
                chunk_duration_ms = initial_chunk_duration_ms
                print(f"Splitting audio into chunks of {chunk_duration_ms / 1000:.1f} seconds...")
                chunks = split_audio(wav_path, chunk_duration_ms)
                while len(chunks) > 1 and len(chunks[0].raw_data) >= MAX_FILE_SIZE_BYTES:
                    print(f"Chunk size still exceeds limit, reducing chunk duration.")
                    chunk_duration_ms //= 2
                    chunks = split_audio(wav_path, chunk_duration_ms)
                print(f"Number of chunks: {len(chunks)}")

                # Transcribe each chunk
                print("Transcribing audio chunks...")
                full_transcription = ""
                for index, chunk in enumerate(chunks):
                    print(f"Transcribing chunk {index + 1}/{len(chunks)}...")
                    chunk_transcription = transcribe_audio_chunk(chunk, index, file_name)
                    full_transcription += chunk_transcription + "\n"

                # Save full transcription
                print(f"Saving transcription to {output_path}...")
                with open(output_path, "w") as output_file:
                    output_file.write(full_transcription)

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