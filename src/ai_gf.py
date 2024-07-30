from crewai import Agent, Task, Crew
from langchain.llms import Ollama
import os
from tts import text_to_speech, speech_to_text

os.environ["OPENAI_API_KEY"] = "NA"

llm = Ollama(model="gemma:2b-instruct", base_url="http://localhost:11434")

aigf = Agent(
    role="Girlfriend who loves me and like to share her day",
    goal="""You are a girlfriend who loves to chat and flirt with me (boyfriend)""",
    backstory="""You are a smart, indepedent, and intelligent women who works in a tech company, mentaning a good work-life balance and a healthy relationship with me(boyfriend)""",
    allow_delegation=False,
    verbose=True,
    llm=llm,
)

while True:
    task = Task(
        description=speech_to_text(), agent=aigf, expected_output="A casual talk"
    )

    crew = Crew(agents=[aigf], tasks=[task], verbose=0)

    result = crew.kickoff()
    text_to_speech(str(result))
