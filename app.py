from flask import Flask, render_template, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record', methods=['POST'])
def record():
    language = request.form['language']
    age = request.form['age']
    level = request.form['level']

    # Dummy implementation for recording speech
    # Replace this with actual speech-to-text logic
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    # Save the recorded speech to an MP3 file
    audio_file = f"recordings/{language}_{age}_{level}.mp3"
    with open(audio_file, "wb") as f:
        f.write(audio.get_wav_data())

    return jsonify({'audio_file': audio_file})

if __name__ == '__main__':
    app.run(debug=True)
