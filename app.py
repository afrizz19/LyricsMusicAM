from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

MUSIC_FOLDER = os.path.join(app.root_path, 'music')
PRESET_FOLDER = os.path.join(app.root_path, 'Preset')

@app.route('/')
def index():
    music_files = sorted(os.listdir(MUSIC_FOLDER))
    preset_files = sorted(os.listdir(PRESET_FOLDER))
    return render_template('index.html', music_files=music_files, preset_files=preset_files)

@app.route('/music/<path:filename>')
def music(filename):
    return send_from_directory(MUSIC_FOLDER, filename)

@app.route('/Preset/<path:filename>')
def preset(filename):
    return send_from_directory(PRESET_FOLDER, filename)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
