import openai
import speech_recognition as sr
import asyncio
import edge_tts
import playsound

openai.api_key = "your-openai-api-key"  # Replace with your real key

# Realistic voice output using Edge TTS
async def speak(text):
    communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural")
    await communicate.save("response.mp3")
    playsound.playsound("response.mp3")

# Simple ChatGPT request
def get_chatgpt_response(query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content

# Listen using SpeechRecognition + Google API
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            print(f"🗣️ You said: {query}")
            return query
        except:
            return "Sorry, I couldn't understand that."

# Main loop
while True:
    user_query = listen()
    if user_query.lower() in ["exit", "quit", "stop"]:
        asyncio.run(speak("Goodbye!"))
        break

    ai_response = get_chatgpt_response(user_query)
    print(f"🤖: {ai_response}")
    asyncio.run(speak(ai_response))