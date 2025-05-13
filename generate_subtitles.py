import sys
import os
import whisper

def format_timestamp(seconds: float) -> str:
    """Format seconds to SRT timestamp format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

def seconds_to_milliseconds(seconds: float) -> int:
    """Convert seconds to integer milliseconds."""
    return int(seconds * 1000)

def write_srt(transcript, srt_path, offset=0.0):
    """Write the transcript segments to an SRT file with optional offset in seconds."""  
    def apply_offset(time_sec):
        adjusted = time_sec - offset
        return max(adjusted, 0.0)

    with open(srt_path, "w", encoding="utf-8") as f:
        index = 1
        for segment in transcript['segments']:
            # If word-level timestamps are available, write each word as a separate subtitle
            if 'words' in segment:
                for word_info in segment['words']:
                    start = format_timestamp(apply_offset(word_info['start']))
                    end = format_timestamp(apply_offset(word_info['end']))
                    text = word_info['word'].strip()
                    f.write(f"{index}\n{start} --> {end}\n{text}\n\n")
                    index += 1
            else:
                start = format_timestamp(apply_offset(segment['start']))
                end = format_timestamp(apply_offset(segment['end']))
                text = segment['text'].strip()
                f.write(f"{index}\n{start} --> {end}\n{text}\n\n")
                index += 1

def write_xml_like(transcript, xml_path, offset=0.0):
    """Write the transcript segments to an XML-like file with startTime and endTime in milliseconds and optional offset."""  
    def apply_offset(time_sec):
        adjusted = time_sec - offset
        return max(adjusted, 0.0)

    with open(xml_path, "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<subtitles>\n')
        index = 1
        for segment in transcript['segments']:
            if 'words' in segment:
                for word_info in segment['words']:
                    start = seconds_to_milliseconds(apply_offset(word_info['start']))
                    end = seconds_to_milliseconds(apply_offset(word_info['end']))
                    text = word_info['word'].strip()
                    f.write(f'  <subtitle id="{index}" startTime="{start}" endTime="{end}">\n')
                    f.write(f'    <text>{text}</text>\n')
                    f.write('  </subtitle>\n')
                    index += 1
            else:
                start = seconds_to_milliseconds(apply_offset(segment['start']))
                end = seconds_to_milliseconds(apply_offset(segment['end']))
                text = segment['text'].strip()
                f.write(f'  <subtitle id="{index}" startTime="{start}" endTime="{end}">\n')
                f.write(f'    <text>{text}</text>\n')
                f.write('  </subtitle>\n')
                index += 1
        f.write('</subtitles>\n')

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_subtitles.py path/to/audio.mp3 [--format xml|srt] [--offset seconds] [--model base|small|medium|large]")
        sys.exit(1)

    audio_path = sys.argv[1]

    # Default output format is srt
    output_format = "srt"
    if "--format" in sys.argv:
        format_index = sys.argv.index("--format") + 1
        if format_index < len(sys.argv):
            output_format = sys.argv[format_index].lower()
            if output_format not in ("srt", "xml"):
                print("Invalid format specified. Use 'srt' or 'xml'.")
                sys.exit(1)

    # Default offset is 0.0 seconds
    offset = 0.0
    if "--offset" in sys.argv:
        offset_index = sys.argv.index("--offset") + 1
        if offset_index < len(sys.argv):
            try:
                offset = float(sys.argv[offset_index])
            except ValueError:
                print("Invalid offset value. Must be a number.")
                sys.exit(1)

    # Default model is base
    model_size = "base"
    if "--model" in sys.argv:
        model_index = sys.argv.index("--model") + 1
        if model_index < len(sys.argv):
            model_size = sys.argv[model_index].lower()
            if model_size not in ("tiny", "base", "small", "medium", "large"):
                print("Invalid model size specified. Use one of: tiny, base, small, medium, large.")
                sys.exit(1)

    if not os.path.isfile(audio_path):
        print(f"Audio file not found: {audio_path}")
        sys.exit(1)

    # Create subtitle folder if it doesn't exist
    output_folder = "subtitle"
    os.makedirs(output_folder, exist_ok=True)

    # Construct output filename based on audio filename and format
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    output_path = os.path.join(output_folder, f"{base_name}.{output_format}")

    print(f"Loading Whisper model '{model_size}'...")
    model = whisper.load_model(model_size)

    print(f"Transcribing audio file: {audio_path}")
    # Enable word-level timestamps
    result = model.transcribe(audio_path, word_timestamps=True)

    # Log the start time of the first segment for debugging
    if 'segments' in result and len(result['segments']) > 0:
        first_start = result['segments'][0]['start']
        print(f"DEBUG: Start time of first detected segment: {first_start} seconds")

    print(f"Writing subtitles to: {output_path}")
    if output_format == "srt":
        write_srt(result, output_path, offset=offset)
    else:
        write_xml_like(result, output_path, offset=offset)

    print("Subtitle generation completed.")

if __name__ == "__main__":
    main()
