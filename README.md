
# Video Transcription and Diarization

This project provides a Python-based solution for transcribing video files to text using OpenAI's Whisper API. It supports batch processing of all video files in a folder and saves the transcriptions as `.txt` files. The script also includes functionality to dynamically adjust chunk sizes to handle API size limits.

## Features

- **Batch Processing**: Transcribes all video files in the specified folder.
- **File Format Support**: Supports `.mp4`, `.mkv`, `.avi`, `.mov`, and more.
- **Dynamic Chunk Splitting**: Automatically adjusts chunk size to ensure API compatibility.
- **Skips Processed Videos**: Avoids reprocessing files with existing transcriptions.

## Requirements

### Python Environment
- Python 3.10 or higher

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/shuuse/video-transcription-and-diarization
   cd video_transcription_and_diarization
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Dependencies
The minimal dependencies are:
```plaintext
openai==1.59.3
pydub==0.25.1
python-dotenv==1.0.1
```

### Additional Requirements
- `ffmpeg` must be installed on your system for audio processing. Install it via Homebrew (macOS):
  ```bash
  brew install ffmpeg
  ```

## Usage

1. Add your OpenAI API key to a `.env` file:
   ```plaintext
   OPENAI_API_KEY=your_api_key_here
   ```

2. Place your video files in the `/video` folder.

3. Run the script:
   ```bash
   python transcribe.py
   ```

4. Transcriptions will be saved in the `/transcriptions` folder.

## Notes

- Ensure your audio files are under the OpenAI Whisper API's file size limit of 25MB. The script dynamically splits audio files to handle this.
- Videos with existing transcriptions are skipped to save time.

## Future Enhancements

- Add support for advanced speaker diarization.
- Extend file format compatibility.

## License

This project is licensed under the MIT License.
