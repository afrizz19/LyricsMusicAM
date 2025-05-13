# LYRICS TO XML

This project provides tools to generate subtitles from audio files using OpenAI's Whisper model, convert subtitle files from SRT format to a custom BaseXML format, and run the entire process sequentially.

## Prerequisites

- Python 3.7 or higher
- Install required Python packages:
  ```bash
  pip install -r requirements.txt
  ```
- The Whisper model will be downloaded automatically when running the scripts.

## Folder Structure

- `generate_subtitles.py`: Script to transcribe audio and generate subtitles in SRT or XML-like format.
- `srt_to_basexml.py`: Script to convert SRT subtitle files to BaseXML format used by the project.
- `run_generate_and_convert.py`: Script to run the subtitle generation and conversion sequentially.
- `subtitle/`: Folder where generated subtitle files (SRT/XML) are saved.
- `Preset/`: Folder where BaseXML files are saved.
- `base.xml`: Example or base XML file.
- `music/`: Folder for audio files (not included in this repo).
- `subtitle/`: Folder for subtitle files.

## Usage

### 1. Generate Subtitles from Audio

Run the `generate_subtitles.py` script with the path to your audio file:

```bash
python generate_subtitles.py path/to/audio.mp3 [--format srt|xml] [--offset seconds] [--model tiny|base|small|medium|large]
```

- `--format`: Output subtitle format, either `srt` (default) or `xml`.
- `--offset`: Optional time offset in seconds to adjust subtitle timestamps.
- `--model`: Whisper model size to use (default is `base`).

Example:

```bash
python generate_subtitles.py music/song.mp3 --format srt --model small
```

The generated subtitle file will be saved in the `subtitle/` folder.

### 2. Convert SRT to BaseXML

Convert an existing SRT subtitle file to BaseXML format using:

```bash
python srt_to_basexml.py path/to/subtitle.srt [output.xml]
```

- If `output.xml` is not provided, the output will be saved as `Preset/{subtitle_basename}.xml`.

Example:

```bash
python srt_to_basexml.py subtitle/song.srt
```

### 3. Run Subtitle Generation and Conversion Sequentially

Use the `run_generate_and_convert.py` script to generate subtitles from audio and convert them to BaseXML in one step:

```bash
python run_generate_and_convert.py path/to/audio.mp3 [--model tiny|base|small|medium|large] [--offset seconds]
```

Example:

```bash
python run_generate_and_convert.py music/song.mp3 --model base --offset 0.5
```

## Notes

- Ensure your audio files are placed in the `music/` folder or provide the correct path.
- Generated subtitles are saved in the `subtitle/` folder.
- Converted BaseXML files are saved in the `Preset/` folder.
- The Whisper model will be downloaded automatically on first run.

## License

This project is provided as-is without warranty.
