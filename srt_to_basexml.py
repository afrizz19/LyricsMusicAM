import xml.etree.ElementTree as ET
import re
import os

def srt_time_to_milliseconds(srt_time):
    """Convert SRT time format HH:MM:SS,mmm to milliseconds."""
    hours, minutes, seconds_millis = srt_time.split(':')
    seconds, millis = seconds_millis.split(',')
    total_millis = (int(hours) * 3600 + int(minutes) * 60 + int(seconds)) * 1000 + int(millis)
    return total_millis

def parse_srt(srt_path):
    """Parse the SRT file and return a list of subtitles with start, end, and text."""
    subtitles = []
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Updated regex to handle multiple consecutive subtitles with word-level timestamps
    pattern = re.compile(r'(\d+)\s+(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s+([\s\S]*?)(?=\n\n|\Z)', re.MULTILINE)
    matches = pattern.findall(content)
    for match in matches:
        index, start, end, text = match
        subtitles.append({
            'index': int(index),
            'start': srt_time_to_milliseconds(start),
            'end': srt_time_to_milliseconds(end),
            'text': text.strip()
        })
    return subtitles

def create_basexml(subtitles, output_path, title):
    """Create an XML file similar to base.xml from subtitles."""
    scene_attrs = {
        'title': title,
        'width': "1920",
        'height': "1080",
        'exportWidth': "1920",
        'exportHeight': "1080",
        'precompose': "dynamicResolution",
        'bgcolor': "#ff000000",
        'totalTime': str(max(s['end'] for s in subtitles)),
        'fps': "60",
        'modifiedTime': "1746959521184",
        'amver': "1028383",
        'ffver': "106",
        'am': "com.alightcreative.motion/5.0.272.1028383",
        'amplatform': "android",
        'retime': "freeze",
        'retimeAdaptFPS': "false"
    }
    scene = ET.Element('scene', scene_attrs)

    # Default attributes for <text> elements
    default_text_attrs = {
        'fillType': "color",
        'mediaFillMode': "fill",
        'size': "40.000000",
        'font': "imported?name=Coolvetica Rg.ttf",
        'wrapWidth': "512",
        'align': "center",
    }
    default_location_value = "960.000000,540.000000,0.000000"
    default_fillColor_value = "#ff7f7f7f"

    for i, subtitle in enumerate(subtitles, start=1):
        text_attrs = {
            'id': str(10218664 + i),  # generate unique id by offset
            'startTime': str(subtitle['start']),
            'endTime': str(subtitle['end']),
            **default_text_attrs
        }
        text_elem = ET.SubElement(scene, 'text', text_attrs)

        transform = ET.SubElement(text_elem, 'transform')
        location = ET.SubElement(transform, 'location', {'value': default_location_value})

        fillColor = ET.SubElement(text_elem, 'fillColor', {'value': default_fillColor_value})

        content = ET.SubElement(text_elem, 'content')
        content.text = subtitle['text']

    tree = ET.ElementTree(scene)
    # Write XML declaration and pretty print
    import xml.dom.minidom
    xml_str = ET.tostring(scene, encoding='utf-8')
    pretty_xml = xml.dom.minidom.parseString(xml_str).toprettyxml(indent="  ", encoding='utf-8')

    # Create Preset folder if it doesn't exist
    output_folder = "Preset"
    os.makedirs(output_folder, exist_ok=True)

    # If output_path is just a filename, prepend Preset folder
    if not os.path.dirname(output_path):
        output_path = os.path.join(output_folder, output_path)

    with open(output_path, 'wb') as f:
        f.write(pretty_xml)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python srt_to_basexml.py input.srt [output.xml]")
        sys.exit(1)
    srt_path = sys.argv[1]

    # Construct output path if not provided
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        base_name = os.path.splitext(os.path.basename(srt_path))[0]
        output_path = f"{base_name}.xml"

    subs = parse_srt(srt_path)
    try:
        create_basexml(subs, output_path, base_name)
        print(f"Converted {srt_path} to {output_path} successfully.")
    except ValueError as e:
        print(f"Error: {e}")
    
    
