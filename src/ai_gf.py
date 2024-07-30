from crewai import Agent, Task, Crew
from langchain.llms import Ollama
import os
import gradio as gr
import speech_recognition as sr
from gtts import gTTS
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

def chatbot_response(audio, history):
    if audio is None:
        return history, history, None
    
    user_input = speech_to_text(audio)
    
    # Add user message to history
    history.append(("You", user_input))
    
    # Prepare the full conversation context
    conversation_context = "\n".join([f"{speaker}: {message}" for speaker, message in history])
    
    task = Task(
        description=f"Respond to the following conversation, focusing on the last message:\n\n{conversation_context}",
        agent=aigf,
        expected_output="A casual response continuing the conversation"
    )

    crew = Crew(agents=[aigf], tasks=[task], verbose=0)
    result = str(crew.kickoff())

    # Add AI response to history
    history.append(("AI Girlfriend", result))

    audio_output = text_to_speech(result)
    
    return history, history, audio_output

iface = gr.Interface(
    fn=chatbot_response,
    inputs=[
        gr.Audio(sources="microphone", type="filepath"),
        gr.State([])
    ],
    outputs=[
        gr.Chatbot(label="Conversation"),
        gr.State(),
        gr.Audio(label="AI Girlfriend's Voice")
    ],
    title="Chat with your AI Girlfriend",
    description="Have a continuous conversation with your AI girlfriend. Click the microphone icon to record your message, then submit to get a response.",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch()