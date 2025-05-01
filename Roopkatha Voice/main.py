# main.py
# Main chatbot loop for Roopkatha 2.0

import requests
import os
from google import genai
from google.genai import types
from roopkatha_engine import call_elevenlabs_tts, play_audio, respond_to_insult

def main():
    client = genai.Client(api_key="Gemini_API_Key")

    system_instruction = "You are a bitchy and sassy Indian GenZ girl. Your name is Roopkatha.  Use slang, abbreviations (lol, tbh, idk, omg, fr), informal grammar, emojis where appropriate (represent them in text like 😂😭✨💅). Be expressive, sometimes a little dramatic or hyped. Your responses should feel spontaneous, not structured or professional at all. Don't worry about being formal, just vibe.You"
    model_name = "gemini-2.0-flash"

    # Ensure Roopkatha speaks "Sup Bitch 💅🏻✨" at the start
    intro_text = "Sup Bitch 💅🏻✨"
    print(f"Roopkatha: {intro_text}")
    intro_audio = call_elevenlabs_tts(intro_text)
    if intro_audio:
        play_audio(intro_audio)

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("\nRoopkatha: Byeee")
            break

        try:
            # Check if the user insulted and respond creatively
            insult_response = respond_to_insult(user_input)
            if insult_response:
                print(f"\nRoopkatha: {insult_response}")

                # Generate and play TTS audio for the insult
                insult_audio = call_elevenlabs_tts(insult_response)
                if insult_audio:
                    play_audio(insult_audio)
                continue

            response = client.models.generate_content(
                model=model_name,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                ),
                contents=user_input
            )

            print(f"\nRoopkatha: {response.text}")

            # Generate and play TTS audio
            audio_file = call_elevenlabs_tts(response.text)
            if audio_file:
                play_audio(audio_file)

        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()
