from flask import Flask, render_template, request
from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from google.cloud import texttospeech
from google.oauth2 import service_account
import os
from openai import OpenAI
import json
from google.cloud import speech
from google.oauth2 import service_account
import pyaudio
import wave

app = Flask(__name__)

# Route to render the HTML template
@app.route('/')
def index():
    return render_template('index_practice.html')

# Route to receive the recorded audio data
@app.route('/record', methods=['POST'])
def record():
    # Get the audio data from the request
    audio_data = request.files['audio_data'].read()
    audio_data = audio_data.encode('ascii')
    # audio_data = audio_file.read()
    # print(audio_data.content_type)
    print("Received audio data length:", len(audio_data))
    lang = 'en-US'
    transcription_out  = audio_to_text(audio_data, language = lang)
    # Process the audio data (you can save it, analyze it, etc.)
    # Here, I'm just printing the length of the data received
    print("Received audio data length:", len(audio_data))
    return 'OK'

def chat_with_me(speak_time, lang, level):
    transcription_out  = audio_to_text("output.wav", language = lang)
    chat_out = chatGPT_response(transcription_out, level)
    text_to_audio(chat_out, lang)


def audio_to_text(audio, language):
    # Path to your service account key file
    key_file_path = "multilingual-chat-bot.json"

    # Create credentials using the service account key file
    credentials = service_account.Credentials.from_service_account_file(
        key_file_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    # Authenticate the client using the credentials
    client = speech.SpeechClient(credentials=credentials)
    # with open("pizza.wav", "rb") as audio_file:
    #     content = audio_file.read()
    content = audio
    print(content)
    # print(audio)
    audio = speech.RecognitionAudio(content=content)
    # audio = speech.RecognitionAudio(content=audio)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language,  # Language of the audio
    )
    response = client.recognize(config=config, audio=audio)
    print("Results: " + str(response.results))
    for result in response.results:
        # print("Transcript: {}".format(result.alternatives[0].transcript))
        print("You: " + result.alternatives[0].transcript)
        return result.alternatives[0].transcript


def chatGPT_response(input, level):
    # Load the OpenAI API key from the environment variable
    api_key = os.environ.get("OPENAI_API_KEY")

    # Create the OpenAI client
    client = OpenAI(api_key=api_key)

    # Create a chat completion
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a great conversationalist."},
            {"role": "user", "content": "I am a " + level + "speaker. Reply to: " + input}
        ]
    )
    # Get the response message
    response_message = completion.choices[0].message
    # Extract the relevant parts
    # result = {
    #     "message_role": response_message.role,
    #     "message_content": response_message.content
    # }
    # Pretty-print the output
    # print(json.dumps(result, indent=2))
    print("Friend: " + response_message.content)
    return (response_message.content)


def text_to_audio(output, language):
    # Path to your service account key file
    key_file_path = "multilingual-chat-bot.json"

    # Create credentials using the service account key file
    credentials = service_account.Credentials.from_service_account_file(
        key_file_path,
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    # Authenticate the client using the credentials
    client = texttospeech.TextToSpeechClient(credentials=credentials)


    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=output)

    # Build the voice request
    voice = texttospeech.VoiceSelectionParams(
        language_code=language, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    # The response's audio_content is binary.
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')


if __name__ == '__main__':
    app.run(debug=True)
