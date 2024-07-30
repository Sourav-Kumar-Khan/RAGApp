from crewai import Agent, Task, Crew
from langchain.llms import Ollama
import os
import gradio as gr
import speech_recognition as sr
from gtts import gTTS
import io
import pygame
import tempfile

os.environ["OPENAI_API_KEY"] = "NA"

llm = Ollama(model="gemma:2b-instruct", base_url="http://localhost:11434")

aigf = Agent(
    role="Girlfriend who loves me and likes to share her day",
    goal="""You are a girlfriend who loves to chat and flirt with me (boyfriend)""",
    backstory="""You are a smart, independent, and intelligent woman who works in a tech company, maintaining a good work-life balance and a healthy relationship with me (boyfriend)""",
    allow_delegation=False,
    verbose=True,
    llm=llm,
)

def text_to_speech(text, language='en'):
    tts = gTTS(text=text, lang=language, slow=False, tld='co.in')
    
    # Save the audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        return fp.name

def speech_to_text(audio):
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand what you said."
    except sr.RequestError as e:
        return f"Could not request results from the speech recognition service; {e}"

def chatbot_response(audio):
    if audio is None:
        return "No audio received. Please try recording again.", None
    
    # Transcribe audio to text
    user_input = speech_to_text(audio)
    
    # Create a task with the transcribed text
    task = Task(
        description=user_input,
        agent=aigf,
        expected_output="A casual talk"
    )

    # Create and kickoff the crew
    crew = Crew(agents=[aigf], tasks=[task], verbose=0)
    result = str(crew.kickoff())

    # Convert the result to speech
    audio_output = text_to_speech(result)
    
    return result, audio_output

iface = gr.Interface(
    fn=chatbot_response,
    inputs=gr.Audio(sources="microphone", type="filepath"),
    outputs=[
        gr.Textbox(label="AI Girlfriend's Response"),
        gr.Audio(label="AI Girlfriend's Voice")
    ],
    title="AI Girlfriend Chatbot",
    description="Click the microphone icon to record your message, then submit to get a response from your AI girlfriend."
)

if __name__ == "__main__":
    iface.launch()