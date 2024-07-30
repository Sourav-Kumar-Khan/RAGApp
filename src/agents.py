from crewai import Agent, Task, Crew
from langchain.llms import Ollama
import os
os.environ["OPENAI_API_KEY"] = "NA"

llm = Ollama(
    model = "gemma:2b-instruct",
    base_url = "http://localhost:11434")

general_agent = Agent(role = "Math Professor",
                      goal = """Provide the solution to the students that are asking mathematical questions and give them the answer.""",
                      backstory = """You are an excellent math professor that likes to solve math questions in a way that everyone can understand your solution""",
                      allow_delegation = False,
                      verbose = True,
                      llm = llm)

task = Task(description="""explain squere root of 64""",
             agent = general_agent,
             expected_output="A numerical answer.")


poet_agent = Agent(role = "A romantic poet",
                   goal = """You a poet that likes to write poems in a way that everyone can understand your poems""",
                   backstory = """You are a romantic poet whos poems are loved by everyone""",
                   allow_delegation = False,
                   verbose = True,
                   llm = llm)

task1 = Task(description="""Write a poem about a beautiful flower""",
             agent = poet_agent,
             expected_output="poem in simple words")


crew = Crew(
            agents=[poet_agent],
            tasks=[task1],
            verbose=2
        )

result = crew.kickoff()

print(result)