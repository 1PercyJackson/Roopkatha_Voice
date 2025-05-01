# roopkatha_engine.py
# Core class and functions for Roopkatha 2.0

import random
import requests
import os
import playsound
import whisper

def genzify_text(input_text):
    """Transform text to a more dramatic, TikTok-style vibe."""
    # Example transformation logic
    return input_text.replace("Omg", "OMGGGGG").replace("can't", "can'tttt")

def detect_mood(input_text):
    """Detect the mood of the text: Hype, Calm, Whisper, Angry."""
    if any(word in input_text.lower() for word in ["omg", "wow", "amazing"]):
        return "HYPE", {"stability": 0.2, "similarity_boost": 0.85}
    return "CALM", {"stability": 0.7, "similarity_boost": 0.5}

def insert_laughs(input_text):
    """Insert random giggles or laughs into the text."""
    if any(word in input_text.lower() for word in ["lol", "lmao", "dead", "😭"]):
        return input_text + " 😂"
    if random.random() > 0.7:  # Random chance for giggles
        return input_text + " hehe"
    return input_text

def adjust_voice_settings(mood):
    """Adjust voice settings dynamically based on mood."""
    settings = {
        "HYPE": {"stability": 0.2, "similarity_boost": 0.85},
        "CALM": {"stability": 0.7, "similarity_boost": 0.5},
    }
    return settings.get(mood, {"stability": 0.5, "similarity_boost": 0.5})

def process_text(input_text):
    """Main processing pipeline for Roopkatha 2.0."""
    genzified_text = genzify_text(input_text)
    mood, voice_settings = detect_mood(genzified_text)
    text_with_laughs = insert_laughs(genzified_text)
    return text_with_laughs, mood, voice_settings

def call_gemini_api(input_text, verify_ssl=True):
    """Call the Gemini API to process the input text."""
    api_key = "AIzaSyCWdj62P-i_ju2CSG1RodABlAyb7vJpjow"
    url = "https://gemini-2.0-flash.googleapis.com/v1/processText"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"text": input_text}

    try:
        response = requests.post(url, json=payload, headers=headers, verify=verify_ssl)
        if response.status_code == 200:
            return response.json().get("processedText", input_text)
        else:
            print(f"Gemini API Error: {response.status_code} - {response.text}")
            return input_text
    except requests.exceptions.SSLError as e:
        print(f"SSL Error: {e}")
        return input_text

def call_elevenlabs_tts(text):
    """Call the ElevenLabs API to generate TTS audio with reduced lag."""
    api_key = "sk_24abd3729f0f8bfafa8dd211b66ef9da0b157de9f9c3d5d2"
    voice_id = "FGY2WhTYpPnrIDTdsKH5"
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.3,  # Adjusted for more energetic tone
            "similarity_boost": 0.9  # Higher similarity for hyped vibe
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        audio_file = "response_audio.mp3"
        with open(audio_file, "wb") as file:
            file.write(response.content)
        return audio_file
    else:
        print(f"ElevenLabs API Error: {response.status_code} - {response.text}")
        return None

def play_audio(file_path):
    """Play the generated audio file."""
    if os.path.exists(file_path):
        playsound.playsound(file_path)
        os.remove(file_path)  # Clean up after playing
    else:
        print("Audio file not found.")

def process_text_with_apis(input_text):
    """Pipeline to process text using Gemini and ElevenLabs APIs."""
    genzified_text = call_gemini_api(input_text, verify_ssl=False)  # Disable SSL verification temporarily
    mood, voice_settings = detect_mood(genzified_text)
    text_with_laughs = insert_laughs(genzified_text)
    audio_file = call_elevenlabs_tts(text_with_laughs)
    if audio_file:
        play_audio(audio_file)
    return text_with_laughs, mood, voice_settings, audio_file

def detect_audio_features(audio_file):
    """Use Whisper to detect accents, tones, modes, base, and language from audio."""
    model = whisper.load_model("base")
    result = model.transcribe(audio_file, task="transcribe", language=None)

    detected_language = result.get("language", "unknown")
    transcription = result.get("text", "")

    print(f"Detected Language: {detected_language}")
    print(f"Transcription: {transcription}")

    return {
        "language": detected_language,
        "transcription": transcription
    }

def voice_to_voice(input_audio_file):
    """Convert input audio to text and back to audio with ElevenLabs."""
    # Detect features from the input audio
    features = detect_audio_features(input_audio_file)

    # Generate a response based on the transcription
    response_text = f"You said: {features['transcription']} in {features['language']} language."

    # Convert the response text back to audio
    response_audio = call_elevenlabs_tts(response_text)

    if response_audio:
        play_audio(response_audio)

    return response_audio

def generate_insult():
    """Generate a creative insult."""
    insults = [
        "You're like a cloud. When you disappear, it's a beautiful day!",
        "You bring everyone so much joy... when you leave the room.",
        "You're proof that even the worst mistakes can be useful as bad examples.",
        "You're like a software bug—annoying and hard to get rid of!",
        "You're the human version of a 404 error."
    ]
    return random.choice(insults)

def respond_to_insult(user_input):
    """Check if the user insulted and respond creatively."""
    insults = ["stupid", "idiot", "dumb", "loser", "fool"]  # Add more trigger words as needed
    if any(insult in user_input.lower() for insult in insults):
        return generate_insult()
    return None