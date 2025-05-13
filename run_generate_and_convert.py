import sys
import subprocess
import os
import argparse

def run_generate_subtitles(audio_path, model="base", offset=0.0):
    """Run generate_subtitles.py to create an SRT subtitle file."""
    cmd = [
        sys.executable, "generate_subtitles.py", audio_path,
        "--format", "srt",
        "--model", model,
        "--offset", str(offset)
    ]
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error running generate_subtitles.py:\n{result.stderr}")
        sys.exit(result.returncode)

def run_srt_to_basexml(srt_path, output_xml=None):
    """Run srt_to_basexml.py to convert SRT to base XML."""
    cmd = [sys.executable, "srt_to_basexml.py", srt_path]
    if output_xml:
        cmd.append(output_xml)
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error running srt_to_basexml.py:\n{result.stderr}")
        sys.exit(result.returncode)

def main():
    parser = argparse.ArgumentParser(description="Run generate_subtitles.py then srt_to_basexml.py sequentially.")
    parser.add_argument("audio_path", help="Path to the audio file")
    parser.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"], help="Whisper model size")
    parser.add_argument("--offset", type=float, default=0.0, help="Offset in seconds for subtitles")

    args = parser.parse_args()

    audio_path = args.audio_path
    model = args.model
    offset = args.offset

    if not os.path.isfile(audio_path):
        print(f"Audio file not found: {audio_path}")
        sys.exit(1)

    # Generate subtitle SRT file path
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    srt_path = os.path.join("subtitle", f"{base_name}.srt")

    # Run generate_subtitles.py
    run_generate_subtitles(audio_path, model=model, offset=offset)

    # Run srt_to_basexml.py on generated SRT
    run_srt_to_basexml(srt_path)

if __name__ == "__main__":
    main()
